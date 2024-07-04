from django.urls import path
from . import views

urlpatterns = [
    path('create_category', views.create_journal_category),
    path('available_categories', views.get_available_journal_categories),
    path('create_entry', views.create_entry),
    path('update_entry', views.update_journal),
    path('delete', views.delete_journal),
    path('filter', views.filter_journal_entries)
]
