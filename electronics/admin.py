from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from electronics.models import Contact, NetworkNode, Product


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """Панель администратора для модели "Сетевое звено"."""

    list_display = ["name", "node_type", "get_supplier_link", "debt", "created_at"]
    list_filter = ["contact__city", "node_type"]  # Фильтр по городу
    actions = ["clear_debt"]

    # Поле только для чтения в админке
    readonly_fields = ("created_at",)

    def get_supplier_link(self, obj):
        """Создаёт ссылку на поставщика"""
        if obj.supplier:
            url = reverse("admin:electronics_networknode_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "Нет поставщика"

    get_supplier_link.short_description = "Поставщик"

    def clear_debt(self, request, queryset):
        """Обнуляет задолженность перед поставщиком"""
        updated_count = queryset.update(debt=0.00)
        self.message_user(request, f"Задолженность очищена для {updated_count} объектов.")

    clear_debt.short_description = "Очистить задолженность перед поставщиком"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Панель администратора для модели "Контакт"."""

    list_display = ["email", "country", "city", "street", "house_number"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Панель администратора для модели "Продукт"."""

    list_display = ["name", "model", "release_date"]
