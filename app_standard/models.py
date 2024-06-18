from django.db import models

# Create your models here.

class MinimumStandard(models.Model):
    number = models.IntegerField
    item_test = models.CharField(max_length=100)
    specification = models.TextField()
    type = models.CharField(max_length=1)
    thailand = models.BooleanField()
    usa_canada = models.BooleanField()
    malaysia =  models.BooleanField()
    indonisia = models.BooleanField()
    europe_PED = models.BooleanField()
    uae = models.BooleanField()
    japan = models.BooleanField()
    russia = models.BooleanField()
    france_NF414 = models.BooleanField()
    philippines = models.BooleanField()
    europe_Keymark = models.BooleanField()
    india_QCO = models.BooleanField()
    china = models.BooleanField() 

    def __str__(self) -> str:
        return '{} (id = {})'.format(self.number, self.id)



class ScopeStandard(models.Model):
    standard = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    scope = models.CharField(max_length=5000)



