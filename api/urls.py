from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('Sneaker/', SneakerList.as_view(), name='sneaker-list'),
    path('Sneaker/<int:pk>/', SneakerDetail.as_view(), name='sneaker-detail'),
    path('Garment/', GarmentList.as_view(), name='garment-list'),
    path('Garment/<int:pk>/', GarmentDetail.as_view(), name='garment-detail'),
    path('Brand/', BrandList.as_view(), name='brand-list'),
    path('Brand/<int:pk>/', BrandDetail.as_view(), name='brand-detail'),
    path('Customer/', CustomerList.as_view(), name='customer-list'),
    path('Customer/<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),
    path('Customer/<int:pk>/Garment/', CustomerGarmentsCreateDelete.as_view(), name='customer-garment'),
    path('Garment/<int:pk>/Customer/', GarmentsCustomerCreateDelete.as_view(), name='garment-customer')
]
