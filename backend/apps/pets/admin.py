from django.contrib import admin

from .models import Pet, Vaccination


class VaccinationInline(admin.TabularInline):
    model = Vaccination
    extra = 0


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ["name", "species", "breed", "owner", "created_at"]
    list_filter = ["species"]
    search_fields = ["name", "breed", "owner__phone", "owner__name"]
    inlines = [VaccinationInline]
