from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from carts.models import Cart
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from addresses.serializers import AddressSerializer


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that username already exists.",
            )
        ],
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    cpf = serializers.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$",
                message="Invalid CPF. Use the format XXX.XXX.XXX-XX.",
                code="invalid_cpf",
            ),
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that cpf already exists.",
            ),
        ],
    )

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        validators=[
            RegexValidator(
                regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",
                message="The password must  including at least one uppercase letter, one lowercase letter, one number.",
                code="invalid_password",
            )
        ],
    )

    cart_id = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "password",
            "email",
            "cpf",
            "bio",
            "birthdate",
            "is_superuser",
            "is_seller",
            "is_client",
            "created_at",
            "updated_at",
            "cart_id",
            "address",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "cart_id", "address"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    @extend_schema_field(OpenApiTypes.UUID)
    def get_cart_id(self, validated_data):
        return validated_data.cart.id

    @extend_schema_field(AddressSerializer or None)
    def get_address(self, validated_data):
        try:
            address_dict = validated_data.address.__dict__
            find_address = AddressSerializer(data=address_dict)
            find_address.is_valid(raise_exception=True)
            response = find_address.data
            response["address_id"] = address_dict["id"]
            return response
        except Exception:
            return None

    def create(self, validated_data: dict) -> User:
        is_superuser = validated_data.pop("is_superuser", None)

        if is_superuser:
            validated_data["is_seller"] = False
            validated_data["is_client"] = False
            new_superuser = User.objects.create_superuser(**validated_data)
            new_cart = Cart.objects.create(user=new_superuser)
            return new_superuser

        new_user = User.objects.create_user(**validated_data)
        new_cart = Cart.objects.create(user=new_user)
        return new_user

    def update(self, instance: User, validated_data: dict) -> User:
        ignore_keys = ["password", "username", "cpf", "is_superuser"]
        for key, value in validated_data.items():
            if not ignore_keys.__contains__(key):
                setattr(instance, key, value)

        if validated_data.get("password"):
            instance.set_password(validated_data["password"])

        instance.save()

        return instance


class CustomJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_superuser"] = user.is_superuser
        token["is_seller"] = user.is_seller
        token["is_client"] = user.is_client

        return token
