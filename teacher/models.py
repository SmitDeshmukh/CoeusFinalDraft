from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator
from student.models import student as Student

# Create your models here.
from django.db.models import OneToOneField


class faculty(models.Model):
    user: OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    dept = models.CharField(default='CSE', max_length=10)
    # fName = models.CharField(default = 'Lionel', max_length=30)
    # lName = models.CharField(default = 'Messi', max_length=30)
    # email = models.EmailField(default = 'lionel@messi.com', max_length=50, unique=True)
    degree = models.CharField(default='Bachelors', max_length=50)
    desig = models.CharField(default='Professor', max_length=50)
    profile = models.URLField()

    def __str__(self):
        return self.user.username


#######Organized at WCE#######(VEERJA)
####Name of the submitting faculty will be displayed automatically at the start of the form.####
class wceworkshops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='kala', max_length=30)
    domain = models.CharField(default='CSE', max_length=30)
    organizer = models.CharField(default='WCE', max_length=30)
    location = models.CharField(default='Sangli', max_length=50)
    mode = models.BooleanField()  # TRUE=Inplace FALSE=Online
    role = models.CharField(default='Head', max_length=50)
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    numberOfParticipants = models.IntegerField()
    certification = models.URLField()
    certBool = models.BooleanField()
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.organizer



class wcefdp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='kala', max_length=30)
    domain = models.CharField(default='CSE', max_length=40)
    organizer = models.CharField(default='WCE', max_length=30)
    location = models.CharField(default='Sangli', max_length=50)
    mode = models.BooleanField()  # TRUE=Online FALSE=Inplace
    role = models.CharField(default='Head', max_length=50)
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    numberOfParticipants = models.IntegerField()
    certification = models.URLField()
    certBool = models.BooleanField()
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.organizer


class wcewebinars(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='kala', max_length=30)
    domain = models.CharField(default='CSE', max_length=40)
    organizer = models.CharField(default='WCE', max_length=30) #Name of Organizing College/University
    location = models.CharField(default='Sangli', max_length=50)
    mode = models.BooleanField()  # TRUE=Inplace FALSE=Online
    role = models.CharField(default='Head', max_length=50)
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    numberOfParticipants = models.IntegerField()
    certification = models.CharField(default='https://storage.googleapis.com/coeus-1482f.appspot.com/jrJHaAmxio5spt4okAh6Pi.pdf', max_length=500)
    certBool = models.BooleanField()
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.organizer


class wceconferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='No Title', max_length=100)
    domain = models.CharField(default='CSE', max_length=30)
    mode = models.BooleanField()  # TRUE=Inplace FALSE=Online
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    location = models.CharField(default='Sangli', max_length=100)
    numberOfParticipants = models.IntegerField()
    level = models.BooleanField()
    index = models.CharField(default='SCI', max_length=30)
    publicationPorR = models.BooleanField()
    publicationtype = models.CharField(default='Book Chapter', max_length=100)
    publicationSupport = models.CharField(default='IEEE', max_length=28)
    role = models.CharField(default='Head', max_length=50)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.domain


class wceguestlectures(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(default='Cyber Security', max_length=60)
    domain = models.CharField(default='CSE', max_length=50)
    resourcepersonname = models.CharField(default='NA', max_length=80)
    resourcepersonprofession = models.CharField(default='Industry', max_length=80)
    date = models.DateTimeField(default=timezone.now)
    beneficiaries = models.CharField(default='Student', max_length=30)
    numberOfParticipants = models.IntegerField()
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.topic + " " + self.domain


class wcesttp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='kala', max_length=30)
    domain = models.CharField(default='CSE', max_length=30)
    organizer = models.CharField(default='WCE', max_length=30)
    location = models.CharField(default='Sangli', max_length=50)
    mode = models.BooleanField()  # TRUE=Inplace FALSE=Online
    role = models.CharField(default='Head', max_length=50)
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    numberOfParticipants = models.IntegerField()
    certification = models.URLField()
    certBool = models.BooleanField()
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.organizer


########Submissions######## VEERJA
class subcoursebooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='Operating System', max_length=80)
    coursecode = models.CharField(default='4CS203', max_length=40)
    coursetype = models.CharField(default='Theory',
                                  max_length=25)  ##use dropdown with two selects Theory OR Laboratory##
    acaclass = models.IntegerField()  ##use a dropdown with name=first year(text to be displayed) value=1(to be sent to db) so on...##
    acayear = models.IntegerField('year', validators=[MaxValueValidator(9999)], default=datetime.datetime.now().year)
    semester = models.IntegerField()  ##use dropdown, refer to student profile for the logic
    coursebook = models.URLField()  ##the faculty is gonna upload a literal book of 60-70 pages##
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.coursecode


class subhighestdegreecerti(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    namefaculty = models.CharField(default='James Bond', max_length=50)
    namedegree = models.CharField(default='Phd', max_length=50)
    namecllg = models.CharField(default='Harvard Bussiness School', max_length=80)
    yearpassing = models.IntegerField()
    certification = models.URLField()
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.namefaculty + " " + self.namedegree


########Attended/Presented/Participated/Completed In Or Outside WCE######## VEERJA VIEWS BY KSHITIJ
####Name of the submitting faculty will be displayed automatically at the start of the form.####
class iopaper(models.Model):
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
    index = models.CharField(default='SCI', max_length=30)
    volumenumber = models.IntegerField()
    issuenumber = models.IntegerField()
    isbnissndoi = models.CharField(default='ISBN', max_length=20, unique=True)
    pagefrom = models.IntegerField()
    pageto = models.IntegerField()
    month = models.CharField(default='September', max_length=15)
    year = models.IntegerField('year', validators=[MaxValueValidator(9999)], default=datetime.datetime.now().year)
    paperurl = models.URLField(default='http://www.sciencedirect.com/science/article/pii/S0747563216304411')
    inorout = models.BooleanField(default=True)  # TRUE=in WCE FALSE=outside WCE
    coauthor = models.CharField(default="Simon Lulla", max_length=300)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.papertitle + " " + self.confname


class iofdp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='kala', max_length=30)
    organizer = models.CharField(default='WCE', max_length=30)
    location = models.CharField(default='Sangli', max_length=50)
    mode = models.BooleanField()  # TRUE=Inplace FALSE=Online
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    domain = models.CharField(default='CSE', max_length=40)
    certification = models.URLField()
    certBool = models.BooleanField()
    inorout = models.BooleanField(default=True)  # TRUE=in WCE FALSE=outside WCE
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.organizer


class ioworkshops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='kala', max_length=30)
    domain = models.CharField(default='CSE', max_length=30)
    organizer = models.CharField(default='WCE', max_length=30)
    location = models.CharField(default='Sangli', max_length=50)
    mode = models.BooleanField()  # TRUE=Online False=Offline
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    certification = models.URLField()
    certBool = models.BooleanField()
    inorout = models.BooleanField(default=True)  # TRUE=in WCE FALSE=outside WCE
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.organizer


class iowebinars(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='kala', max_length=30)
    organizer = models.CharField(default='WCE', max_length=30)
    location = models.CharField(default='Sangli', max_length=50)
    domain = models.CharField(default='CSE', max_length=40)
    mode = models.BooleanField()
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    certification = models.URLField()
    certBool = models.BooleanField()
    inorout = models.BooleanField(default=True)  # TRUE=in WCE FALSE=outside WCE
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.organizer


class iocourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='C++', max_length=30)
    domain = models.CharField(default='CSE', max_length=30)
    platform = models.CharField(default='Udemy', max_length=30)
    durationweeks = models.IntegerField(null=True, default=4)
    endDate = models.DateTimeField(default=timezone.now)
    certification = models.URLField()
    certBool = models.BooleanField()
    inorout = models.BooleanField(default=True)  # TRUE=in WCE FALSE=outside WCE
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.domain


class iosttp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default='kala', max_length=30)
    domain = models.CharField(default='CSE', max_length=30)
    organizer = models.CharField(default='WCE', max_length=30)
    location = models.CharField(default='Sangli', max_length=50)
    mode = models.BooleanField()  # TRUE=Inplace FALSE=Online
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    certification = models.URLField()
    certBool = models.BooleanField()
    inorout = models.BooleanField(default=True)  # TRUE=in WCE FALSE=outside WCE
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.name + " " + self.organizer

#######Kshitij Ends here####

###################################PE

