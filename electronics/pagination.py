from rest_framework.pagination import PageNumberPagination


class NetworkNodesPagination(PageNumberPagination):
    """Пагинатор для вывода объектов 'Сетевое звено'"""

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10


class ContactsPagination(PageNumberPagination):
    """Пагинатор для вывода объектов 'Контакт'"""

    page_size = 7
    page_size_query_param = "page_size"
    max_page_size = 15


class ProductsPagination(PageNumberPagination):
    """Пагинатор для вывода объектов 'Продукт'"""

    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 20
