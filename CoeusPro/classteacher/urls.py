from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . import views
app_name = 'HOD'
urlpatterns = [
    path('/', include([
        path('ClassTeacherHome', views.ClassTeacherHome.as_view(), name="ClassTeacherHome"),
        path('addStudents', views.addStudents.as_view(), name="addStudents"),
        path('PEs', views.addPEs.as_view(), name="PEs"),
        path('viewPEs', views.viewPEs.as_view(), name="viewPEs"),
        path('delete_items/<str:ido>/<str:pagetype>', views.delete_items, name="delete_items"),
        path('assignPEs', views.assignPE.as_view(), name="assignPEs")
    ])),
]
