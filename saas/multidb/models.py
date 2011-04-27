from django.db import models
from django.conf import settings
from django.utils import simplejson as json

import managers
from signals import db_pre_load, db_post_load, db_pre_unload, db_post_unload


DEFAULT = settings.DATABASES['default']

class Database(models.Model):
    ENGINES = (
        ('django.db.backends.postgresql_psycopg2', 'django.db.backends.postgresql_psycopg2'),
        ('django.db.backends.postgresql', 'django.db.backends.postgresql'),
        ('django.db.backends.mysql', 'django.db.backends.mysql'),
        ('django.db.backends.sqlite3', 'django.db.backends.sqlite3'),
        ('django.db.backends.oracle', 'django.db.backends.oracle'),
    )

    db = models.CharField(max_length=256, primary_key=True, help_text='The database name that goes into Django settings')
    
    engine = models.CharField(max_length=48, default=DEFAULT['ENGINE'], choices=ENGINES, help_text='Django database engine type')
    name = models.CharField(max_length=256, null=False, blank=False, help_text='The name of the database')
    user = models.CharField(max_length=24, blank=True, default=DEFAULT['USER'], help_text='The database user')
    password = models.CharField(max_length=512, blank=True, default=DEFAULT['PASSWORD'], help_text='The password for the database user. Encrypted')
    host = models.CharField(max_length=96, blank=True, default=DEFAULT['HOST'], help_text='The hostname of the database server')
    port = models.CharField(max_length=24, blank=True, default=DEFAULT['PORT'], help_text='The port of the database server')
    extra = models.TextField(blank=True)
    
    objects = managers.DatabaseManager()
    
    def __unicode__(self):
        return u'%s(%s)' % (self.db, self.engine.split('.')[-1])
        
    @property
    def settings(self):
        return {
            'ENGINE': self.engine,
            'NAME': self.name,
            'USER': self.user,
            'PASSWORD': self.password,
            'HOST': self.host,
            'PORT': self.port,
        }
    
    def is_loaded(self):
        return self.db in settings.DATABASES
        
    def load(self):
        db_pre_load.send(sender=self.__class__, instance=self)
        loaded = False
        if not self.is_loaded():
            settings.DATABASES[self.db] = self.settings
            loaded = True
        db_post_load.send(sender=self.__class__, instance=self, loaded=loaded)
    
    def unload(self):
        db_pre_unload.send(sender=self.__class__, instance=self)
        if self.is_loaded():
            del settings.DATABASES[self.db]
        db_post_unload.send(sender=self.__class__, instance=self)
    
    def __enter__(self):
        self.load()
    
    def __exit__(self, **exceptions):
        self.unload()


from signals import create_db, drop_db, unload_db
if getattr(settings, 'SAAS_MULTIDB_AUTOCREATE', True): models.signals.post_save.connect(create_db, sender=Database)
if getattr(settings, 'SAAS_MULTIDB_AUTODROP', True): models.signals.post_delete.connect(drop_db, sender=Database)
if getattr(settings, 'SAAS_MULTIDB_AUTOUNLOAD', True): models.signals.post_delete.connect(unload_db, sender=Database)
