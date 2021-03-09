from django.contrib import admin

from .models import ApiLog


@admin.register(ApiLog)
class ApiLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "method",
        "path",
        "response_status",
    )
    list_filter = ("created_at", "method", "response_status", "path")
    raw_id_fields = ("created_report",)

    def has_change_permission(self, request, obj=None):
        return False
