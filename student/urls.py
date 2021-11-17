from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'student'
urlpatterns = [
    #path('', views.studentformView.as_view(), name="studentregister"),
    path('/', include([
        path('studentHome', views.studentHome, name="studentHome"),
        path('register', views.studentformView.as_view(), name="studentregister"),
        path('courses', views.courses.as_view(), name="courses"),
        path('addCourse', views.addCourse.as_view(), name="addCourse"),
        path('webinars', views.webinars.as_view(), name="webinars"),
        path('addWebinar', views.addWebinar.as_view(), name="addWebinar"),
        path('workshops', views.workshops.as_view(), name="workshops"),
        path('addWorkshop', views.addWorkshop.as_view(), name="addWorkshop"),
        path('competitions', views.competitions.as_view(), name="competitions"),
        path('addCompetition', views.addCompetition.as_view(), name="addCompetition"),
        path('addCompetitionCertificate', views.addCompetitionCertificate.as_view(), name="addCompetitionCertificate"),
        path('addPaper', views.addPaper.as_view(), name="addPaper"),
        path('papers', views.papers.as_view(), name="papers"),
        path('addTOEFL', views.addTOEFL.as_view(), name="addTOEFL"),
        path('addGATE', views.addGATE.as_view(), name="addGATE"),
        path('addGRE', views.addGRE.as_view(), name="addGRE"),
        path('addInternship', views.addInternship.as_view(), name="addInternship"),
        path('addStartUp', views.addStartUp.as_view(), name="addStartUp"),
        path('addPlacement', views.addPlacement.as_view(), name="addPlacement"),
        path('placement', views.placements.as_view(), name="placements"),
        path('TOEFL', views.TOEFL.as_view(), name="TOEFL"),
        path('GATE', views.GATE.as_view(), name="GATE"),
        path('GRE', views.GRE.as_view(), name="GRE"),
        path('Internship', views.internship.as_view(), name="internship"),
        path('StartUp', views.StartUp.as_view(), name="StartUp"),
        path('projects', views.projects.as_view(), name="projects"),
        path('addProject', views.addProject.as_view(), name="addProject"),
        path('PEs', views.PE.as_view(), name="PEs"),
        path('delete_items/<str:ido>/<str:pagetype>', views.delete_items, name="delete_items"),
    ])),
]
