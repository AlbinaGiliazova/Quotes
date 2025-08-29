"""Админка."""

from django.contrib import admin
from backend.models import Quote, Source


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'source',
        'get_source_name',
        'weight',
        'views',
        'likes',
        'dislikes',
        'created_at',
        'added_by',
        'get_added_by',
    )
    search_fields = (
        'text',
        'added_by__username',
        'source__name',
        'source_author',
    )
    list_filter = ('source', 'added_by')
    autocomplete_fields = ['source', 'added_by']

    def get_source_name(self, obj):
        return obj.source.name
    
    def get_added_by(self, obj):
        return obj.added_by.username
    
    get_added_by.short_description = 'Пользователь'
    get_source_name.short_description = 'Источник'


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_type', 'author', 'year', 'details')
    search_fields = ('name', 'author')
    list_filter = ('source_type', 'year')
