from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from main.views import TrackViewSet, GenreViewSet

schema_view = get_schema_view(
    openapi.Info(
        title='Spotify Api',
        description='spotify',
        default_version='v1'
    ),
    public=True
)

router = DefaultRouter()
router.register('tracks', TrackViewSet, 'tracks')
router.register('genres', GenreViewSet, 'genres')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/docs/', schema_view.with_ui('swagger')),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
