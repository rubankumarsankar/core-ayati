from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogCategoryViewSet, BlogViewSet

router = DefaultRouter()
router.register(r"blog/categories", BlogCategoryViewSet, basename="blog-category")
router.register(r"blogs", BlogViewSet, basename="blog")

urlpatterns = [
    path("", include(router.urls)),
]
