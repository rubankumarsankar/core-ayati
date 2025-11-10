from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Role
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    RoleSerializer,
    UserSerializer,
    AdminUserSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class IsRoleAdmin(BasePermission):
    """
    Treat users as admin if:
    - user.role.slug == 'admin'
    - OR user.is_staff / user.is_superuser is True
    """

    def has_permission(self, request, view):
        user = request.user

        if not (user and user.is_authenticated):
            return False

        # Check custom Role model
        role = getattr(user, "role", None)
        if role and getattr(role, "slug", "").lower() == "admin":
            return True

        # Fallback to Django staff/superuser
        if user.is_staff or user.is_superuser:
            return True

        return False


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    "message": "User registered successfully",
                    "user": UserSerializer(user).data,
                    "tokens": tokens,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    "message": "Login successful",
                    "user": UserSerializer(user).data,
                    "tokens": tokens,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    """
    GET /api/auth/me/
    Returns the logged-in user's details + role.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleViewSet(viewsets.ModelViewSet):
    """
    Role CRUD:

    - GET    /api/roles/        -> list roles        (auth required)
    - GET    /api/roles/{id}/   -> retrieve role     (auth required)
    - POST   /api/roles/        -> create role       (admin)
    - PUT    /api/roles/{id}/   -> full update       (admin)
    - PATCH  /api/roles/{id}/   -> partial update    (admin)
    - DELETE /api/roles/{id}/   -> delete role       (admin)
    """
    queryset = Role.objects.all().order_by("id")
    serializer_class = RoleSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsRoleAdmin()]


class UserViewSet(viewsets.ModelViewSet):
    """
    Admin-only User management:

    - GET    /api/users/        -> list users
    - GET    /api/users/{id}/   -> user details
    - POST   /api/users/        -> create user (with role, password)
    - PUT    /api/users/{id}/   -> full update
    - PATCH  /api/users/{id}/   -> partial update (role, status, etc.)
    - DELETE /api/users/{id}/   -> delete user

    Uses AdminUserSerializer.
    """
    queryset = User.objects.select_related("role").all().order_by("id")
    serializer_class = AdminUserSerializer

    def get_permissions(self):
        return [IsRoleAdmin()]
