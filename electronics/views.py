from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView

from electronics.models import Product, Contact, NetworkNode
from electronics.serializer import ProductSerializer, ContactSerializer, NetworkNodeSerializer, \
    NetworkNodeUpdateSerializer


class ProductViewSet(ModelViewSet):
    """
    CRUD для продуктов через ViewSet
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'model']  # Фильтрация по точному совпадению
    search_fields = ['name', 'model']     # Поиск по частичному совпадению
    permission_classes = (IsAuthenticated,)


class ContactViewSet(ModelViewSet):
    """
    CRUD для контактов через ViewSet
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country', 'city']
    search_fields = ['country', 'city', 'email']
    permission_classes = (IsAuthenticated,)


class NetworkNodeCreateAPIView(CreateAPIView):
    """Создаёт объект класса 'Сетевое звено'"""

    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(operation_id="task_create", operation_summary="Создание нового задания")
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    
class NetworkNodeListAPIView(ListAPIView):
    """Передаёт информацию о всех звеньях сети"""

    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = (IsAuthenticated,)
    # pagination_class = NetworkNodesPagination

    @swagger_auto_schema(
        operation_id="owners",
        operation_summary="Список всех сетевых звеньев",
        responses={200: NetworkNodeSerializer(many=True), 400: "Неверные параметры запроса"},
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class NetworkNodeRetrieveAPIView(RetrieveAPIView):
    """Передаёт представление определённого объекта класса 'Сетевое звено'"""

    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        operation_id="task_retrieve",
        operation_summary="Предоставляет всю информацию о выбранном сетевом звене",
    )
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class NetworkNodeUpdateAPIView(UpdateAPIView):
    """Меняет информацию в представлении объекта класса 'Сетевое звено'"""

    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeUpdateSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
    operation_id="task_full_update",
    operation_summary="Полное обновление информации сетевого звена")
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
    operation_id="task_partial_update",
    operation_summary="Частичное обновление информации о сетевом звене")
    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class NetworkNodeDestroyAPIView(DestroyAPIView):
    """Удаляет объект класса 'Сетевое звено'"""

    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(operation_id="task_delete", operation_summary="Удаление задачи")
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
