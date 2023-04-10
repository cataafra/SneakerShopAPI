from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Sneaker Shop API",
      default_version='v1',
      description="Test description",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
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
