from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    LoginView,
    MeView,
    RoleViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"roles", RoleViewSet, basename="role")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]
