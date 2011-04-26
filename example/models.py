from django.db import models

class TestData(models.Model):
    name = models.CharField(max_length=256)
    
    def __unicode__(self):
        return '%s %s' % (self.name, self.pk)
