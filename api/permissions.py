from rest_framework.permissions import BasePermission
from items.models import Item

class IsAddedBy(BasePermission):
    message = "You are not allow to view this page because you did not add this.." 

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj.added_by == request.user:
            return True
        return False