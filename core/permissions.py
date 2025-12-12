from django.contrib.auth import get_user_model
from rest_framework import permissions
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, BasePermission
User = get_user_model()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL: combine
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ManagePermission(permissions.BasePermission):
    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser or user.role in ['superuser', 'admin']:
            return True

        if user.role == 'user':
            return getattr(obj, '_created_by', None) == user

        return False
# ~~~~~~~~~~~~~~~~~~~~~~ allowed host  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class HostAllowedPermission(BasePermission):
    def has_permission(self, request, view):
        allowed_hosts = settings.ALLOWED_EXPORT_IPS
        secret_token = settings.SECRET_KEY_API
        allowed_user_id = settings.ALLOWED_USER

        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        request_token = request.headers.get('X-Secret-Token')

        # Check user authentication and ID match
        user_allowed = (
            request.user and
            request.user.is_authenticated and
            str(request.user.id) == str(allowed_user_id)
        )
        print(f"Client IP: {ip}, Allowed IPs: {allowed_hosts}")
        print(f"Token Match: {request_token == secret_token}")
        print(f"IP Match: {ip in allowed_hosts}")
        print(f"User Match: {user_allowed}")

        return (
            ip in allowed_hosts and
            request_token == secret_token and
            user_allowed
        )