from django.db import models

class TestModel1(models.Model):
    value = models.CharField(max_length=256)
    
    def __unicode__(self):
        return '%s pk=%s' % (self.value, self.pk)


class TestModel2(models.Model):
    value = models.CharField(max_length=256)
    
    def __unicode__(self):
        return '%s pk=%s' % (self.value, self.pk)

class TestModel3(models.Model):
    value = models.CharField(max_length=256, unique=True)
    
    def __unicode__(self):
        return '%s pk=%s' % (self.value, self.pk)
