from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator

# Create your models here.
from django.db.models import OneToOneField


# Create your models here.

class courseexitsurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default="Operating Systems", max_length=60)
    coursecode = models.CharField(default="4CS203", max_length=25)
    courseclass = models.IntegerField(default=4, null=True)  ##Use dropdown##
    year = models.IntegerField('year', validators=[MaxValueValidator(9999)], default=datetime.datetime.now().year)
    semester = models.IntegerField(default=2, null=True)  ##Use dropdown##
    uploadcourseexitsurvey = models.URLField()
    
    def __str__(self):
        return self.name + " " + self.coursecode


class deptfeedbacksurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deptname = models.CharField(default="CSE", max_length=60)
    courseclass = models.IntegerField(default=4, null=True)  ##Use dropdown##
    year = models.IntegerField('year', validators=[MaxValueValidator(9999)], default=datetime.datetime.now().year)
    semester = models.IntegerField(default=2, null=True)
    uploaddeptexitsurvey = models.URLField()
    
    def __str__(self):
        return self.deptname + " " + self.courseclass


class gradexitsurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deptname = models.CharField(default="CSE", max_length=60)
    startYear = models.IntegerField('year', validators=[MaxValueValidator(9999)], default=datetime.datetime.now().year)
    endYear = models.IntegerField('year', validators=[MaxValueValidator(9999)], default=datetime.datetime.now().year)
    uploadgradexitsurvey = models.URLField()
    
    def __str__(self):
        return self.deptname + " " + self.startYear + "-" + self.endYear
