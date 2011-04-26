from django.db import models
from django.conf import settings
from django.utils import simplejson as json

class Database(models.Model):
    ENGINES = (
        ('django.db.backends.postgresql_psycopg2', 'django.db.backends.postgresql_psycopg2'),
        ('django.db.backends.mysql', 'django.db.backends.mysql'),
        ('django.db.backends.sqlite3', 'django.db.backends.sqlite3'),
        ('django.db.backends.oracle', 'django.db.backends.oracle'),
    )

    db = models.CharField(max_length=256, primary_key=True)
    
    engine = models.CharField(max_length=48, choices=ENGINES)
    name = models.CharField(max_length=256)
    user = models.CharField(max_length=24, blank=True)
    password = models.CharField(max_length=512, blank=True)
    host = models.CharField(max_length=96, blank=True)
    port = models.CharField(max_length=24, blank=True)
    extra = models.TextField(blank=True)
    
    def to_dict(self):
        return {
            'ENGINE': self.engine,
            'NAME': self.name,
            'USER': self.user,
            'PASSWORD': self.password,
            'HOST': self.host,
            'PORT': self.port,
        }
        
    def load(self):
        raise NotImplementedError
#        settings.DATABASES.update(self.to_dict())
