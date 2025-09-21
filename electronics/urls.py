from electronics.apps import ElectronicsConfig
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ContactViewSet


app_name = ElectronicsConfig.name

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    # path('network-nodes/', NetworkNodeAPIView.as_view(), name='network-node-list'),
    # path('network-nodes/<int:pk>/', NetworkNodeAPIView.as_view(), name='network-node-detail'),

    path('', include(router.urls)),
]