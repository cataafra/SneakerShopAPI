import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country_of_origin = models.CharField(max_length=100)
    founder = models.CharField(max_length=100)
    motto = models.CharField(max_length=100)

    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

class Sneaker(models.Model):
    style = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    size = models.PositiveIntegerField()

    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __gt__(self, other):
        return self.price > self.other

class Garment(models.Model):
    style = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=15)

    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

class Customer(models.Model):
    name = models.CharField(max_length=25)
    age = models.PositiveIntegerField()
    date_added = models.DateField(auto_now_add=True)
    garments_bought = models.ManyToManyField(Garment, through='BoughtGarments')

    user = models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE)

class BoughtGarments(models.Model):
    garment = models.ForeignKey(Garment, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    year = models.PositiveIntegerField()
    review = models.CharField(max_length=255)

    class Meta:
        unique_together = [['garment', 'customer']]
        ordering = ['customer']

