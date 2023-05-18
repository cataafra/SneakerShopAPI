from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", to_field="username"
    )
    bio = models.TextField(max_length=50, default="No bio.")
    location = models.CharField(max_length=50, default="No location.")
    gender = models.CharField(max_length=10, choices=(("m", "Male"), ("f", "Female"), ("o", "Other")), default="o")
    marital_status = models.CharField(max_length=20, choices=(("s", "Single"), ("m", "Married")), default="s")

    activation_code = models.CharField(max_length=36, null=True)
    activation_expiry_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=30))
    active = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=(
        ("regular", "Regular"), ("moderator", "Moderator"), ("admin", "Admin")),
                            default="regular")
    page_size = models.IntegerField(choices=((12, 12), (36, 36), (60, 60), (120, 120)), default=12)

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country_of_origin = models.CharField(max_length=100)
    founder = models.CharField(max_length=100)
    motto = models.CharField(max_length=100)

    date_added = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)


class Sneaker(models.Model):
    style = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    size = models.PositiveIntegerField()

    date_added = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)

    def __gt__(self, other):
        return self.price > other.price


class Garment(models.Model):
    style = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=15)

    date_added = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)


class Customer(models.Model):
    name = models.CharField(max_length=25)
    age = models.PositiveIntegerField()
    date_added = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    garments_bought = models.ManyToManyField(Garment, through='BoughtGarments')


class BoughtGarments(models.Model):
    garment = models.ForeignKey(Garment, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    year = models.PositiveIntegerField()
    review = models.CharField(max_length=255)

    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = [['garment', 'customer']]
        ordering = ['customer']



