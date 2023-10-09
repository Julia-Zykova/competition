from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('photo_app.urls'))
]

#urlpatterns += [('django.views.static',(r'^media/(?P<path>.*)','serve',{'document_root':settings.MEDIA_ROOT}),)]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)