from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('postsite.urls')),
    path('user/', include('user.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found