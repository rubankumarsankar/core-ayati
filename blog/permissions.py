from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    - Anyone authenticated can GET.
    - Only admin role (user.role.slug == 'admin') can POST/PATCH/DELETE.
    Adjust if your role model differs.
    """

    def has_permission(self, request, view):
        # allow safe methods for authenticated users
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # write operations: must be admin role
        user = request.user
        role_slug = getattr(getattr(user, "role", None), "slug", None)
        return bool(user and user.is_authenticated and role_slug == "admin")
