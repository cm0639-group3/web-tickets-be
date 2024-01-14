from rest_framework import permissions

class TicketPermissions(permissions.BasePermission):
    def has_permission(self, request, view) :
        if view.action == "create":
            return request.user.is_authenticated
        elif view.action == "list":
            return request.user.is_authenticated
        elif view.action in ["retrieve"]:
            return request.user.is_authenticated
        elif view.action in ["update", "partial_update"]:
            return False
        elif view.action in ["destroy"]:
            return request.user.is_authenticated
        elif view.action in ['current_price']:
            return request.user.is_authenticated
        else:
            return False
