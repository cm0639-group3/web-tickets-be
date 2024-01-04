from rest_framework import permissions

class CustomPermissions_1(permissions.BasePermission):
    def has_permission(self, request, view) :        
        # CRUD
        # Create
        if view.action == "create":
            return request.user.is_authenticated and request.user.is_staff
        # Read
        if view.action == "list":
            return True
        elif view.action in ["retrieve"]:
            return True
        # Update
        elif view.action in ["update", "partial_update"]:
            return request.user.is_authenticated and request.user.is_staff
        # Delete
        elif view.action in ["destroy"]:
            return request.user.is_authenticated and request.user.is_staff
        else:
            return False