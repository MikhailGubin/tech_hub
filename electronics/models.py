from django.core.validators import MinValueValidator
from django.db import models, transaction
from rest_framework.serializers import ValidationError


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

    def clean(self):
        super().clean()
        # Пример: если указана улица, но не указан город - это ошибка
        if self.street and not self.city:
            raise ValidationError({'city': 'Если указана улица, необходимо указать и город.'})
        if self.house_number and not self.city:
            raise ValidationError({'city': 'Если указан номер дома, необходимо указать и город.'})
        if self.house_number and not self.street:
            raise ValidationError({'street': 'Если указан номер дома, необходимо указать и улицу.'})


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
        validators=[
            # Задолженность не может быть отрицательной
            MinValueValidator(0, message='Задолженность не может быть отрицательной.')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Сетевое звено"
        verbose_name_plural = "Сетевые звенья"

    def save(self, *args, **kwargs):
        # Флаг, указывающий, что нужно обновить потомков
        update_children = False
        old_level = None

        # Если объект уже существует в БД, получим его старую версию
        if self.pk:
            old_obj = NetworkNode.objects.get(pk=self.pk)
            old_supplier = old_obj.supplier
            old_level = old_obj.level

            # Проверяем, изменился ли поставщик (а значит, может измениться и уровень)
            if self.supplier != old_supplier:
                update_children = True

        # Вычисляем новый уровень
        if self.supplier is None:
            self.level = 0
        else:
            # Важно: у поставщика уровень уже должен быть вычислен и сохранен!
            self.level = self.supplier.level + 1

        # Сохраняем объект
        super().save(*args, **kwargs)

        # Если изменился поставщик и уровень, то обновляем информацию у потомков
        if update_children and (old_level is not None and self.level != old_level):
            self.update_children_levels()

    def update_children_levels(self):
        """Рекурсивно обновляет уровни всех дочерних элементов."""
        # Используем транзакцию для целостности данных
        with transaction.atomic():
            children = self.children.all()
            for child in children:
                # Пересчитываем уровень для каждого потомка
                child.level = self.level + 1
                child.save()  # Важно: save() потомка также вызовет обновление его детей
                # Рекурсивный вызов происходит автоматически благодаря методу save()

    def __str__(self):
        return f"{self.get_node_type_display()}: {self.name}"
