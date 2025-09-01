# backend/products/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow:
    - Read access to everyone (GET, HEAD, OPTIONS)
    - Write access only to admin users (POST, PUT, PATCH, DELETE)
    """
    def has_permission(self, request, view):
        # Allow read permissions for any request
        if request.method in SAFE_METHODS:
            return True
        
        # Write permissions only for authenticated admin users
        return bool(
            request.user and 
            request.user.is_authenticated and
            (request.user.is_staff or request.user.is_superuser)
        )

# Alternative: Allow all operations (for testing)
class AllowAny(BasePermission):
    """
    Allow any access.
    This permission is not restricted at all.
    """
    def has_permission(self, request, view):
        return True