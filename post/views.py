from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from common.paginations import CustomLimitOffsetPagination
from .models import (
    Media, 
    Post,
    ContactMessage,
    Redirect, 
    Schema, 
    Tag,
    Category
    )
from .serializers import (
    DetailPostSerializer,
    MediaSerializer,
    RedirectSerializer,
    SchemaSerializer,
    TagsSerializer, 
    CategorySerializer,
    PostCreateUpdateSerializer,
    ListPostSerializer,
    ContactMessageCreateSerializer
    )
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import viewsets, permissions, generics, mixins
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.filters import OrderingFilter, SearchFilter
User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomLimitOffsetPagination

    filter_backends = [
        DjangoFilterBackend, 
        OrderingFilter, 
        SearchFilter
        ]
    filterset_fields = [
        "category__slug",
        "title", 
        "tags__title"
        ]
    search_fields = [
        "title",
        "slug", 
        "category__title"
        ]
    ordering_fields = [
        "created_at", 
        "updated_at"
        ]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ListPostSerializer
        return PostCreateUpdateSerializer
    
class ListPostAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    serializer_class = ListPostSerializer
    pagination_class = CustomLimitOffsetPagination

    filter_backends = [
        DjangoFilterBackend, 
        OrderingFilter, 
        SearchFilter
        ]
    filterset_fields = [
        "category__slug", 
        "title", 
        "tags__title"
        ]
    search_fields = [
        "title",
        "slug",
        "category__title"
    ]
    ordering_fields = [
        "created_at", 
        "updated_at"
        ]
    ordering = ["-created_at"]

class CreateUpdatePostAPIView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView ):
    
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class PostRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = DetailPostSerializer
    queryset = Post.objects.all()
    lookup_field = "id"

class TagsView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer

class CategoryView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostDetailBySlugAPIView(APIView):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        serializer = DetailPostSerializer(post)
        return Response(serializer.data)

class RedirectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Redirect.objects.all()
    serializer_class = RedirectSerializer
    pagination_class = CustomLimitOffsetPagination

class SchemaViewSet(viewsets.ModelViewSet):
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer
    permission_classes = [permissions.AllowAny]

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.AllowAny]

class ContactMessageCreateView(CreateAPIView):
    serializer_class = ContactMessageCreateSerializer
    permission_classes = [AllowAny]
    queryset = ContactMessage.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            ip_address=self.request.META.get('REMOTE_ADDR')
        )

