from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from config.core.permissions import ManagePermission
User = get_user_model()

# -----------------------------------------------------------------------------------

class BaseAPIView(APIView):
    def success_response(self, data=None, message=None, status_code=status.HTTP_200_OK):
        data = data or {}
        return Response(data, status=status_code)

class BaseModelViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            status=status.HTTP_204_NO_CONTENT)

#------------for all view ----------------------
class BaseViewSet(ModelViewSet):
    permission_classes = [ManagePermission]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.role in ['superuser', 'admin']:
            return self.queryset.all()

        if user.role == 'user':
            return self.queryset.filter(_created_by=user)
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(_created_by=self.request.user)


#------------for without _created_by view/user ----------------------
class BaseUserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.role == 'admin':
            return self.queryset.all()

        if user.role == 'user':
            return self.queryset.filter(id=user.id)

        return self.queryset.none()