from core.serializers import GenericModelSerializer
from rest_framework import serializers
from django.utils.text import slugify
from post.models import Category, ContactMessage, Post, Tag

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~ category serializer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CategorySerializer(GenericModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta(GenericModelSerializer.Meta):
        model = Category
        fields = GenericModelSerializer.Meta.fields + (
            'id',
            'title',
            'slug'
        )

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~ category serializer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ContactMessageSerializer(GenericModelSerializer):
    class Meta(GenericModelSerializer.Meta):
        model = ContactMessage
        fields = GenericModelSerializer.Meta.fields + (
            'id',
            'name',
            'email',
            'subject',
            'message',
        )

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~ category serializer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TagSerializer(GenericModelSerializer):
    class Meta(GenericModelSerializer.Meta):
        model = Tag
        fields = GenericModelSerializer.Meta.fields + (
            'id',
            'title',
            'slug'
        )

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~ category serializer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PostSerializer(GenericModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta(GenericModelSerializer.Meta):
        model = Post
        fields = GenericModelSerializer.Meta.fields + (
            'id',
            'title',
            'slug',
            'body',
            'description',
            'tags',
            # 'image',
            'is_published',
            'category'
        )