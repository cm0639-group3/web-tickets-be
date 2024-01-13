from rest_framework import permissions

class OrderPermissions(permissions.BasePermission):
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
        else:
            return False
