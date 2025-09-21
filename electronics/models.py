from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.serializers import ValidationError
from django.utils import timezone


class Contact(models.Model):
    """Модель 'Контакт'"""

    email = models.EmailField(
        verbose_name="Email",
        help_text="Укажите почту",
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Страна",
        help_text="Укажите страну",
        blank=True,
        default="",
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        help_text="Укажите город",
        blank=True,
        default="",
    )
    street = models.CharField(
        max_length=100,
        verbose_name="Улица",
        help_text="Укажите улицу",
        blank=True,
        default="",
    )
    house_number = models.CharField(
        max_length=10,
        verbose_name="Номер дома",
        help_text="Укажите номер дома",
        blank=True,
        default="",
    )

    def clean(self):
        """ Проверяет связи между городом, улицей и номером дома """
        super().clean()
        if self.street and not self.city:
            raise ValidationError({'city': 'Если указана улица, необходимо указать и город.'})
        if self.house_number and not self.city:
            raise ValidationError({'city': 'Если указан номер дома, необходимо указать и город.'})
        if self.house_number and not self.street:
            raise ValidationError({'street': 'Если указан номер дома, необходимо указать и улицу.'})

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"Контакт: {self.email}, {self.country}, {self.city}"


class Product(models.Model):
    """Модель 'Продукт'"""

    name = models.CharField(
        max_length=100,
        verbose_name="Название",
        help_text="Укажите название продукта",
    )
    model = models.CharField(
        max_length=100,
        verbose_name="Модель",
        help_text="Укажите модель",
        blank=True,
        default="",
    )
    release_date = models.DateField(
        verbose_name="Дата выхода на рынок",
        help_text="Укажите дату выхода на рынок",
        blank=True,
        null=True,
    )

    def clean(self):
        super().clean()
        if self.release_date:
            if self.release_date > timezone.now().date():
                raise ValidationError({'release_date': 'Дата выхода продукта не может быть в будущем.'})

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"Продукт: {self.name} {self.model}"


class NetworkNode(models.Model):
    """Модель 'Сетевого звена'"""

    class NodeType(models.IntegerChoices):
        FACTORY = 0, "Завод"
        RETAIL = 1, "Розничная сеть"
        ENTREPRENEUR = 2, "Индивидуальный предприниматель"

    name = models.CharField(max_length=100, verbose_name="Название")
    node_type = models.IntegerField(
        choices=NodeType.choices,
        verbose_name="Уровень звена",
        help_text="Укажите уровень звена в иерархии сети",
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        verbose_name="Контакты",
        help_text="Укажите контакты сетевого звена",
    )
    products = models.ManyToManyField(
        Product,
        verbose_name="Продукты",
        help_text="Укажите продукты",
    )
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Поставщик",
        help_text="Укажите поставщика",
    )
    debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name="Задолженность перед поставщиком",
        help_text="Укажите задолженность перед поставщиком",
        validators=[
            # Задолженность не может быть отрицательной
            MinValueValidator(0, message='Задолженность не может быть отрицательной.')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def clean(self):
        super().clean()

        if self.node_type == self.NodeType.FACTORY and self.supplier is not None:
            raise ValidationError(
                {'supplier': 'Завод не может иметь поставщика.'}
            )

        if self.supplier == self:
            raise ValidationError({'supplier': 'Объект не может быть поставщиком для самого себя.'})

        if self.supplier is not None:
            if (self.node_type == self.NodeType.FACTORY and
                    self.supplier.node_type == self.NodeType.ENTREPRENEUR):
                raise ValidationError(
                    {'supplier': 'У розничной сети не может быть поставщиком индивидуальный предприниматель.'}
                )

    class Meta:
        verbose_name = "Сетевое звено"
        verbose_name_plural = "Сетевые звенья"

    def __str__(self):
        return f"{self.get_node_type_display()}: {self.name}"

