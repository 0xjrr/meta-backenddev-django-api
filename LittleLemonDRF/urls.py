from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'menu-items', views.MenuItems, basename='menu-items')
router.register(r'cart/menu-items', views.CartViewSet, basename='cart')

urlpatterns = router.urls