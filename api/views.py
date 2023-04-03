from rest_framework import generics, status
from rest_framework.response import Response

from .models import *
from .serializers import *


# Create your views here.
class BrandList(generics.ListCreateAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BrandSerializerDetailed
    queryset = Brand.objects.all()


class SneakerList(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.query_params.get('brand-avg-price'):
            return SneakerSerializerAvgPrice
        return SneakerSerializer

    def get_queryset(self):
        queryset = Sneaker.objects.all()
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


class SneakerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SneakerSerializerDetailed
    queryset = Sneaker.objects.all()


class GarmentList(generics.ListCreateAPIView):
    queryset = Garment.objects.all()
    serializer_class = GarmentSerializer


class GarmentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GarmentSerializerDetailed
    queryset = Garment.objects.all()

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Garment.objects.filter(id=pk)
        return queryset.annotate(avg_age=Avg('boughtgarments__customer__age'))


class CustomerList(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializerDetailed
    queryset = Customer.objects.all()


class CustomerGarmentsCreateDelete(generics.RetrieveUpdateDestroyAPIView):
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











