# Import the necessary models
from django.utils import timezone
from datetime import datetime, timedelta
from random import randint
from models import *

# Create 10 Brands
brands = [
    Brand(name='Nike', country_of_origin='USA', founder='Phil Knight', motto='Just Do It'),
    Brand(name='Adidas', country_of_origin='Germany', founder='Adolf Dassler', motto='Impossible Is Nothing'),
    Brand(name='Supreme', country_of_origin='USA', founder='James Jebbia', motto='Supreme'),
    Brand(name='Off-White', country_of_origin='USA', founder='Virgil Abloh', motto='Off-White'),
    Brand(name='Bape', country_of_origin='Japan', founder='Nigo', motto='A Bathing Ape'),
    Brand(name='Palace', country_of_origin='UK', founder='Lev Tanju', motto='Palace Skateboards'),
    Brand(name='Yeezy', country_of_origin='USA', founder='Kanye West', motto='Yeezy'),
    Brand(name='Gucci', country_of_origin='Italy', founder='Guccio Gucci', motto='Gucci'),
    Brand(name='Puma', country_of_origin='Germany', founder='Rudolf Dassler', motto='Forever Faster'),
    Brand(name='Stone Island', country_of_origin='Italy', founder='Massimo Osti', motto='Stone Island')
]

# Save the Brands to the database
for brand in brands:
    brand.save()

# Create 10 Sneakers with relevant data and several brands
sneakers = [
    Sneaker(style='Air Force 1', price=100, quantity=15, brand=Brand.objects.get(name='Nike'), size=10),
    Sneaker(style='Air Max 90', price=120, quantity=10, brand=Brand.objects.get(name='Nike'), size=10),
    Sneaker(style='Air Max 95', price=130, quantity=11, brand=Brand.objects.get(name='Nike'), size=10),
    Sneaker(style='Air Max 97', price=140, quantity=12, brand=Brand.objects.get(name='Nike'), size=10),
    Sneaker(style='Air Max 270', price=150, quantity=10, brand=Brand.objects.get(name='Nike'), size=10),
    Sneaker(style='Stan Smith', price=100, quantity=10, brand=Brand.objects.get(name='Adidas'), size=10),
    Sneaker(style='Yeezy Boost 350', price=220, quantity=3, brand=Brand.objects.get(name='Adidas'), size=10),
    Sneaker(style='Yeezy Boost 700', price=230, quantity=7, brand=Brand.objects.get(name='Adidas'), size=10),
    Sneaker(style='Air Force 1', price=100, quantity=10, brand=Brand.objects.get(name='Supreme'), size=10),
    Sneaker(style='Air Force 1', price=100, quantity=10, brand=Brand.objects.get(name='Off-White'), size=10),
    Sneaker(style='Rihanna Creeper', price=200, quantity=10, brand=Brand.objects.get(name='Puma'), size=10),
    Sneaker(style='Rihanna Fenty', price=120, quantity=10, brand=Brand.objects.get(name='Puma'), size=10)
]

for sneaker in sneakers:
    sneaker.save()

# Create 10 Garments with relevant data and different styles
garments = [
    Garment(style='Red T-Shirt', price=20, quantity=10, size='S'),
    Garment(style='Black Oversized T-Shirt', price=20, quantity=10, size='M'),
    Garment(style='Multicolor T-Shirt', price=20, quantity=10, size='L'),
    Garment(style='Ripped T-Shirt', price=20, quantity=10, size='XL'),

    Garment(style='Hooded Sweatshirt', price=30, quantity=10, size='S'),
    Garment(style='Grey Heather Hoodie', price=30, quantity=10, size='M'),
    Garment(style='Black Hoodie', price=30, quantity=10, size='L'),

    Garment(style='Bomber Jacket', price=40, quantity=10, size='S'),
    Garment(style='Denim Jacket', price=40, quantity=10, size='M'),

    Garment(style='Jeans', price=50, quantity=10, size='S')
]

for garment in garments:
    garment.save()


# Create 10 Customers with relevant data and random names and ages
customers = [
    Customer(name='Jon Jones', age=random.randint(18, 60)),
    Customer(name='Jane Doe', age=random.randint(18, 60)),
    Customer(name='Bob Dylan', age=random.randint(18, 60)),
    Customer(name='Alice Wonderland', age=random.randint(18, 60)),
    Customer(name='Tom Brown', age=random.randint(18, 60)),
    Customer(name='John Doe', age=random.randint(18, 60)),
    Customer(name='Jane Smith', age=random.randint(18, 60)),
    Customer(name='Bob Marley', age=random.randint(18, 60)),
    Customer(name='Alice Cooper', age=random.randint(18, 60)),
    Customer(name='Tom Hanks', age=random.randint(18, 60))
]

for customer in customers:
    customer.save()

# Create 10 BoughtGarments with relevant data and random customers and items
entries = [
    BoughtGarments(customer=Customer.objects.get(name='Jon Jones'), garment=Garment.objects.get(style='Red T-Shirt'), year=2020, review='Great product!'),
    BoughtGarments(customer=Customer.objects.get(name='Jon Jones'), garment=Garment.objects.get(style='Black Oversized T-Shirt'), year=2021, review='Great product!'),
    BoughtGarments(customer=Customer.objects.get(name='Jon Jones'), garment=Garment.objects.get(style='Multicolor T-Shirt'), year=2020, review='Great product!'),

    BoughtGarments(customer=Customer.objects.get(name='Jane Doe'), garment=Garment.objects.get(style='Ripped T-Shirt'), year=2022, review='Not so great product!'),
    BoughtGarments(customer=Customer.objects.get(name='Jane Doe'), garment=Garment.objects.get(style='Hooded Sweatshirt'), year=2021, review='Great product!'),

    BoughtGarments(customer=Customer.objects.get(name='Bob Dylan'), garment=Garment.objects.get(style='Grey Heather Hoodie'), year=2020, review='Great product!'),

    BoughtGarments(customer=Customer.objects.get(name='Alice Wonderland'), garment=Garment.objects.get(style='Black Hoodie'), year=2020, review='Great product!'),
    BoughtGarments(customer=Customer.objects.get(name='Alice Wonderland'), garment=Garment.objects.get(style='Bomber Jacket'), year=2021, review='Great product!'),

    BoughtGarments(customer=Customer.objects.get(name='Tom Brown'), garment=Garment.objects.get(style='Denim Jacket'), year=2020, review='Insane quality!'),
    BoughtGarments(customer=Customer.objects.get(name='Tom Brown'), garment=Garment.objects.get(style='Jeans'), year=2021, review='Great product!')
]

for entry in entries:
    entry.save()









