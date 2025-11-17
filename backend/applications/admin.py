from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("application_number", "imei", "phone", "status", "created_at")
    search_fields = ("application_number", "imei", "phone")
    list_filter = ("status",)