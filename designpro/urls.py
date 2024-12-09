from django.contrib import admin
from django.urls import include
from django.urls import path
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AppDesign.urls', namespace='catalog')),
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
