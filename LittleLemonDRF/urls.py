from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('menu-items', views.MenuItems, 'menu-items')

urlpatterns = router.urls