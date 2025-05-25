from rest_framework.permissions import BasePermission, SAFE_METHODS


class SupplierPermissions(BasePermission):
    def has_permission(self, request, view) -> bool:
        if not request.user.is_active:
            return False
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_superuser or request.user.is_staff)
