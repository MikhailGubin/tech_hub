from django.utils import timezone
from rest_framework.serializers import ValidationError


class AddressContactValidator:
    """Проверяет связи между городом, улицей и номером дома"""

    def __call__(self, attrs):
        """
        attrs - это уже частично валидированные данные
        """
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
        if release_date > timezone.now():
            raise ValidationError(
                {"release_date": "Дата выхода продукта на рынок не может быть в будущем."}
            )


class SupplierNetworkNodeValidator:
    """ Настраивает правильные условия для поля 'Поставщик' """

    def __init__(self, field, instance):
        self.field = field
        self.instance = instance

    def __call__(self, value):
        supplier = value

        if self.instance.node_type == self.instance.NodeType.FACTORY and supplier is not None:
            raise ValidationError({'supplier': 'Завод не может иметь поставщика.'})

        if self.instance.supplier == supplier:
            raise ValidationError({'supplier': 'Объект не может быть поставщиком для самого себя.'})

        if (self.instance.node_type == self.instance.NodeType.FACTORY and
                supplier.node_type == self.instance.NodeType.ENTREPRENEUR):
            raise ValidationError(
                {'supplier': 'У розничной сети не может быть поставщиком индивидуальный предприниматель.'}
            )
