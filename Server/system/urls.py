from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^index/$', views.index, name = 'index'),
    url(r'^print/$', views.print_, name = 'print'),
    url(r'^handle/$', views.handle, name = 'handle'),
    url(r'^get_history/$', views.get_history, name = 'get_history'),
    url(r'^check_user/$', views.check_user, name = 'check_user'),
    url(r'^register_user/$', views.register_user, name = 'register_user'),
    url(r'^get_current_result/$', views.get_current_result, name = 'get_current_result'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

