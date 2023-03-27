from django.db.models import Avg
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch, MagicMock
from .models import Garment, Customer, BoughtGarments, Sneaker, Brand
from .serializers import GarmentSerializer


class GarmentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.garment1 = Garment.objects.create(
            style='T-Shirt',
            price=15.99,
            quantity=100,
            size='M'
        )
        self.garment2 = Garment.objects.create(
            style='Jeans',
            price=49.99,
            quantity=50,
            size='L'
        )
        self.customer1 = Customer.objects.create(
            name='John',
            age=30
        )
        self.customer2 = Customer.objects.create(
            name='Jane',
            age=20
        )
        self.bought_garment1 = BoughtGarments.objects.create(
            garment=self.garment1,
            customer=self.customer1,
            year=2021,
            review='Great shirt'
        )
        self.bought_garment2 = BoughtGarments.objects.create(
            garment=self.garment1,
            customer=self.customer2,
            year=2022,
            review='Good fit'
        )

    def test_get_garment_average_age(self):
        response = self.client.get(reverse('garment-detail', args=[self.garment1.id]) + '?avg_age')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['avg_age'], 25)


# unit test for the get_brand_avg_price function in the Sneaker model
class SneakerTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.brand1 = Brand.objects.create(
            name='Nike',
            country_of_origin='USA',
            founder='Bill Bowerman',
            motto='Just do it'
        )
        self.brand2 = Brand.objects.create(
            name='Adidas',
            country_of_origin='Germany',
            founder='Adolf Dassler',
            motto='Impossible is nothing'
        )
        self.sneaker1 = Sneaker.objects.create(
            style='Air Jordan 1',
            price=200,
            quantity=50,
            size=10,
            brand=self.brand1
        )
        self.sneaker2 = Sneaker.objects.create(
            style='Yeezy Boost 350',
            price=300,
            quantity=50,
            size=10,
            brand=self.brand2
        )
        self.sneaker3 = Sneaker.objects.create(
            style='Stan Smith',
            price=200,
            quantity=50,
            size=10,
            brand=self.brand2
        )

    def test_get_sneaker_brand_avg_price(self):
        response = self.client.get(reverse('sneaker-list') + '?brand-avg-price=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0]['brand_avg_price'], 250)
        self.assertEqual(response.data[1]['brand_avg_price'], 250)
        self.assertEqual(response.data[2]['brand_avg_price'], 200)
