from django.db.models import Avg

from rest_framework import serializers

from .models import *
from django.contrib.auth.models import User

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class SneakerSerializer(serializers.ModelSerializer):
    brand_name = BrandSerializer(read_only=True)

    class Meta:
        model = Sneaker
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['brand_name'] = BrandSerializer(instance.brand).data["name"]
        return representation


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ("user", "bio", "location", "gender", "marital_status", "role", "active", "activation_code", "activation_expiry_date")
        extra_kwargs = {"role": {"read_only": True}, "user.password": {"write_only": True}, "activation_code": {"required": False}, "activation_expiry_date": {"required": False}}

    def to_internal_value(self, data):
        user_data = {
            'username': data.pop('username'),
            'password': data.pop('password')
        }
        data['user'] = user_data
        return super().to_internal_value(data)

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, is_active=False)
        validated_data['user'] = user
        return super().create(validated_data)



class UserActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['activation_code']


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["role"]

    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance

