from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_version = 'api/v1'

schema_view = get_schema_view(
   openapi.Info(
      title="Personal Journal API",
      default_version=api_version,
      description="Hello! Here you will find detailed endpoints, so I encourage you to install postman and test them out. If you have any questions, please just ping me",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path(f'{api_version}/entry/', include('entry.urls')),
    path(f'{api_version}/user/', include('user.urls'))
]
