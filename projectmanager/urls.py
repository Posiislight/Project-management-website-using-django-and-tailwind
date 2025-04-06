from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from django.http import HttpResponse

def home(request):
    return HttpResponse("🎉 Hello from Django on Railway!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projectmanagement.urls')),  # Includes all app URLs
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/',include(debug_toolbar.urls))]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
