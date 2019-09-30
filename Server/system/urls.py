from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^index/$', views.index, name = 'index'),
    url(r'^print/$', views.print_, name = 'print'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

