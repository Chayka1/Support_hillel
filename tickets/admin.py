from django.contrib import admin

from tickets.models import Ticket


@admin.register(Ticket)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ["user", "title", "text"]
    list_display = ["title", "user", "manager", "status"]
    list_filter = ["status", "manager"]
    search_fields = ["title"]
