from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity_stock",
            "is_available_for_sale",
            "brand",
            "category"
        ]
        read_only_fields = ["id","created_at","updated_at"]
    
    def create(self, validated_data):
        return Product.objects.create(**validated_data)
