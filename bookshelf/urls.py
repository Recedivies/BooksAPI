from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Books API",
        default_version='v1',
        description="Modified Books API as a requirement task for Dicoding",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
        authentication_classes='rest_framework_simplejwt.authentication.JWTAuthentication'
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/auth/', include('authorization.urls')),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
