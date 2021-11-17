from django.db import models
from student.models import student as Student


# Create your models here.

class PEs(models.Model):
    # year, sem(1, 2, 3, 4, 5, 6), courseName, courseCode, acadYear(SE, TE, BE)
    year = models.IntegerField()  # 2020 2021
    sem = models.IntegerField(default=1, null=True)
    courseName = models.CharField(default='FLAT', max_length=100)
    courseCode = models.CharField(default='4CS101', max_length=20, unique=True)
    acadYear = models.IntegerField()  # SE TE BE
    
    def __str__(self):
        return self.courseName + " " + self.courseCode + " " + str(self.year) + " " + str(self.sem)


class PETakenByStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    PE = models.ForeignKey(PEs, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.student.user.first_name + " " + self.student.user.last_name + " " + self.PE.courseName + " " + self.PE.courseCode
