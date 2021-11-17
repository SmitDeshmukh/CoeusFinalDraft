from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator

# Create your models here.
from django.db.models import OneToOneField


class student(models.Model):
    user: OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    PRN = models.CharField(max_length=20, unique=True)
    dept = models.CharField(max_length=10)
    year = models.IntegerField()  # current year
    semester = models.IntegerField(default=1, null=True)
    yearOfEnrollment = models.CharField(max_length=4, default="NA")
    yearOfGraduation = models.CharField(max_length=4, default="NA.Enter after 4th year results")
    isDA = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    guideName = models.CharField(max_length=50)
    domain = models.CharField(max_length=20)
    semester = models.IntegerField(default=1, null=True)
    year = models.IntegerField('year', validators=[MaxValueValidator(9999)], default=datetime.datetime.now().year)
    socialCause = models.BooleanField(default=False)
    cause = models.CharField(max_length=50)
    customer = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title + " " + self.guideName + " " + self.domain


class startUp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    registrationNumber = models.CharField(max_length=20, default="NA")
    domain = models.CharField(max_length=20)
    supportingAgency = models.CharField(max_length=50)
    
    def __str__(self):
        return self.companyName + " " + self.domain + " " + self.supportingAgency


class placements(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=50)
    yearPlaced = models.CharField(max_length=4)
    domain = models.CharField(max_length=20)
    ctc = models.CharField(max_length=20)
    role = models.CharField(max_length=50)
    
    def __str__(self):
        return self.companyName + " " + self.yearPlaced + " " + self.role


class gate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seatNo = models.CharField(max_length=20)
    qualified = models.BooleanField(default=False)
    testDate = models.DateField(blank=True, null=True)
    marks = models.CharField(max_length=5)
    rank = models.CharField(max_length=8)
    marksheet = models.URLField()
    marksheetBool = models.BooleanField()
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.seatNo


class gre(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    regNo = models.CharField(max_length=20)
    testDate = models.DateField()
    marks = models.CharField(max_length=6)
    totalMarks = models.CharField(max_length=6)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.regNo


class toefl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    regNo = models.CharField(max_length=20)
    testDate = models.DateField()
    marks = models.CharField(max_length=6)
    totalMarks = models.CharField(max_length=6)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.regNo


class internship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=30, default="Morgan Stanley")
    startDate = models.DateField()
    endDate = models.DateField()
    certification = models.URLField()
    certBool = models.BooleanField()
    domain = models.CharField(max_length=20)
    details = models.CharField(max_length=10000)
    mode = models.BooleanField(default=True)
    # True-online and False-on-site
    internshipType = models.BooleanField(default=True)
    # lets say False for Summer and True for Winter
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.companyName



class courses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='C++', max_length=30)
    domain = models.CharField(default='CSE', max_length=30)
    platform = models.CharField(default='Udemy', max_length=30)
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    certification = models.URLField()
    certBool = models.BooleanField()
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.domain



class webinars(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='kala', max_length=30)
    organizer = models.CharField(default='WCE', max_length=30)
    location = models.CharField(default='Sangli', max_length=50)
    domain = models.CharField(default='CSE', max_length=30)
    mode = models.BooleanField()
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    certification = models.URLField()
    certBool = models.BooleanField()
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.organizer


class workshops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='kala', max_length=30)
    organizer = models.CharField(default='WCE', max_length=30)
    location = models.CharField(default='Sangli', max_length=50)
    mode = models.BooleanField()
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    certification = models.URLField()
    certBool = models.BooleanField()
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.organizer


class competitions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    compname = models.CharField(default='WCE Hackathon', max_length=50)
    organizer = models.CharField(default='Walchand College of Engineering, Sangli', max_length=60)
    location = models.CharField(default='Sangli', max_length=15)
    mode = models.BooleanField()
    projectTitle = models.CharField(default='No Title', max_length=45)
    description = models.TextField(default='No description')
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    winner = models.BooleanField()
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.compname + " " + self.organizer


class paperpublications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    papertitle = models.CharField(default='Research Paper', max_length=100)
    mode = models.BooleanField()
    confname = models.CharField(default='No Title', max_length=100)
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    location = models.CharField(default='Sangli', max_length=100)
    level = models.BooleanField()
    publicationPorR = models.BooleanField()
    publicationtype = models.CharField(default='Book Chapter', max_length=100)
    index = models.CharField(default='8888888888', max_length=30)
    volumenumber = models.IntegerField()
    issuenumber = models.IntegerField()
    isbnissndoi = models.CharField(default='ISBN', max_length=20)
    pagefrom = models.IntegerField()
    pageto = models.IntegerField()
    month = models.CharField(default='September', max_length=15)
    year = models.IntegerField('year', validators=[MaxValueValidator(9999)], default=datetime.datetime.now().year)
    paperurl = models.URLField(default='http://www.sciencedirect.com/science/article/pii/S0747563216304411')
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.papertitle + " " + self.location


class author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    papers = models.ForeignKey(paperpublications, null=True, on_delete=models.CASCADE)
    #papers = models.ForeignKey(paperpublications, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.papers.papertitle


class teamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comps = models.ForeignKey(competitions, null=True, on_delete=models.CASCADE)
    certBool = models.BooleanField(default=False)
    certification = models.URLField(default='NA')
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.comps.compname + " " + self.comps.organizer

    # associate professor
    # assistant professor
    # professer
    # hi username

    # HOD view
    # Handle Certificate Individuality
    # Handle Duplicate Competitions- could not be done
    # Add Semester and Elective in student profile for ty and final

    # delete the posts
