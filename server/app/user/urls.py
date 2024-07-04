from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.create_account),
    path('login', views.login),
    path('validate_token', views.validate_token),
    path('update_profile', views.update_profile)
]
