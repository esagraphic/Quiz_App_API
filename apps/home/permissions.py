from rest_framework.permissions import BasePermission, SAFE_METHODS

class AllowCreateUser(BasePermission):
    """
    - Allows **anyone** to create a user (POST /users/).
    - Requires authentication for all other requests (GET, PUT, DELETE).
    """

    def has_permission(self, request, view):
        # Allow user creation without authentication
        if view.action == 'create':  
            return True  
        
        # For all other actions, authentication is required
        return request.user and request.user.is_authenticated
