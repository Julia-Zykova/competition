from rest_framework import permissions

from models_app.models import CustomUser


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.method == 'POST':
            return request.user.is_authenticated

        elif request.method in ['PATCH', 'DELETE', 'PUT']:

            if request.user.is_authenticated:
                photo = request.parser_context['kwargs']['photo']
                author = CustomUser.objects.get(photos=photo)
                return author.auth_token.key == request.user.auth_token.key

            return False

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.method in ['PATCH', 'DELETE', 'PUT']:
            if hasattr(obj, 'user'):
                # Instance must have an attribute named `user`.
                return obj.user.auth_token.key == request.user.auth_token.key
            elif hasattr(obj, 'author'):
                # Instance must have an attribute named `author`.
                return obj.author.auth_token.key == request.user.auth_token.key
