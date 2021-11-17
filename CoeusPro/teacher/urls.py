from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'teacher'

urlpatterns = [

    path('/', include([
        path('facultyHome', views.facultyHome, name="facultyHome"),
        path('facultyregister', views.facultyFormView.as_view(), name="facultyregister"),
        path('editFacultyProfile', views.facultyProfileEditView.as_view(), name="editFacultyProfile"),
        path('inoroutWCE/', include([
        path('courses', views.courses.as_view(), name="courses"),
        path('addCourse', views.addCourse.as_view(), name="addCourse"),
        path('webinars', views.webinars.as_view(), name="webinars"),
        path('addWebinar', views.addWebinar.as_view(), name="addWebinar"),
        path('workshops', views.workshops.as_view(), name="workshops"),
        path('addWorkshop', views.addWorkshop.as_view(), name="addWorkshop"),
        path('addPaper', views.addPaper.as_view(), name="addPaper"),
        path('papers', views.papers.as_view(), name="papers"),
        path('addFdp', views.addFdp.as_view(), name="addFdp"),
        path('fdp', views.fdps.as_view(), name="fdps"),
        path('addSttp', views.addSttp.as_view(), name="addSttp"),
        path('sttps', views.sttps.as_view(), name="sttps"),
        path('addCourseBook', views.addCourseBook.as_view(), name="addCourseBook"),
        path('courseBooks', views.coursebooks.as_view(), name="courseBooks"),
        path('addDegree', views.addHighestDegree.as_view(), name="addDegree"),
        path('degrees', views.highestdegree.as_view(), name="degrees"),
        path('delete_itemsIO/<str:ido>/<str:pagetype>', views.delete_items, name="delete_itemsIO"),
        ])),
        ####Organized in WCE urls####
        path('WCE/', include([
        path('addWorkshop', views.addWCEWorkshop.as_view(), name="addWCEWorkshop"),
        path('Workshops', views.wceworkshops.as_view(), name="WCEWorkshops"),
        path('addFdp', views.addWCEFdp.as_view(), name="addWCEFdp"),
        path('Fdps', views.wcefdps.as_view(), name="WCEFdps"),
        path('addWebinar', views.addWCEWebinar.as_view(), name="addWCEWebinar"),
        path('Webinars', views.wcewebinars.as_view(), name="WCEWebinars"),
        path('addConference', views.addWCEConference.as_view(), name="addWCEConference"),
        path('Conferences', views.wceconferences.as_view(), name="WCEConferences"),
        path('addGL', views.addWCEGl.as_view(), name="addWCEGL"),
        path('GLs', views.wceguestlectures.as_view(), name="WCEGLs"),
        path('addSttp', views.addWCESttp.as_view(), name="addWCESttp"),
        path('Sttps', views.wcesttps.as_view(), name="WCESttps"),
        path('delete_items/<str:ido>/<str:pagetype>', views.delete_items, name="delete_items"),
        ])),

    ])),
]
