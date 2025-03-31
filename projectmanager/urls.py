from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projectmanagement.urls')),  # Includes all app URLs
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/',include(debug_toolbar.urls))]