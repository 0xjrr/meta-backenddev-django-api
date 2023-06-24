from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'menu-items', views.MenuItems, basename='menu-items')
router.register(r'cart/menu-items', views.CartViewSet, basename='cart')
router.register(r'groups/manager/users', views.ManagerGroupViewSet, basename='manager-group')
router.register(r'groups/delivery-crew/users', views.DeliveryCrewGroupViewSet, basename='delivery-crew-group')
router.register(r'orders', views.OrderViewSet, basename='orders')

urlpatterns = router.urls