from rest_framework import permissions

class IsManager(permissions.BasePermission):
    """
    Object-level permission to only allow managers to access the view.
    """
    def has_permission(self, request, view):
        if request.user:
            return request.user.groups.filter(name='manager').exists()
        return False

class IsCrew(permissions.BasePermission):
    """
    Object-level permission to only allow delivery_crew to access the view.
    """
    def has_permission(self, request, view):
        if request.user:
            return request.user.groups.filter(name='delivery_crew').exists()
        return False
    
class IsCustomer(permissions.BasePermission):
    """
    Object-level permission to only allow customers to access the view.
    """
    def has_permission(self, request, view):
        if request.user:
            return request.user.groups.filter(name='customer').exists()
        return False