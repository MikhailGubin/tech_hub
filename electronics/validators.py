from django.utils import timezone
from rest_framework.serializers import ValidationError

from electronics.models import NetworkNode


class AddressContactValidator:
    """Проверяет связи между городом, улицей и номером дома"""

    def __call__(self, attrs):

        city = attrs.get('city', '')
        street = attrs.get('street', '')
        house_number = attrs.get('house_number', '')

        errors = {}

        if street and not city:
            errors['city'] = 'Если указана улица, необходимо указать и город.'

        if house_number and not city:
            errors['city'] = 'Если указан номер дома, необходимо указать и город.'

        if house_number and not street:
            errors['street'] = 'Если указан номер дома, необходимо указать и улицу.'

        if errors:
            raise ValidationError(errors)

        return attrs


class ReleaseDateProductValidator:
    """Проверяет, что продукт не может выйти на рынок в будущем"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        release_date = dict(value).get(self.field)
        if release_date > timezone.now().date():
            raise ValidationError(
                {"release_date": "Дата выхода продукта на рынок не может быть в будущем."}
            )


class SupplierNetworkNodeValidator:
    """ Настраивает правильные условия для поля 'Поставщик' """

    def __init__(self, instance=None):
        self.instance = instance

    def __call__(self, attrs):
        node_type = attrs.get('node_type')
        supplier = attrs.get('supplier')


        if self.instance is None:
            self._validate_create(attrs, node_type, supplier)
        else:
            self._validate_update(attrs, node_type, supplier)

        return attrs

    def _validate_create(self, attrs, node_type, supplier):
        """Валидация при создании"""
        if supplier is None and node_type != NetworkNode.NodeType.FACTORY:
            raise ValidationError({
                'supplier': 'Объект без поставщика может быть только Заводом.'
            })

        if supplier is not None and node_type is not None:
            self._validate_supplier_hierarchy(supplier, node_type)

    def _validate_update(self, attrs, node_type, supplier):
        """Валидация при обновлении"""
        # Если оба поля не переданы - ничего не проверяем
        if node_type is None and supplier is None:
            return

        # Определяем текущие значения
        current_node_type = node_type if node_type is not None else self.instance.node_type
        current_supplier = supplier if supplier is not None else self.instance.supplier

        # Проверяем только если оба значения известны
        if current_supplier is None and current_node_type != NetworkNode.NodeType.FACTORY:
            raise ValidationError({
                'supplier': 'Объект без поставщика может быть только Заводом.'
            })

        if current_supplier is not None:
            self._validate_supplier_hierarchy(current_supplier, current_node_type)

    def _validate_supplier_hierarchy(self, supplier, node_type):
        """Общие проверки иерархии"""
        if isinstance(supplier, int):
            supplier_obj = NetworkNode.objects.get(id=supplier)
        else:
            supplier_obj = supplier

        if node_type == NetworkNode.NodeType.FACTORY:
            raise ValidationError({'supplier': 'Завод не может иметь поставщика.'})

        if self.instance and supplier_obj.id == self.instance.id:
            raise ValidationError({'supplier': 'Объект не может быть поставщиком для самого себя.'})

        if node_type == NetworkNode.NodeType.RETAIL and supplier_obj.node_type == NetworkNode.NodeType.ENTREPRENEUR:
            raise ValidationError({
                'supplier': 'У розничной сети не может быть поставщиком индивидуальный предприниматель.'
            })


