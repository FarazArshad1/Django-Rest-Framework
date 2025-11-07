from django.contrib import admin
from .models import Students

# Register your models here.

@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["name", "roll_number", "batch", "city"]
    list_display_links = ["name", "roll_number"]
    search_fields = ["name", "roll_number", "city"]
    list_filter = ["batch", "city"]
    ordering = ["-batch", "roll_number"]
    readonly_fields = ["id"]
