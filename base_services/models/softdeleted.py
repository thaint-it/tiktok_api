from django.db import models
from django.utils import timezone


class SoftDeletableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeletableModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeletableManager()
    
    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()
