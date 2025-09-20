from django.db import models


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
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Сетевое звено"
        verbose_name_plural = "Сетевые звенья"

    def __str__(self):
        return f"{self.get_node_type_display()}: {self.name}"

    @property
    def level(self):
        """Вычисляет уровень иерархии"""
        if self.supplier is None:
            return 0
        return self.supplier.level + 1
