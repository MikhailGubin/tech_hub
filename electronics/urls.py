from django.urls import include, path
from rest_framework.routers import DefaultRouter

from electronics.apps import ElectronicsConfig

from .views import (
    ContactViewSet,
    NetworkNodeCreateAPIView,
    NetworkNodeDestroyAPIView,
    NetworkNodeListAPIView,
    NetworkNodeRetrieveAPIView,
    NetworkNodeUpdateAPIView,
    ProductViewSet
)

app_name = ElectronicsConfig.name

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"contacts", ContactViewSet, basename="contact")


urlpatterns = [
    path("", NetworkNodeListAPIView.as_view(), name="network-nodes-list"),
    path("<int:pk>/", NetworkNodeRetrieveAPIView.as_view(), name="network-node-retrieve"),
    path("create/", NetworkNodeCreateAPIView.as_view(), name="network-node-create"),
    path("<int:pk>/delete/", NetworkNodeDestroyAPIView.as_view(), name="network-node-delete"),
    path("<int:pk>/update/", NetworkNodeUpdateAPIView.as_view(), name="network-node-update"),
    path("", include(router.urls)),
]
