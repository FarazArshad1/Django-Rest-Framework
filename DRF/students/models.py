from django.db import models
from uuid import uuid4
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
import re

class ActiveStudentManager(models.Manager):
    """ Manager that returns only active (non-deleted) students"""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)

class Students(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    batch = models.PositiveIntegerField()
    roll_number = models.CharField(max_length=25, unique=True)
    city = models.CharField(max_length=100)

    created_at = models.DateTimeField(null=False)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True ,related_name="deleted_students")

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

    def clean(self):
        """
        Custom Model validation.
        Django automatically calls this when saving via admin or forms,
        but you can also call `full_clean()` manually before saving in code.
        """

        # Validate batch year.
        # Batch year can only be between 2000 and current year
        current_year = datetime.now().year
        if not (2000 <= self.batch <= current_year):
            raise ValidationError(
                {"batch": f"Batch year must be between 2000 and {current_year}"}
            )

        # Make sure the correct format of roll number
        # Each roll must be follow this format F-Batch Year-Batch Section-Serial Number
        expected_prefix = f"F{str(self.batch)[-2:]}"
        pattern = rf"^{expected_prefix}(AB|BB)\d{{3}}$"

        if not re.match(pattern, self.roll_number):
            raise ValidationError(
                {
                    "roll_number": (
                        f"Roll number must follow pattern {expected_prefix}(AB|BB)###,"
                        f"e.g. {expected_prefix}AB001 or {expected_prefix}BB127."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # triggers `clean()`
        super().save(*args, **kwargs)

    # Soft delete
    def delete(self, user=None, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if user:
            self.deleted_by = user
        self.save()

    # Restore a soft-deleted record
    def restore(self):
        self.is_deleted = False
        self.is_deleted = timezone.now()
        self.save()

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ["-batch", "roll_number"]


# subscription -> utils
# cloud loom -> subscription
# make sure ->  imessage, whatsapp works properly
# homespun in cofig -> 90 days
