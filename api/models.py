import random
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country_of_origin = models.CharField(max_length=100)
    founder = models.CharField(max_length=100)
    motto = models.CharField(max_length=100)

    date_added = models.DateField(auto_now_add=True)


class Sneaker(models.Model):
    style = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    size = models.PositiveIntegerField()

    date_added = models.DateField(auto_now_add=True)

    def __gt__(self, other):
        return self.price > self.other


class Garment(models.Model):
    style = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=15)

    date_added = models.DateField(auto_now_add=True)


class Customer(models.Model):
    name = models.CharField(max_length=25)
    age = models.PositiveIntegerField()
    date_added = models.DateField(auto_now_add=True)
    garments_bought = models.ManyToManyField(Garment, through='BoughtGarments')


class BoughtGarments(models.Model):
    garment = models.ForeignKey(Garment, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    year = models.PositiveIntegerField()
    review = models.CharField(max_length=255)

    class Meta:
        unique_together = [['garment', 'customer']]
        ordering = ['customer']

