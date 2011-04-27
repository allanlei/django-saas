from django.db import models
from django.conf import settings
from django.utils import simplejson as json

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
        if not self.is_loaded():
            settings.DATABASES[self.db] = self.settings
    
    def unload(self):
        if self.is_loaded():
            del settings.DATABASES[self.db]


from signals import create_db, drop_db
if getattr(settings, 'SAAS_MULTIDB_AUTOCREATE', True): models.signals.post_save.connect(create_db, sender=Database)
if getattr(settings, 'SAAS_MULTIDB_AUTODROP', True):models.signals.post_delete.connect(drop_db, sender=Database)
