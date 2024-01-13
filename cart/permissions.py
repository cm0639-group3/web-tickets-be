from rest_framework import permissions

class CartPermissions(permissions.BasePermission):
    def has_permission(self, request, view) :
        if view.action == "create":
            return False
        elif view.action == "list":
            return request.user.is_authenticated
        elif view.action in ["retrieve"]:
            return False
        elif view.action in ["update", "partial_update"]:
            return False
        elif view.action in ["destroy"]:
            return False
        elif view.action in ['buy_tickets' , 'clear_cart']:
            return request.user.is_authenticated
        else:
            return False
