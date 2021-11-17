from pydoc import serve

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'CoeusPro'
namespace = 'CoeusPro'
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.home, name='home'),
                  path('login', views.login_user, name='login'),
                  path('logout', views.logout_user, name='logout'),
                  path('change_password', views.changePassword.as_view(), name="change_password"),
                  path('student', include('student.urls', namespace='student')),
                  path('faculty', include('teacher.urls', namespace='teacher')),
                  path('HOD', include('HOD.urls', namespace='HOD')),
                  path('classteacher', include('classteacher.urls', namespace='classteacher')),
                  path('profile/<str:user>', views.belongsto, name='profile'),
                  url(r'^media/(?P<path>.*)$', serve, {'document_root':       settings.MEDIA_ROOT}),
                  url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
