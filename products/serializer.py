from django.db import models # type: ignore
from django.utils.translation import gettext_lazy as _ # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from rest_framework import serializers # type: ignore
from .models import Product, ProductCategory, ProductImage


User = get_user_model()

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

