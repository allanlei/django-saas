from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

class Pizza(models.Model):
    name = models.CharField(max_length=128, unique=True)
    toppings = models.ManyToManyField(Topping)

    def __unicode__(self):
        return self.name
