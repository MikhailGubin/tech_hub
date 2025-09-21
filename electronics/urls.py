from electronics.apps import ElectronicsConfig
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ContactViewSet, NetworkNodeListAPIView, NetworkNodeRetrieveAPIView, \
    NetworkNodeCreateAPIView, NetworkNodeDestroyAPIView, NetworkNodeUpdateAPIView

app_name = ElectronicsConfig.name

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'contacts', ContactViewSet, basename='contact')


urlpatterns = [
    path("", NetworkNodeListAPIView.as_view(), name="network_nodes"),
    path("<int:pk>/", NetworkNodeRetrieveAPIView.as_view(), name="network-node-retrieve"),
    path("create/", NetworkNodeCreateAPIView.as_view(), name="network-node-create"),
    path("<int:pk>/delete/", NetworkNodeDestroyAPIView.as_view(), name="network-node-delete"),
    path("<int:pk>/update/", NetworkNodeUpdateAPIView.as_view(), name="network-node-update"),
    path('', include(router.urls)),
]