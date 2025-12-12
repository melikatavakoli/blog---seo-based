from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.shortcuts import reverse
from uuid import uuid4

from core.models import GenericModel
User=get_user_model()

# =========================================================================================================
# ====================== Contact Message MODEL
# =========================================================================================================
class ContactMessage(GenericModel):
    name=models.CharField(
        "name",
        max_length=100,
        null=True,
        blank=True,
    )
    email=models.EmailField()
    subject=models.CharField(
        "subject",
        max_length=200,
        null=True,
        blank=True,
    )
    message=models.TextField(
        "message",
        max_length=300,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "contact us"
        verbose_name_plural = "contact us"
        db_table = 'contact_us'
        # ordering=["-created_at"]

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

# =========================================================================================================
# ====================== Tag MODEL
# =========================================================================================================
class Tag(GenericModel):
    title=models.CharField(
        "title",
        max_length=100,
        null=True,
        blank=True,
    )
    slug=models.SlugField(
        "slug",
        unique=True,
        null=True,
        blank=True,
        allow_unicode=True
    )

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        db_table = 'tag'
        # ordering=["-created_at"]

    def __str__(self):
        return self.title or "none"

# =========================================================================================================
# ====================== Category MODEL
# =========================================================================================================
class Category(GenericModel):
    id = models.UUIDField(
        verbose_name="unique id",
        primary_key=True,
        unique=True,
        default=uuid4,
        editable=False
    )
    title=models.CharField(max_length=100)
    slug=models.SlugField(
        "slug",
        unique=True,
        null=True,
        blank=True,
        allow_unicode=True
    )

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        db_table = 'category'
        # ordering=["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title or "none"

# =========================================================================================================
# ====================== Post MODEL
# =========================================================================================================
class Post(GenericModel):
    slug = models.SlugField(
        "slug",
        unique=True,
        null=True,
        blank=True,
        allow_unicode=True
    )
    title = models.CharField(
        "title",
        max_length=150,
        null=True,
        blank=True,
    )
    body = models.TextField(
        'body',
        null=True,
        blank=True
    )
    description = models.CharField(
        "description",
        max_length=250,
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='%(app_label)s_%(class)s_tags',
        verbose_name='Tags',
    )
    # image = models.ImageField(
    #     "image",
    #     upload_to='media',
    #     blank=True,
    #     null=True
    # )
    is_published = models.BooleanField(
        default=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        db_table = 'post'
        ordering=["-created_at"]

    def __str__(self):
        return self.title or 'Untitled Post'
    
    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_api_url(self):
        try:
            return reverse("post_api:post_detail", kwargs={"slug": self.slug})
        except:
            return None

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})