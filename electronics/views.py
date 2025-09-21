from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from electronics.models import Product, Contact
from electronics.serializer import ProductSerializer, ContactSerializer


class ProductViewSet(ModelViewSet):
    """
    CRUD для продуктов через ViewSet
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'model']  # Фильтрация по точному совпадению
    search_fields = ['name', 'model']     # Поиск по частичному совпадению

class ContactViewSet(ModelViewSet):
    """
    CRUD для контактов через ViewSet
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country', 'city']
    search_fields = ['country', 'city', 'email']
