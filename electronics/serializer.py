from rest_framework import serializers

from electronics.models import NetworkNode, Contact, Product
from django.core.validators import MinValueValidator
from electronics.validators import ReleaseDateProductValidator, SupplierNetworkNodeValidator, AddressContactValidator


class ContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели "Контакт" с кастомным валидатором.
    """

    class Meta:
        model = Contact

        fields = [
            "id",
            "email",
            "country",
            "city",
            "street",
            "house_number",
        ]

    def validate(self, attrs):
        """Вызываем валидатор, который проверяет связи между городом, улицей и номером дома"""
        attrs = super().validate(attrs)
        validator = AddressContactValidator()
        return validator(attrs)


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели "Продукт" с кастомным валидатором.
    """

    class Meta:
        model = Product

        fields = [
            "id",
            "name",
            "model",
            "release_date",
        ]
        validators = [
            ReleaseDateProductValidator(field="release_date"),
        ]


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели "Сетевое звено" с кастомными валидаторами.
    """

    class Meta:
        model = NetworkNode

        fields = [
            "id",
            "name",
            "node_type",
            "contact",
            "products",
            "supplier",
            "debt",
            "created_at",
        ]
        read_only_fields = ["created_at",]
        extra_kwargs = {
            'debt': {
                'validators': [MinValueValidator(0)]
            }
        }

    def validate(self, attrs):
        """Валидация условий для поставщика"""

        attrs = super().validate(attrs)
        validator = SupplierNetworkNodeValidator(instance=self.instance)
        return validator(attrs)


class NetworkNodeUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели "Сетевое звено" с кастомными валидаторами.
    """

    class Meta:
        model = NetworkNode

        fields = [
            "id",
            "name",
            "node_type",
            "contact",
            "products",
            "supplier",
            "debt",
            "created_at",
        ]
        read_only_fields = ["created_at", "debt",]


    def validate(self, attrs):
        """Валидация условий для поставщика"""

        attrs = super().validate(attrs)
        validator = SupplierNetworkNodeValidator(instance=self.instance)
        return validator(attrs)
