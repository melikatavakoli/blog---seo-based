from uuid import uuid4
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from django_currentuser.db.models import CurrentUserField
from rest_framework import serializers


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(_is_deleted=True, _deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(_is_deleted=False)

    def dead(self):
        return self.filter(_is_deleted=True)

class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', None)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only is True:
            return SoftDeleteQuerySet(self.model).filter(_is_deleted=False)
        if self.alive_only is False:
            return SoftDeleteQuerySet(self.model).filter(_is_deleted=True)
        if self.alive_only is None:
            return SoftDeleteQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()
    
class GenericModel(models.Model):
    id = models.UUIDField(
        verbose_name=_("unique id"),
        primary_key=True,
        unique=True,
        null=False,
        default=uuid4,
        editable=False
    )
    _created_by = CurrentUserField(
        related_name="%(app_label)s_%(class)s_created_by",
        verbose_name=_("created by"),
    )
    _updated_by = CurrentUserField(
        related_name="%(app_label)s_%(class)s_updated_by",
        verbose_name=_("updated by"),
        on_update=True
    )
    _created_at = models.DateTimeField(
        verbose_name=_('created at'),
        default=timezone.now
    )
    _updated_at = models.DateTimeField(
        verbose_name=_('updated at'),
        auto_now=True
    )
    _is_deleted = models.BooleanField(default=False)
    _deleted_at = models.DateTimeField(null=True, blank=True)
    objects = SoftDeleteManager(alive_only=True)
    all_objects = SoftDeleteManager(alive_only=None)
    deleted_objects = SoftDeleteManager(alive_only=False)

    def delete(self, using=None, keep_parents=False):
        self._is_deleted = True
        self._deleted_at = timezone.now()
        self.save(using=using)

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self._is_deleted = False
        self._deleted_at = None
        self.save()
        
    class Meta:
        abstract = True
        indexes = (
            models.Index(fields=['id'], name='%(class)s_id_idx'),
        )
    @property
    def created_by(self):
        if self._created_by:
            return f"{self._created_by.first_name} {self._created_by.last_name}".strip() or self._created_by.mobile
        return None

    @property
    def updated_by(self):
        if self._updated_by:
            return f"{self._updated_by.first_name} {self._updated_by.last_name}".strip() or self._updated_by.mobile
        return None

    @cached_property
    def can_delete(self):
        for field in self._meta.related_objects:
            try:
                if getattr(self, field.related_name).all().exists():
                    return False
            except Exception as e:
                pass
        return True
    
    
class GenericModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    _created_by = serializers.SerializerMethodField()
    _updated_by = serializers.SerializerMethodField()
    can_delete = serializers.ReadOnlyField()

    class Meta:
        model = None
        fields = (
            "id",
            "_created_by",
            "created_by",
            "_updated_by",
            "updated_by",
            "created_at",
            "updated_at",
            "can_delete",
        )
        read_only_fields = fields

    def get__created_by(self, obj):
        user = getattr(obj, "_created_by", None)
        if not user or hasattr(user, "all"):
            return None
        return f"{user.first_name} {user.last_name}".strip() or user.mobile
    
    def get_updated_by(self, obj):
        user = getattr(obj, "_updated_by", None)
        if not user or hasattr(user, "all"):
            return None
        return f"{user.first_name} {user.last_name}".strip() or user.mobile

    def get_created_by(self, obj):
        """
        فقط id کاربر را برمی‌گرداند.
        """
        user = getattr(obj, "created_by", None)
        if not user:
            return None
        # اگر user یک رشته باشد، فرض کن id همان رشته است
        if isinstance(user, str):
            return user
        # اگر user یک شیء User است
        return str(getattr(user, "id", None))

    def get__updated_by(self, obj):
        """
        فقط id کاربر را برمی‌گرداند.
        """
        user = getattr(obj, "_updated_by", None)
        if not user or hasattr(user, "all"):
            return None
        return str(user.id)

    def get_created_at(self, obj):
        return getattr(obj, "created_at", None)

    def get_updated_at(self, obj):
        return getattr(obj, "updated_at", None)