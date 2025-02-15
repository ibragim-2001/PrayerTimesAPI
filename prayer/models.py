from django.db import models

class Country(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Region(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='regions')
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class City(models.Model):
    id = models.BigAutoField(primary_key=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name