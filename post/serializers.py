from rest_framework import serializers
from common.base import GenericModelSerializer
from .models import (
    Media, 
    Post, 
    ContactMessage, 
    Redirect, 
    Schema, 
    Tag,
    Category
    )
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import re
User=get_user_model()

class UserSerializer(GenericModelSerializer):
    class Meta:
        model = User
        fields = GenericModelSerializer.Meta.fields + (
            'id', 
            'username'
            )

class MediaSerializer(GenericModelSerializer):
    class Meta:
        model = Media
        fields = GenericModelSerializer.Meta.fields + (
            "id",
            "image",
            "created_at",
            "meta_og_image",
        )

class CategorySerializer(GenericModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = GenericModelSerializer.Meta.fields + (
            'id',
            'title',
            'slug'
        )

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)

class SchemaSerializer(GenericModelSerializer):
    class Meta:
        model = Schema
        fields = GenericModelSerializer.Meta.fields + (
            "id", 
            "content",
            "post"
            )

class TagsSerializer(GenericModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model=Tag
        fields = GenericModelSerializer.Meta.fields + (
            "id",
            "title",
            "slug",
            "description"
        )

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)
    
class PostSerializer(GenericModelSerializer):
    category_title = serializers.CharField(
        source='category.title',
        read_only=True
        )
    tags = serializers.CharField(
        source='tag.title', 
        read_only=True
        )
    schema_items = SchemaSerializer(
        many=True, 
        read_only=True
        )
    image = MediaSerializer(read_only=True)

    class Meta:
        model = Post
        fields = GenericModelSerializer.Meta.fields + (
            "id",
            'category_title',
            "title",
            'is_published',
            "image",
            "description",
            "body",
            'slug',
            'body',
            'tags',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'canonical',
            'index',
            'follow',
            "schema_items",
            "alt"
        )

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'], allow_unicode=True)
        base_slug = validated_data['slug']
        unique_slug = base_slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{num}"
            num += 1
        validated_data['slug'] = unique_slug
        
        return super().create(validated_data)
    
class ListPostSerializer(GenericModelSerializer):
    category_title = serializers.CharField(
        source='category.title',
        read_only=True
        )
    tags = serializers.CharField(
        source='tag.title', 
        read_only=True
        )
    schema_items = SchemaSerializer(
        many=True, 
        read_only=True
        )
    image = MediaSerializer(read_only=True)  

    class Meta:
        model = Post
        fields = [
            "id",
            "category_title",
            "title",
            "image",
            "description",
            "slug",
            "tags",
            'is_published',
            "meta_title",
            "meta_description",
            "meta_keywords",
            'canonical',
            'index',
            'follow',
            "schema_items",
            "alt",
        ]

class PostCreateUpdateSerializer(GenericModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
        )
    schema_items = serializers.PrimaryKeyRelatedField(
        queryset=Schema.objects.all(),
        many=True,
        required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )
    image = serializers.PrimaryKeyRelatedField(
        queryset=Media.objects.all(), 
        required=False,
        allow_null=True
        )

    class Meta:
        model = Post
        fields = GenericModelSerializer.Meta.fields + (
            "id",
            "title",
            "image",
            "description",
            "category",
            "slug",
            "body",
            'is_published',
            "tags",
            "meta_title",
            "meta_description",
            "meta_keywords",
            'canonical',
            'index',
            "schema_items",
            'follow',
            "alt"
        )

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        schemas = validated_data.pop("schema_items", [])
        post = super().create(validated_data)
        if tags:
            post.tags.set(tags)
        for schema in schemas:
            schema.post = post
            schema.save()
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", [])
        schemas = validated_data.pop("schema_items", [])
        post = super().update(instance, validated_data)
        if tags:
            post.tags.set(tags)
        Schema.objects.filter(post=post).update(post=None)
        for schema in schemas:
            schema.post = post
            schema.save()
        return post

class RedirectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redirect
        fields = [
            "id",
            "origin",
            "target",
            "status",
        ]

class DetailPostSerializer(GenericModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    schema_items = SchemaSerializer(many=True, read_only=True)
    image = MediaSerializer(read_only=True)

    class Meta:
        model = Post
        fields = GenericModelSerializer.Meta.fields + (
            "id",
            'category',
            "title",
            "image",
            "description",
            "body",
            'slug',
            'body',
            'tags',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'canonical',
            'index',
            'follow',
            "schema_items",
            "alt"
        )

class ContactMessageCreateSerializer(GenericModelSerializer):
    class Meta:
        model= ContactMessage
        fields= GenericModelSerializer.Meta.fields + (
            'id',
            'name',
            'mobile',
            'work_field',
            'company_name'
        )

    def validate(self, data):
        mobile = data.get('mobile')
        if not mobile:
            raise serializers.ValidationError(
                "وارد کردن شماره موبایل الزامی است."
            )
        return data

    def validate_message(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("متن پیام خیلی کوتاه است")
        return value

    def validate_mobile(self, value):
        if value:
            if not re.match(r'^09\d{9}$', value):
                raise serializers.ValidationError("شماره موبایل معتبر نیست")
        return value

