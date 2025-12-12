from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.pagination import CustomLimitOffsetPagination
from .models import ContactMessage, Post, Tag, Category
from .serializers import CategorySerializer, ContactMessageSerializer, ContactMessageSerializer, PostSerializer, TagSerializer
from rest_framework import viewsets, status, permissions, generics
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.filters import OrderingFilter, SearchFilter
User = get_user_model()

# =========================================================================================================
# ====================== Tags VIEW
# =========================================================================================================
class TagsView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

# =========================================================================================================
# ====================== Category VIEW
# =========================================================================================================
class CategoryView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# =========================================================================================================
# ====================== Contact Us Message VIEW ---> user create
# =========================================================================================================
class ContactUsUserView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset=ContactMessage.objects.all()
    serializer_class=ContactMessageSerializer

# =========================================================================================================
# ====================== Contact Us Message VIEW ---> admin get list
# =========================================================================================================
class ContactUsAdminView(generics.ListAPIView):
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomLimitOffsetPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["category__slug", "title", "tags__title"]
    search_fields = ["title", "slug", "category__title"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PostSerializer
        return PostSerializer