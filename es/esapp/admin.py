from django.contrib import admin

# Register your models here.
from .models import Events

# custom admin
from django.conf import settings

# admin.site.register(Events)


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "date",
        "description",
        "category",
        "location",
        "status",
        "user",
    ]
    list_filter = ["id", "title", "user", "location"]


class CustomAdminSite(admin.AdminSite):
    site_header = settings.SITE_NAME
    site_title = settings.SITE_NAME
    index_title = f"Welcome to {settings.SITE_NAME}"


# admin.site = CustomAdminSite()
