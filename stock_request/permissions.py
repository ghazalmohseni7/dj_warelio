from rest_framework.permissions import BasePermission, SAFE_METHODS


class SRPermissions(BasePermission):
    def has_permission(self, request, view) -> bool:
        if not request.user.is_active:
            return False
        if request.method in SAFE_METHODS:
            return True
        if view.action == 'complete_stock_request':
            return bool(request.user.is_superuser or request.user.is_staff)
        if view.action == 'approve_stock_request':
            return request.user.is_superuser
        return bool(request.user.is_superuser or request.user.is_staff)


class SRIPermissions(BasePermission):
    def has_permission(self, request, view) -> bool:
        if not request.user.is_active:
            return False
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_superuser or request.user.is_staff)
