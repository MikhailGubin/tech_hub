from rest_framework import serializers

from electronics.models import NetworkNode
from django.core.validators import MinValueValidator
from electronics.validators import ProductValidator, SupplierNetworkNodeValidator


class ContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели "Контакт".
    """

    class Meta:
        model = NetworkNode

        fields = [
            "id",
            "email",
            "country",
            "city",
            "street",
            "house_number",
        ]


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели "Продукт" с кастомным валидатором.
    """

    class Meta:
        model = NetworkNode

        fields = [
            "id",
            "name",
            "model",
            "release_date",
        ]
        validators = [
            ProductValidator(field="release_date"),
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
        read_only_fields = ["created_at", "debt",]
        validators = [
            MinValueValidator(0, message='Задолженность не может быть отрицательной.', field="debt")
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["supplier"].validators.append(
            SupplierNetworkNodeValidator(
            field="supplier",
            instance=self.instance
        )
        )