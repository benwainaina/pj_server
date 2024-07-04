from django.contrib import admin
from .models import Entry, EntryCategory

@admin.register(Entry)
class EntryModelAdmin(admin.ModelAdmin):
    list_display = [
        'owner',
        'title',
        'content',
        'category',
        'date',
    ]
    
@admin.register(EntryCategory)
class EntryCategoryModelAdmin(admin.ModelAdmin):
    list_display = [
        'category_name',
        'category_uuid'
    ]
    