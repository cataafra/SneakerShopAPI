from django.db import models
from django.contrib.auth.models import User


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
        return self.price > other.price


class Garment(models.Model):
    style = models.CharField(max_length=100)
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


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", to_field="username"
    )
    bio = models.TextField(max_length=500)
    location = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=(("m", "Male"), ("f", "Female"), ("o", "Other")))
    marital = models.CharField(max_length=20, choices=(("s", "Single"), ("m", "Married")))
    activation_code = models.CharField(max_length=36, default="123")
    activation_expiry_date = models.DateTimeField()
    active = models.BooleanField()
    role = models.CharField(max_length=10, choices=(
        ("regular", "Regular"), ("moderator", "Moderator"), ("admin", "Admin")),
                            default="regular")
    page_size = models.IntegerField(choices=((25, 25), (50, 50), (100, 100)), default=100, )

    def __str__(self):
        return self.user.username

