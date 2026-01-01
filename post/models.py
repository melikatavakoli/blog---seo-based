from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.shortcuts import reverse
from uuid import uuid4
User=get_user_model()

# =========================================================================================================
# ====================== Contact Message MODEL
# =========================================================================================================
class ContactMessage(models.Model):
    id = models.UUIDField(
        verbose_name="unique id",
        primary_key=True,
        unique=True,
        default=uuid4,
        editable=False
    )
    name=models.CharField(
        "name",
        max_length=100,
        null=True,
        blank=True,
    )
    company_name=models.CharField(
        "company_name",
        max_length=100,
        null=True,
        blank=True,
    )
    mobile = models.CharField(
        max_length=11,
        blank=True,
        null=True
    )
    work_field=models.CharField(
        "work_field",
        max_length=200,
        null=True,
        blank=True,
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )
    created_at=models.DateTimeField(
        "created_at",
        auto_now=True,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created_by"
    )

    class Meta:
        verbose_name = "contact us"
        verbose_name_plural = "contact us"
        db_table = 'contact_us'
        # ordering=["-created_at"]

    def __str__(self):
        return self.name or "none"

# =========================================================================================================
# ====================== Tag MODEL
# =========================================================================================================
class Tag(models.Model):
    id = models.UUIDField(
        verbose_name="unique id",
        primary_key=True,
        unique=True,
        default=uuid4,
        editable=False
    )
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
class Category(models.Model):
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
# ====================== Media MODEL
# =========================================================================================================
class Media(models.Model):
    id = models.UUIDField(
        verbose_name="unique id",
        primary_key=True,
        unique=True,
        default=uuid4,
        editable=False
    )
    image = models.ImageField(
        "image",
        upload_to='media',
        blank=True,
        null=True
    )
    meta_og_image = models.ImageField(
        "meta_og_image",
        upload_to="meta_images/",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        verbose_name='Created At',
    )

    class Meta:
        verbose_name = "media"
        verbose_name_plural = "media"
        db_table = 'media'
        ordering=["-created_at"]

    def __str__(self):
        return self.image.name if self.image else str(self.id)
# =========================================================================================================
# ====================== Post MODEL
# =========================================================================================================
class Post(models.Model):
    id = models.UUIDField(
        verbose_name="unique id",
        primary_key=True,
        unique=True,
        default=uuid4,
        editable=False
    )
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
        blank=True,
        related_name='%(app_label)s_%(class)s_tags',
        verbose_name='Tags',
    )
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        verbose_name='Created At',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        verbose_name='Updated At',
    )
    image = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(
        default=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    meta_title = models.CharField(
        "meta_title",
        max_length=200,
        null=True,
        blank=True
    )
    meta_description = models.CharField(
        "meta_description",
        max_length=300,
        null=True,
        blank=True
    )
    meta_keywords = models.CharField(
        "meta_keywords",
        max_length=300,
        null=True,
        blank=True
    )
    canonical = models.CharField(
        "canonical",
        max_length=200,
        null=True,
        blank=True
    )
    index = models.BooleanField(
        default=True
    )
    follow = models.BooleanField(
        default=False
    )
    alt = models.CharField(
        "alt",
        max_length=1000,
        null=True,
        blank=True,
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

# =========================================================================================================
# ====================== Redirect
# =========================================================================================================
class Redirect(models.Model):
    id = models.UUIDField(
        verbose_name="unique id",
        primary_key=True,
        unique=True,
        default=uuid4,
        editable=False
    )
    origin = models.CharField(
        "origin",
        max_length=1000,
        null=True,
        blank=True,
    )
    target = models.CharField(
        "target",
        max_length=1000,
        null=True,
        blank=True,
    )
    status = models.CharField(
        "status",
        max_length=1000,
        null=True,
        blank=True,
    )
    
    class Meta:
        verbose_name = "redirect"
        verbose_name_plural = "redirect"
        db_table = 'redirect'
        # ordering=["-created_at"]

    def __str__(self):
        return str(self.id) if self.id else 'none'
    
# =========================================================================================================
# ====================== Schema
# =========================================================================================================
class Schema(models.Model):
    id = models.UUIDField(
        verbose_name="unique id",
        primary_key=True,
        unique=True,
        default=uuid4,
        editable=False
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="schema_items",
        null=True,
        blank=True,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "schema"
        verbose_name = "schema"
        verbose_name_plural = "schemas"

    def __str__(self):
        return self.content or None