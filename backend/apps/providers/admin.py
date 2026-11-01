from django.contrib import admin

from .models import ProviderProfile, Service


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ["business_name", "city", "status", "offers_home_service", "created_at"]
    list_filter = ["status", "city", "offers_home_service"]
    search_fields = ["business_name", "user__phone", "license_number"]
    inlines = [ServiceInline]
    actions = ["mark_verified", "mark_rejected"]

    @admin.action(description="Verify selected providers")
    def mark_verified(self, request, queryset):
        queryset.update(status=ProviderProfile.Status.VERIFIED)

    @admin.action(description="Reject selected providers")
    def mark_rejected(self, request, queryset):
        queryset.update(status=ProviderProfile.Status.REJECTED)
