from rest_framework.generics import CreateAPIView, ListAPIView
from .models import CartListProducts, Cart
from .serializers import CartListProductsSerializer, CartRetrieveSerializer
from .permissions import IsCartOwner
from django.shortcuts import get_object_or_404


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPaginationCartRetrieve(PageNumberPagination):
    def get_paginated_response(self, data):
        cart_id = self.request.path.split("/")[3]
        total_value_cart = 0
        for product in data:
            total_value_cart += product["total_product"]
        return Response(
            {"id": cart_id, "total_value_cart": total_value_cart, "cart_list": data}
        )


class CartListProductsView(CreateAPIView):
    permission_classes = [IsCartOwner]
    queryset = CartListProducts.objects.all()
    serializer_class = CartListProductsSerializer

    def perform_create(self, serializer):
        return serializer.save(
            cart_id=self.kwargs.get("cart_id"),
            product_id=self.request.data["product_id"],
        )


# class CartRetrieve(ListAPIView):
#     permission_classes = [IsCartOwner]
#     serializer_class = CartRetrieveSerializer
#     pagination_class = CustomPaginationCartRetrieve

#     def get_queryset(self):
#         cart_id = self.kwargs.get("cart_id")
#         cart = get_object_or_404(Cart, pk=cart_id)
#         return Cart.objects.filter(pk=cart_id)


class CartRetrieve(ListAPIView):
    permission_classes = [IsCartOwner]
    serializer_class = CartRetrieveSerializer
    pagination_class = CustomPaginationCartRetrieve

    def get_queryset(self):
        cart_id = self.kwargs.get("cart_id")
        cart = get_object_or_404(Cart, pk=cart_id)
        return CartListProducts.objects.filter(cart_id=cart_id).select_related(
            "product"
        )
