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

        print(f"Validator: node_type={node_type}, supplier={supplier}, type={type(supplier)}")

        # Если supplier не передан
        if supplier is None:
            if node_type != NetworkNode.NodeType.FACTORY:
                raise ValidationError({
                    'supplier': 'Объект без поставщика может быть только Заводом.'
                })
            return attrs

        # Если supplier это ID (число), преобразуем в объект для проверок
        if isinstance(supplier, int):
            try:
                supplier_obj = NetworkNode.objects.get(id=supplier)
            except NetworkNode.DoesNotExist:
                raise ValidationError({'supplier': 'Указанный поставщик не существует.'})
        else:
            # Если это уже объект, используем его
            supplier_obj = supplier

        # Проверка: Завод не может иметь поставщика
        if node_type == NetworkNode.NodeType.FACTORY:
            raise ValidationError({'supplier': 'Завод не может иметь поставщика.'})

        # Проверка: Нельзя быть поставщиком для самого себя
        if self.instance and supplier_obj.id == self.instance.id:
            raise ValidationError({'supplier': 'Объект не может быть поставщиком для самого себя.'})

        # Проверка: Розничная сеть не может иметь поставщиком ИП
        if node_type == NetworkNode.NodeType.RETAIL and supplier_obj.node_type == NetworkNode.NodeType.ENTREPRENEUR:
            raise ValidationError({
                'supplier': 'У розничной сети не может быть поставщиком индивидуальный предприниматель.'
            })

        return attrs
