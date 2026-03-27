from django.contrib import admin
from .models import Program


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'level', 'delivery_format', 'is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured', 'level', 'delivery_format')
    search_fields = ('title', 'short_description', 'description')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['published_selected', 'unpublished_selected']

    @admin.action(description='Publish selected programs')
    def publish_selected(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description='Unpublish selected programs')
    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)
