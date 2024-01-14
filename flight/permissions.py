from rest_framework import permissions

class FlightPermissions(permissions.BasePermission):
    def has_permission(self, request, view) :
        if view.action == "create":
            return request.user.is_authenticated and request.user.is_staff
        elif view.action == "list":
            return True
        elif view.action in ["retrieve"]:
            return True
        elif view.action in ["update", "partial_update"]:
            return request.user.is_authenticated and request.user.is_staff
        elif view.action in ["destroy"]:
            return request.user.is_authenticated and request.user.is_staff
        elif view.action in ['current_price', 'add_to_cart']:
            return request.user.is_authenticated
        else:
            return False
