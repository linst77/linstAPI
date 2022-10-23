from rest_framework import serializers
from .models import VerifyType, ProductType, NationType, StoreType, Category, EntryType


class EntryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryType
        fields = "__all__"

class VerifyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyType
        fields = "__all__"

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"

class NationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationType
        fields = "__all__"

class StoreTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreType
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
