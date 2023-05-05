from rest_framework import serializers
from carts.models import CartListProducts
from .models import PurchaseOrders


class ProductCartSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    brand = serializers.CharField()
    seller_id = serializers.UUIDField()


class PurchaseOrdersSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrders
        fields = ["id", "price", "quantity_items", "user_id", "seller_id", "orders"]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "price",
            "quantity_items",
            "orders",
        ]

    def get_orders(self, validated_data):
        list_orders = validated_data[0]
        list_cart_products = validated_data[1]

        orders = []
        for order in list_orders:
            list_product_order = [product for product in order.products.values()]
            list_product_order_serializer = ProductCartSerializer(
                data=list_product_order, many=True
            )
            list_product_order_serializer.is_valid(raise_exception=True)

            for product in list_product_order_serializer.data:
                for item in list_cart_products:
                    if str(product["id"]) == str(item.product.id):
                        product["quantity_product"] = item.quantity

            orders.append(
                {
                    "id": order.id,
                    "status": order.status,
                    "price": order.price,
                    "quantity_items": order.quantity_items,
                    "user_id": order.user.id,
                    "seller_id": order.seller.id,
                    "created_at": order.created_at,
                    "updated_at": order.updated_at,
                    "products": list_product_order_serializer.data,
                }
            )
        return orders

    def create(self, validated_data):
        cart_id = validated_data.pop("cart_id")

        cart_list = CartListProducts.objects.filter(cart_id=cart_id).select_related(
            "product"
        )

        if cart_list.count() == 0:
            raise serializers.ValidationError(
                {"message": "Sorry, your shopping cart is empty!"}
            )

        for item in cart_list:
            if item.product.is_available_for_sale is False:
                raise serializers.ValidationError(
                    {
                        "message": f"Sorry, the product {item.product.name} is not available!"
                    }
                )
            if item.quantity > item.product.quantity_stock:
                raise serializers.ValidationError(
                    {
                        "message": f"Sorry, the product {item.product.name} is not available!"
                    }
                )

        for item in cart_list:
            new_product_stock = item.product.quantity_stock - item.quantity
            item.product.quantity_stock = new_product_stock

            if new_product_stock == 0:
                item.product.is_available_for_sale = False
            item.product.save()

        seller_id_list = []
        for item in cart_list:
            if item.product.seller not in seller_id_list:
                seller_id_list.append(item.product.seller)

        order_list = []
        for seller in seller_id_list:
            validated_data["seller"] = seller
            price = 0
            quantity = 0
            for item in cart_list:
                if item.product.seller == seller:
                    price += item.quantity * item.product.price
                    quantity += item.quantity
            validated_data["quantity_items"] = quantity
            validated_data["price"] = price
            order = PurchaseOrders.objects.create(**validated_data)
            order_list.append(order)

        for item in cart_list:
            for order in order_list:
                if order.seller == item.product.seller:
                    order.products.add(item.product)

        cart_list.delete()
        return [order_list, cart_list]
