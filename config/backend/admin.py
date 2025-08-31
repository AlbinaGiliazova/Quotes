"""Админка."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend.models import Quote, Source, CustomUser, QuoteVote


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email")


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "source",
        "get_source_name",
        "weight",
        "views",
        "created_at",
        "added_by",
        "get_added_by",
    )
    search_fields = (
        "text",
        "added_by__username",
        "source__name",
        "source_author",
    )
    list_filter = ("source", "added_by")
    autocomplete_fields = ["source", "added_by"]

    def get_source_name(self, obj):
        return obj.source.name

    def get_added_by(self, obj):
        return obj.added_by.username


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "source_type", "author", "year", "details")
    search_fields = ("name", "author")
    list_filter = ("source_type", "year")


@admin.register(QuoteVote)
class QuoteVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'quote', 'value')
    list_filter = ('value', 'user')
    search_fields = ('user__username')
