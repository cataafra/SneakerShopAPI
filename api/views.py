from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework_swagger.views import get_swagger_view
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from datetime import timedelta, timezone
from django.utils import timezone
import uuid

from .serializers import *
from .permissions import *
from .pagination import CustomPagination

schema_view = get_swagger_view(title='Pastebin API')


# Create your views here.
class BrandList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BrandSerializer
    queryset = Brand.objects.all().order_by('id')
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]

    serializer_class = BrandSerializerDetailed
    queryset = Brand.objects.all()


class SneakerList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.query_params.get('brand-avg-price'):
            return SneakerSerializerAvgPrice
        return SneakerSerializer

    def get_queryset(self):
        queryset = Sneaker.objects.all().order_by('id')
        brand = self.request.query_params.get('brand')
        price = self.request.query_params.get('min-price')
        order_by_avg_price_per_brand = self.request.query_params.get('brand-avg-price')

        if brand:
            queryset = queryset.filter(brand=brand)
        if price:
            queryset = queryset.filter(price__gte=price)
        if order_by_avg_price_per_brand:
            queryset = queryset.annotate(avg_price=Avg('brand__sneaker__price')).order_by('-avg_price', 'brand')

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SneakerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = SneakerSerializerDetailed
    queryset = Sneaker.objects.all()


class GarmentList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Garment.objects.all().order_by('id')
    serializer_class = GarmentSerializer
    pagination_class = CustomPagination


class GarmentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = GarmentSerializerDetailed
    queryset = Garment.objects.all()

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Garment.objects.filter(id=pk)
        return queryset.annotate(avg_age=Avg('boughtgarments__customer__age'))


class CustomerList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all().order_by('id')
    pagination_class = CustomPagination


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CustomerSerializerDetailed
    queryset = Customer.objects.all()


class CustomerGarmentsCreateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BoughtGarmentsSerializer
    queryset = BoughtGarments.objects.all()

    def put(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        garment = Garment.objects.get(pk=request.data['garment'])

        # update if already exists
        try:
            bought_garment = BoughtGarments.objects.get(customer=customer, garment=garment)
            bought_garment.year = request.data['year']
            bought_garment.review = request.data['review']
            bought_garment.save()
            return Response(status=status.HTTP_200_OK)
        except BoughtGarments.DoesNotExist:
            # create if not exists
            new_bought_garment = BoughtGarments.objects.create(customer=customer, garment=garment,
                                                               year=request.data['year'], review=request.data['review'])
            new_bought_garment.save()
            return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk, *args, **kwargs):
        customer = Customer.objects.get(pk=pk)
        garment = Garment.objects.get(pk=request.data['garment'])
        bought_garment = BoughtGarments.objects.get(customer=customer, garment=garment)
        bought_garment.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


class GarmentsCustomerCreateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BoughtGarmentsSerializer
    queryset = BoughtGarments.objects.all()

    def put(self, request, pk):
        garment = Garment.objects.get(pk=pk)
        customer = Customer.objects.get(pk=request.data['customer'])

        try:
            # update if already exists
            bought_garment = BoughtGarments.objects.get(customer=customer, garment=garment)
            bought_garment.year = request.data['year']
            bought_garment.review = request.data['review']
            bought_garment.save()
            return Response(status=status.HTTP_200_OK)
        except BoughtGarments.DoesNotExist:
            # create if not exists
            new_bought_garment = BoughtGarments.objects.create(customer=customer, garment=garment,
                                                               year=request.data['year'], review=request.data['review'])
            new_bought_garment.save()
            return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk, *args, **kwargs):
        garment = Garment.objects.get(pk=pk)
        customer = Customer.objects.get(pk=request.data['customer'])
        bought_garment = BoughtGarments.objects.get(customer=customer, garment=garment)
        bought_garment.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


# authentication
class UserProfileList(generics.ListCreateAPIView):
    permissions_classes = [IsAdminUser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsOwnerOrReadOnly]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        username = self.kwargs.get("username")
        obj = UserProfile.objects.filter(user_id=username)[0]
        return obj

class UserRegistrationView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        activation_expiry_date = timezone.now() + timedelta(minutes=10)
        activation_code = str(uuid.uuid4())
        data = request.data.copy()
        data["activation_code"] = activation_code
        data["activation_expiry_date"] = activation_expiry_date
        data["active"] = False

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"activation_code": activation_code}, status=status.HTTP_201_CREATED, headers=headers)

class UserActivationView(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, confirmation_code):
        try:
            user_profile = UserProfile.objects.get(activation_code=confirmation_code)
        except UserProfile.DoesNotExist:
            return Response({"error": "Activation code not found"}, status=status.HTTP_400_BAD_REQUEST)

        if user_profile.activation_expiry_date < timezone.now():
            return Response({"error": "Activation code expired"}, status=status.HTTP_400_BAD_REQUEST)

        if user_profile.user.is_active:
            return Response({"success": "Account already active"}, status=status.HTTP_200_OK)

        user_profile.user.is_active = True
        user_profile.user.save()

        user_profile.active = True
        user_profile.save()

        return Response({"success": "User profile activated"}, status=status.HTTP_200_OK)

# user roles
class UserRolesEditView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = UserProfile.objects.all()
    serializer_class = UserRoleUpdateSerializer

class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data)

