from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, RoleViewSet

router = DefaultRouter()
router.register(r"roles", RoleViewSet, basename="role")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("", include(router.urls)),
]
