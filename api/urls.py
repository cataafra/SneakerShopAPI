from django.urls import path, re_path
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

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('Sneaker/', SneakerList.as_view(), name='sneaker-list'),

    # models
    path('Sneaker/<int:pk>/', SneakerDetail.as_view(), name='sneaker-detail'),
    path('Garment/', GarmentList.as_view(), name='garment-list'),
    path('Garment/<int:pk>/', GarmentDetail.as_view(), name='garment-detail'),
    path('Brand/', BrandList.as_view(), name='brand-list'),
    path('Brand/<int:pk>/', BrandDetail.as_view(), name='brand-detail'),
    path('Customer/', CustomerList.as_view(), name='customer-list'),
    path('Customer/<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),
    path('Customer/<int:pk>/Garment/', CustomerGarmentsCreateDelete.as_view(), name='customer-garment'),
    path('Garment/<int:pk>/Customer/', GarmentsCustomerCreateDelete.as_view(), name='garment-customer'),

    # auth
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('activate/<uuid:confirmation_code>/', UserActivationView.as_view(), name='user-activate'),
    path('login/', TokenObtainPairView.as_view(), name='user-login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # user profile
    path('UserProfile/', UserProfileList.as_view(), name='profile_list'),
    path('UserProfile/<str:username>/', UserProfileDetail.as_view(), name='profile_detail'),
    path('UserProfile/<int:pk>/editrole/', UserRolesEditView.as_view(), name='edit-user-profile-role'),
    path('UserProfile/me/', CurrentUserView.as_view(), name='current_user'),
]
