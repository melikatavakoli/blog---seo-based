from rest_framework import serializers
from .models import Media, Post, ContactMessage, Redirect, Schema, Tag, Category
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import re
User=get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# =========================================================================================================
# ====================== Media Serializer
# =========================================================================================================
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            "id",
            "image",
            "created_at",
            "meta_og_image",
        ]
# =========================================================================================================
# ====================== Post Serializer
# =========================================================================================================
class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug'
        ]

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)

# =========================================================================================================
# ====================== Schema Serializer
# =========================================================================================================
class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schema
        fields = ["id", "content", "created_at", "post"]

# =========================================================================================================
# ====================== Tags Serializer
# =========================================================================================================
class TagsSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model=Tag
        fields = [
            "id",
            "title",
            "slug"
        ]

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)
    
# =========================================================================================================
# ====================== Post Serializer
# =========================================================================================================
class PostSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source='category.title', read_only=True)
    tags = serializers.CharField(source='tag.title', read_only=True)
    created_by = serializers.CharField(source="created_by.username", read_only=True)
    schema_items = SchemaSerializer(many=True, read_only=True)
    image = MediaSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            'category_title',
            "title",
            "image",
            "description",
            "body",
            'slug',
            'body',
            'tags',
            'created_by',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'canonical',
            'index',
            'follow',
            "schema_items",
            "alt"
        ]

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
    
# =========================================================================================================
# ====================== List Post Serializer
# =========================================================================================================
class ListPostSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source='category.title', read_only=True)
    tags = serializers.CharField(source='tag.title', read_only=True)
    created_by = serializers.CharField(source="created_by.username", read_only=True)
    schema_items = SchemaSerializer(many=True, read_only=True)
    image = MediaSerializer(read_only=True)
    # created_by = UserSerializer(read_only=True)  

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
            "created_by",
            'created_at',
            "meta_title",
            "meta_description",
            "meta_keywords",
            'canonical',
            'index',
            'follow',
            "schema_items",
            "alt",
        ]

# =========================================================================================================
# ====================== Post Create Update Serializer
# =========================================================================================================
class PostCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
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
    image = serializers.PrimaryKeyRelatedField(queryset=Media.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "image",
            "description",
            "category",
            "slug",
            "body",
            "tags",
            "meta_title",
            "meta_description",
            "meta_keywords",
            'canonical',
            'index',
            "schema_items",
            'follow',
            "alt"
        ]

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

# =========================================================================================================
# ====================== Redirect Serializer
# =========================================================================================================
class RedirectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redirect
        fields = [
            "id",
            "origin",
            "target",
            "status",
        ]

# =========================================================================================================
# ====================== Detail Post Serializer
# =========================================================================================================
class DetailPostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    created_by = serializers.CharField(source="created_by.username", read_only=True)
    schema_items = SchemaSerializer(many=True, read_only=True)
    image = MediaSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            'category',
            "title",
            "image",
            "description",
            "body",
            'slug',
            'body',
            'tags',
            'created_by',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'canonical',
            'index',
            'follow',
            "schema_items",
            "alt"
        ]

# =========================================================================================================
# ====================== Contact Message -- create / Serializer
# =========================================================================================================
class ContactMessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model= ContactMessage
        fields=[
            'id',
            'name',
            'mobile',
            'work_field',
            'company_name'
        ]

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

