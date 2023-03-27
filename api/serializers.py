from rest_framework import serializers
from django.db.models import Avg

from .models import *


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class SneakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sneaker
        fields = '__all__'


class SneakerSerializerAvgPrice(serializers.ModelSerializer):
    brand_avg_price = serializers.SerializerMethodField()

    class Meta:
        model = Sneaker
        fields = ['id', 'style', 'price', 'quantity', 'size', 'brand', 'brand_avg_price']


    def get_brand_avg_price(self, obj):
        return obj.brand.sneaker_set.aggregate(avg_price=Avg('price'))['avg_price']


class GarmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garment
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class BrandSerializerDetailed(serializers.ModelSerializer):
    sneakers = SneakerSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sneakers'] = SneakerSerializer(instance.sneaker_set.all(), many=True).data
        return representation


class BoughtGarmentsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = BoughtGarments
        fields = ["garment", "customer", "year", "review"]

    def create(self, validated_data):
        garment = validated_data.pop('garment')
        customer = validated_data.pop('customer')
        bought_garment = BoughtGarments.objects.create(garment=garment, customer=customer, **validated_data)
        return bought_garment


class SneakerSerializerDetailed(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Sneaker
        fields = (
            'style',
            'price',
            'quantity',
            'size',
            'brand')


class CustomerSerializerDetailed(serializers.ModelSerializer):
    bought_garments = BoughtGarmentsSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "name", "age", "date_added", "bought_garments"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['bought_garments'] = BoughtGarmentsSerializer(instance.boughtgarments_set.all(), many=True, fields=('garment', 'year', 'review')).data
        return representation


class GarmentSerializerDetailed(serializers.ModelSerializer):
    bought_by = BoughtGarmentsSerializer(many=True, read_only=True)
    avg_age = serializers.SerializerMethodField()

    class Meta:
        model = Garment
        fields = ['id', 'style', 'price', 'quantity', 'size', 'avg_age', 'bought_by']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["bought_by"] = BoughtGarmentsSerializer(instance.boughtgarments_set.all(), many=True).data
        return representation

    def get_avg_age(self, obj):
        avg_age = obj.boughtgarments_set.aggregate(Avg('customer__age'))['customer__age__avg']
        return avg_age if avg_age else 0


