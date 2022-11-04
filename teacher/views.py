import os
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic.base import View
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.base import View
from teacher.models import iocourses as Coursera
from teacher.models import iowebinars as Webi
from teacher.models import ioworkshops as Work
from teacher.models import iopaper as Paper
from teacher.models import faculty as Faculty
from teacher.models import iofdp as FDP
from teacher.models import iosttp as STTP
from teacher.models import subcoursebooks as CourseBook
from teacher.models import subhighestdegreecerti as Degree
from teacher.models import wceworkshops as WCEWork
from teacher.models import wcefdp as WCEFdp
from teacher.models import wcewebinars as WCEWebinar
from teacher.models import wceconferences as WCEConference
from teacher.models import wceguestlectures as WCEGL
from teacher.models import wcesttp as WCESttp
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
import shortuuid
import requests
import json

# if group == 'student_group':
#     return render(request, 'student/home.html', {'student': userr, user: user})
# if group == 'HOD_group':
#     return render(request, 'HOD/HODhome.html', {'HOD': userr, user:user})

def getFileUploadLink(file):
    site = 'https://asia-south1-coeus-1482f.cloudfunctions.net/api/upload-file'
    up = {'file':(file.name, file.read(), "multipart/form-data")}
    resp = requests.post(site, files=up).json()
    return resp['link']

def isFaculty(group_name):
    if group_name == 'faculty_group':
        return 1
    else:
        return 0


def isNotFaculty(group_name):
    if group_name == 'faculty_group':
        return False
    else:
        return True


def facultyHome(request):
    group = request.user.groups.all()[0].name
    if isFaculty(group) == 0:
        return render(request, 'login.html')
    else:
        return render(request, 'teacher/facultyHome.html', {})


class facultyFormView(View):

    def get(self, request, template_name='teacher/facreg.html'):
        return render(request, template_name)

    def post(self, request, template_name='teacher/facreg.html'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department = request.POST.get('dept')
        confPassword = request.POST.get('conf_password')
        degree = request.POST.get('degree')
        desig = request.POST.get('designation')

        if confPassword != password:
            err = {'error_message': "Passwords don't match. Please Try Again."}
            return render(request, 'teacher/facreg.html', err)

        try:
            user = User.objects.create_user(username, email, password, first_name=first_name,
                                            last_name=last_name, )
            user.save()
        except:
            messages.warning(request, 'Account with this Username or Email Already Exists.')
            return render(request, template_name)

        profile = request.FILES['profile']
        url = getFileUploadLink(profile)

        facultyData = Faculty(user=user, dept=department, degree=degree, profile=url, desig=desig)
        facultyData.save()

        my_group = Group.objects.get(name='faculty_group')
        my_group.user_set.add(user)

        messages.success(request, 'Registration Successful. Please Login.')
        return render(request, template_name)


# Edit Profile for Faculty
class facultyProfileEditView(View):

    def get(self, request, template_name='teacher/facultyProfileEdit.html'):
        # user = request.user
        # teacher = Faculty.objects.get(user=user)
        # args = {}
        # args["teacher"] = teacher
        return render(request, template_name)

    def post(self, request, template_name='teacher/facultyProfileEdit.html'):
        user = request.user
        #teacher = Faculty.objects.get(user=user)
        teacher = user.faculty
        # password = request.POST.get('password')
        # email = request.POST.get('email')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        department = request.POST.get('dept')
        # confPassword = request.POST.get('conf_password')
        degree = request.POST.get('degree')
        desig = request.POST.get('designation')
        fs = FileSystemStorage()
        if not bool(request.FILES.get('profile', False)):
            url = request.user.faculty.profile
        else:
            profile = request.FILES['profile']
            url = getFileUploadLink(profile)
        try:
            teacher.dept = department
            teacher.degree = degree
            teacher.desig = desig
            teacher.profile = url
            teacher.save()
            #my_group = Group.objects.get(name='faculty_group')
            #my_group.user_set.add(teacher)
        except:
            messages.warning(request, 'Update Unsuccessful.')
            return render(request, template_name)
        messages.success(request, 'Profile Updated Successfully.')
        return render(request, template_name)

##Views for in or out of WCE##
class papers(View):
    def get(self, request, template_name='teacher/attendedActivities/papers.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allPapers = Paper.objects.filter(user=user)
                countPapers = len(allPapers)
                for i in allPapers:
                    mates = i.coauthor
                    mates = mates.split("$$$")
                    matees = ""
                    for j in range(len(mates)):
                        matees += mates[j]
                        if j == len(mates) - 1:
                            matees += "."
                        else:
                            matees += ", "
                    i.coauthor = matees
            except:
                allPapers = None
                countPapers = 0
            args = {}
            args["allPapers"] = allPapers
            args["countPapers"] = countPapers
            return render(request, template_name, args)




class addPaper(View):
    def get(self, request, template_name='teacher/attendedActivities/addPaper.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/attendedActivities/addPaper.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            user = request.user
            papertitle = request.POST.get('papertitle')
            if request.POST.get('mode') == "Online":
                mode = True
            else:
                mode = False
            confname = request.POST.get('confname')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            location = request.POST.get('location')
            if request.POST.get('level') == "International":
                level = True
            else:
                level = False
            if request.POST.get('publicationPorR') == "Peered-reviewed":
                publicationPorR = True
            else:
                publicationPorR = False
            publicationtype = request.POST.get('publicationtype')
            index = request.POST.get('index')
            volumenumber = request.POST.get('volumenumber')
            issuenumber = request.POST.get('issuenumber')
            isbnissndoi = request.POST.get('isbnissndoi')
            pagefrom = request.POST.get('pagefrom')
            pageto = request.POST.get('pageto')
            month = request.POST.get('month')
            year = request.POST.get('year')
            paperurl = request.POST.get('paperurl')
            coauthor = request.POST.get('allMates')
            if request.POST.get('inorout') == "In WCE":
                inorout = True
            else:
                inorout = False
            try:
                publishPaper = Paper(user=user, papertitle=papertitle, mode=mode, confname=confname,
                                     startDate=startDate,
                                     endDate=endDate, location=location,
                                     level=level, publicationPorR=publicationPorR, publicationtype=publicationtype,
                                     index=index,
                                     volumenumber=volumenumber, inorout=inorout, coauthor=coauthor,
                                     issuenumber=issuenumber, isbnissndoi=isbnissndoi, pagefrom=pagefrom, pageto=pageto,
                                     month=month, year=year, paperurl=paperurl)
                publishPaper.save()
            except:
                err = {}
                err['error_message'] = "You have already uploaded this Paper."
                return render(request, template_name, err)

            # To Do: How to add authors for Faculty

            err = {'error_message': "Paper Added Successfully."}

            # allMates = request.POST.get('allMates')
            # allMates = allMates.rstrip()
            # allMates = allMates.lstrip()
            # allMates = allMates.split()

            # start adding all teammates with the associated competition
            # currentPaper = publishPaper
            # # add the adder
            # adder = Author(user=user, papers=currentPaper)
            # adder.save()
            # # add other team-mates
            # try:
            #     for mate in allMates:
            #         # get User Obj of mate: PNR
            #         mate = mate.upper()
            #         matePerson = Faculty.objects.filter(PRN=mate)
            #         matePerson = matePerson[0]
            #         matePerson = matePerson.user
            #         addMate = Author(user=matePerson, papers=currentPaper)
            #         addMate.save()

            # except:
            #     err = {'error_message': "Entered PRNs of Co-Authors are Incorrect."}
            # print(allMates)
            return render(request, template_name, err)


########################################################################################################################

class courses(View):
    def get(self, request, template_name='teacher/attendedActivities/courses.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allCourses = Coursera.objects.filter(user=user)
                countCourses = len(allCourses)
            except:
                allCourses = None
                countCourses = 0
            args = {}
            args["allCourses"] = allCourses
            args["countCourses"] = countCourses
            return render(request, template_name, args)




class addCourse(View):
    def get(self, request, template_name='teacher/attendedActivities/addCourse.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/attendedActivities/addCourse.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            user = request.user
            name = request.POST.get('name')
            domain = request.POST.get('domain')
            platform = request.POST.get('platform')
            durationweeks = request.POST.get('durationweeks')  # In weeks
            endDate = request.POST.get('endDate')
            if request.POST.get('inorout') == "In WCE":
                inorout = True
            else:
                inorout = False

            try:
                certBool = True
                certification = request.FILES['certification']
                certification = getFileUploadLink(certification)
                publishCourse = Coursera(name=name, domain=domain, platform=platform, inorout=inorout,
                                         durationweeks=durationweeks,
                                         endDate=endDate,
                                         user=user, certification=certification, certBool=certBool)
                publishCourse.save()

            except:
                certification = "NA"
                certBool = False
                publishCourse = Coursera(name=name, domain=domain, platform=platform, inorout=inorout,
                                         durationweeks=durationweeks,
                                         endDate=endDate,
                                         user=user, certification=certification, certBool=certBool)
                publishCourse.save()

            err = {'error_message': "Course Added Successfully."}
            return render(request, template_name, err)


########################################################################################################################

class webinars(View):
    def get(self, request, template_name='teacher/attendedActivities/webinars.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allWebinars = Webi.objects.filter(user=user)
                countWebinars = len(allWebinars)
            except:
                allWebinars = None
                countWebinars = 0
            args = {}
            args["allWebinars"] = allWebinars
            args["countWebinars"] = countWebinars
            return render(request, template_name, args)

class addWebinar(View):
    def get(self, request, template_name='teacher/attendedActivities/addWebinar.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/attendedActivities/addWebinar.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            name = request.POST.get('name')
            organizer = request.POST.get('organizer')
            location = request.POST.get('location')
            if (request.POST.get('mode') == "Online"):
                mode = True
            else:
                mode = False
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            user = request.user
            if (request.POST.get('inorout') == "In WCE"):
                inorout = True
            else:
                inorout = False
            domain = request.POST.get('domain')

            try:
                certBool = True
                certification = request.FILES['certification']
                certification = getFileUploadLink(certification)
                
                publishWebinar = Webi(name=name, organizer=organizer, location=location, mode=mode, startDate=startDate,
                                    endDate=endDate, domain=domain, user=user, inorout=inorout,
                                    certification=certification, certBool=certBool)
                publishWebinar.save()

            except:
                certification = "NA"
                certBool = False
                publishWebinar = Webi(name=name, organizer=organizer, location=location, mode=mode, startDate=startDate,
                                      endDate=endDate, domain=domain, user=user, inorout=inorout,
                                      certification=certification, certBool=certBool)
                publishWebinar.save()

            err = {"error_message": "Webinar Added Successfully."}
            return render(request, template_name, err)


########################################################################################################################

class workshops(View):
    def get(self, request, template_name='teacher/attendedActivities/workshops.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allWorkshops = Work.objects.filter(user=user)
                countWorkshops = len(allWorkshops)
            except:
                allWorkshops = None
                countWorkshops = 0
            args = {}
            args["allWorkshops"] = allWorkshops
            args["countWorkshops"] = countWorkshops
            return render(request, template_name, args)




class addWorkshop(View):
    def get(self, request, template_name='teacher/attendedActivities/addWorkshop.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/attendedActivities/addWorkshop.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            user = request.user
            name = request.POST.get('name')
            organizer = request.POST.get('organizer')
            location = request.POST.get('location')
            domain = request.POST.get('domain')
            if request.POST.get('mode') == "Online":
                mode = True
            else:
                mode = False
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')

            if request.POST.get('inorout') == "In WCE":
                inorout = True
            else:
                inorout = False
            try:
                certBool = True
                certification = request.FILES['certification']
                certification = getFileUploadLink(certification)
                publishWorkshop = Work(name=name, organizer=organizer, location=location, mode=mode,
                                       startDate=startDate,
                                       endDate=endDate, user=user, domain=domain, inorout=inorout,
                                       certification=certification, certBool=certBool)
                publishWorkshop.save()

            except:
                certification = "NA"
                certBool = False
                publishWorkshop = Work(name=name, organizer=organizer, location=location, mode=mode,
                                       startDate=startDate,
                                       endDate=endDate, user=user, domain=domain, inorout=inorout,
                                       certification=certification, certBool=certBool)
                publishWorkshop.save()

            err = {'error_message': "Workshop Added Successfully."}
            return render(request, template_name, err)


############# FDP VEERJA##############
# 1) Name of FDP
# 2) Name of Organizing College/University
# 3) Place
# 4) Mode of Participation (online or In Person)
# 5) Duration (start date, end date)
# 6) Domain of FDP
# 7) Certification (yes or no)
# 8) Upload Certificate

class fdps(View):
    def get(self, request, template_name='teacher/attendedActivities/fdps.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allFdps = FDP.objects.filter(user=user)
                countFdps = len(allFdps)
            except:
                allFdps = None
                countFdps = 0
            args = {}
            args["allFdps"] = allFdps
            args["countFdps"] = countFdps
            return render(request, template_name, args)




class addFdp(View):
    def get(self, request, template_name='teacher/attendedActivities/addFdp.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/attendedActivities/addFdp.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            user = request.user
            name = request.POST.get('name')
            organizer = request.POST.get('organizer')
            location = request.POST.get('location')
            domain = request.POST.get('domain')
            if (request.POST.get('mode') == "Online"):
                mode = True
            else:
                mode = False
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')

            if (request.POST.get('inorout') == "In WCE"):
                inorout = True
            else:
                inorout = False
            try:
                certBool = True
                certification = request.FILES['certification']
                certification = getFileUploadLink(certification)
                publishFdp = FDP(name=name, organizer=organizer, location=location, mode=mode, startDate=startDate,
                                 endDate=endDate, user=user, domain=domain, inorout=inorout,
                                 certification=certification, certBool=certBool)
                publishFdp.save()

            except:
                certification = "NA"
                certBool = False
                publishFdp = FDP(name=name, organizer=organizer, location=location, mode=mode, startDate=startDate,
                                 endDate=endDate, user=user, domain=domain, inorout=inorout,
                                 certification=certification, certBool=certBool)
                publishFdp.save()

            err = {'error_message': "FDP Added Successfully."}
            return render(request, template_name, err)


###### STTP VEERJA ####
# 1) Name of STTP
# 2) Name of Organizing College/University
# 3) Place
# 4) Mode of Participation (online or In Person)
# 5) Duration (start date, end date)
# 6) Domain of Workshop
# 7) Certification (yes or no)
# 8) Upload Certificate
class sttps(View):
    def get(self, request, template_name='teacher/attendedActivities/sttps.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allSttps = STTP.objects.filter(user=user)
                countSttps = len(allSttps)
            except:
                allSttps = None
                countSttps = 0
            args = {}
            args["allSttps"] = allSttps
            args["countSttps"] = countSttps
            return render(request, template_name, args)


class addSttp(View):
    def get(self, request, template_name='teacher/attendedActivities/addSttp.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/attendedActivities/addSttp.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            user = request.user
            name = request.POST.get('name')
            organizer = request.POST.get('organizer')
            location = request.POST.get('location')
            domain = request.POST.get('domain')
            if (request.POST.get('mode') == "Online"):
                mode = True
            else:
                mode = False
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')

            if (request.POST.get('inorout') == "In WCE"):
                inorout = True
            else:
                inorout = False
            try:
                certBool = True
                certification = request.FILES['certification']
                certification = getFileUploadLink(certification)
                publishSttp = STTP(name=name, organizer=organizer, location=location, mode=mode, startDate=startDate,
                                   endDate=endDate, user=user, domain=domain, inorout=inorout,
                                   certification=certification, certBool=certBool)
                publishSttp.save()

            except:
                certification = "NA"
                certBool = False
                publishSttp = STTP(name=name, organizer=organizer, location=location, mode=mode, startDate=startDate,
                                   endDate=endDate, user=user, domain=domain, inorout=inorout,
                                   certification=certification, certBool=certBool)
                publishSttp.save()

            err = {'error_message': "STTP Added Successfully."}
            return render(request, template_name, err)


####Faculty Submissions####
class coursebooks(View):
    def get(self, request, template_name='teacher/submissions/coursebooks.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allCourseBooks = CourseBook.objects.filter(user=user)
                countCourseBooks = len(allCourseBooks)
            except:
                allCourseBooks = None
                countCourseBooks = 0
            args = {}
            args["allCourseBooks"] = allCourseBooks
            args["countCourseBooks"] = countCourseBooks
            return render(request, template_name, args)

####Submissions VEERJA####
# CourseBooks
class addCourseBook(View):
    def get(self, request, template_name='teacher/submissions/addCourseBook.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/submissions/addCourseBook.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            user = request.user
            name = request.POST.get('name')
            coursecode = request.POST.get('coursecode')
            coursetype = request.POST.get('coursetype')  ##use dropdown with two selects Theory OR Laboratory##
            acaclass = request.POST.get(
                'acaclass')  ##use a dropdown with name=first year(text to be displayed) value=1(to be sent to db) so on...#
            acayear = request.POST.get('acayear')
            semester = request.POST.get('semester')  ##use dropdown, refer to student profile for the logic
            try:
                coursebook = request.FILES['coursebook']
                coursebook = getFileUploadLink(coursebook)
                publishCourseBook = CourseBook(name=name, coursecode=coursecode, coursetype=coursetype,
                                               acaclass=acaclass,
                                               acayear=acayear,
                                               user=user, semester=semester, coursebook=coursebook)
                publishCourseBook.save()

            except:
                coursebook = "NA"
                publishCourseBook = CourseBook(name=name, coursecode=coursecode, coursetype=coursetype,
                                               acaclass=acaclass,
                                               acayear=acayear, user=user, semester=semester, coursebook=coursebook)
                publishCourseBook.save()

            err = {'error_message': "Course Book Added Successfully."}
            return render(request, template_name, err)


# Highest Degree
class highestdegree(View):
    def get(self, request, template_name='teacher/submissions/degrees.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allDegrees = Degree.objects.filter(user=user)
                countDegrees = len(allDegrees)
            except:
                allDegrees = None
                countDegrees = 0
            args = {}
            args["allDegrees"] = allDegrees
            args["countDegrees"] = countDegrees
            return render(request, template_name, args)




class addHighestDegree(View):
    def get(self, request, template_name='teacher/submissions/addDegree.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/submissions/addDegree.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            user = request.user
            namefaculty = request.POST.get('namefaculty')
            namedegree = request.POST.get('namedegree')
            namecllg = request.POST.get('namecllg')
            yearpassing = request.POST.get(
                'yearpassing')  ##use a dropdown and use the year dropdown logic we used for year paper
            try:
                certBool = True
                certification = request.FILES['certification']
                certification = getFileUploadLink(certification)
                publishDegree = Degree(user=user, namefaculty=namefaculty, namedegree=namedegree, namecllg=namecllg,
                                       yearpassing=yearpassing, certification=certification)
                publishDegree.save()

            except:
                err = {'error_message': "Couldn't Upload Certificate. Try Again"}
                return render(request, template_name, err)

            err = {'error_message': "Degree Added Successfully."}
            return render(request, template_name, err)


########################################################################################################################
####IMP NOTE: Note: Name of the submitting faculty will be displayed automatically at the start of the
#####form.
####Views for Organized at WCE VEERJA#################

# workshops in WCE
class wceworkshops(View):
    def get(self, request, template_name='teacher/organizedActivities/wceworkshops.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allWCEWorkshops = WCEWork.objects.filter(user=user)
                countWCEWorkshops = len(allWCEWorkshops)
            except:
                allWCEWorkshops = None
                countWCEWorkshops = 0
            args = {}
            args["allWCEWorkshops"] = allWCEWorkshops
            args["countWCEWorkshops"] = countWCEWorkshops
            return render(request, template_name, args)



class addWCEWorkshop(View):
    def get(self, request, template_name='teacher/organizedActivities/addWCEWorkshop.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/organizedActivities/addWCEWorkshop.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            user = request.user
            name = request.POST.get('name')
            organizer = request.POST.get('organizer')
            location = request.POST.get('location')
            domain = request.POST.get('domain')
            role = request.POST.get('role')
            numberOfParticipants = request.POST.get('numberOfParticipants')
            if request.POST.get('mode') == "Online":
                mode = True
            else:
                mode = False
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')

            try:
                certBool = True
                certification = request.FILES['certification']
                certification = getFileUploadLink(certification)
                publishWCEWorkshop = WCEWork(name=name, organizer=organizer, location=location, mode=mode,
                                             startDate=startDate,
                                             endDate=endDate, user=user, domain=domain, role=role,
                                             numberOfParticipants=numberOfParticipants,
                                             certification=certification, certBool=certBool)
                publishWCEWorkshop.save()

            except:
                certification = "NA"
                certBool = False
                publishWCEWorkshop = WCEWork(name=name, organizer=organizer, location=location, mode=mode,
                                             startDate=startDate,
                                             endDate=endDate, user=user, domain=domain, role=role,
                                             numberOfParticipants=numberOfParticipants,
                                             certification=certification, certBool=certBool)
                publishWCEWorkshop.save()

            err = {'error_message': "Workshop Organized in WCE Added Successfully."}
            return render(request, template_name, err)


# FDPs in WCE
class wcefdps(View):
    def get(self, request, template_name='teacher/organizedActivities/wcefdps.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allWCEFdps = WCEFdp.objects.filter(user=user)
                countWCEFdps = len(allWCEFdps)
            except:
                allWCEFdps = None
                countWCEFdps = 0
            args = {}
            args["allWCEFdps"] = allWCEFdps
            args["countWCEFdps"] = countWCEFdps
            return render(request, template_name, args)

class addWCEFdp(View):
    def get(self, request, template_name='teacher/organizedActivities/addWCEFdp.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/organizedActivities/addWCEFdp.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            user = request.user
            name = request.POST.get('name')
            organizer = request.POST.get('organizer')
            location = request.POST.get('location')
            domain = request.POST.get('domain')
            role = request.POST.get('role')
            numberOfParticipants = request.POST.get('numberOfParticipants')
            if request.POST.get('mode') == "Online":
                mode = True
            else:
                mode = False
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')

            try:
                certBool = True
                certification = request.FILES['certification']
                certification = getFileUploadLink(certification)
                publishWCEFdp = WCEFdp(name=name, organizer=organizer, location=location, mode=mode,
                                       startDate=startDate,
                                       endDate=endDate, user=user, domain=domain, role=role,
                                       numberOfParticipants=numberOfParticipants,
                                       certification=certification, certBool=certBool)
                publishWCEFdp.save()

            except:
                certification = "NA"
                certBool = False
                publishWCEFdp = WCEFdp(name=name, organizer=organizer, location=location, mode=mode,
                                       startDate=startDate,
                                       endDate=endDate, user=user, domain=domain, role=role,
                                       numberOfParticipants=numberOfParticipants,
                                       certification=certification, certBool=certBool)
                publishWCEFdp.save()

            err = {'error_message': "Faculty Development Programme Organized in WCE Added Successfully."}
            return render(request, template_name, err)


# webinars in wce
class wcewebinars(View):
    def get(self, request, template_name='teacher/organizedActivities/wcewebinars.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allWCEWebinars = WCEWebinar.objects.filter(user=user)
                countWCEWebinars = len(allWCEWebinars)
            except:
                allWCEWebinars = None
                countWCEWebinars = 0
            args = {}
            args["allWCEWebinars"] = allWCEWebinars
            args["countWCEWebinars"] = countWCEWebinars
            return render(request, template_name, args)

class addWCEWebinar(View):
    def get(self, request, template_name='teacher/organizedActivities/addWCEWebinar.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/organizedActivities/addWCEWebinar.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            user = request.user
            name = request.POST.get('name')
            organizer = request.POST.get('organizer')  # Name of Organizing College/University
            location = request.POST.get('location')
            domain = request.POST.get('domain')
            role = request.POST.get('role')
            numberOfParticipants = request.POST.get('numberOfParticipants')
            if request.POST.get('mode') == "Online":
                mode = True
            else:
                mode = False
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')

            try:
                certBool = True
                certification = request.FILES['certification']
                certification = getFileUploadLink(certification)
                publishWCEWebinar = WCEWebinar(name=name, organizer=organizer, location=location, mode=mode,
                                               startDate=startDate,
                                               endDate=endDate, user=user, domain=domain, role=role,
                                               numberOfParticipants=numberOfParticipants,
                                               certification=certification, certBool=certBool)
                publishWCEWebinar.save()

            except:
                certification = "NA"
                certBool = False
                publishWCEWebinar = WCEWebinar(name=name, organizer=organizer, location=location, mode=mode,
                                               startDate=startDate,
                                               endDate=endDate, user=user, domain=domain, role=role,
                                               numberOfParticipants=numberOfParticipants,
                                               certification=certification, certBool=certBool)
                publishWCEWebinar.save()

            err = {'error_message': "Webinar Organized in WCE Added Successfully."}
            return render(request, template_name, err)


## Conferences organized in WCE ##

class wceconferences(View):
    def get(self, request, template_name='teacher/organizedActivities/wceconferences.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allWCEConferences = WCEConference.objects.filter(user=user)
                countWCEConferences = len(allWCEConferences)
            except:
                allWCEConferences = None
                countWCEConferences = 0
            args = {}
            args["allWCEConferences"] = allWCEConferences
            args["countWCEConferences"] = countWCEConferences
            return render(request, template_name, args)

class addWCEConference(View):
    def get(self, request, template_name='teacher/organizedActivities/addWCEConference.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/organizedActivities/addWCEConference.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            user = request.user
            name = request.POST.get('name')
            domain = request.POST.get('domain')
            if request.POST.get('mode') == "Online":
                mode = True
            else:
                mode = False
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            location = request.POST.get('location')
            numberOfParticipants = request.POST.get('numberOfParticipants')
            if request.POST.get('level') == "International":
                level = True
            else:
                level = False
            index = request.POST.get('index')
            if request.POST.get('publicationPorR') == "Peered-reviewed":
                publicationPorR = True
            else:
                publicationPorR = False
            publicationtype = request.POST.get('publicationtype')
            publicationSupport = request.POST.get('publicationSupport')
            role = request.POST.get('role')
            publishWCEConference = WCEConference(user=user, name=name, domain=domain, mode=mode, startDate=startDate,
                                                 endDate=endDate,
                                                 location=location, numberOfParticipants=numberOfParticipants,
                                                 level=level,
                                                 index=index,
                                                 publicationPorR=publicationPorR, publicationtype=publicationtype,
                                                 publicationSupport=publicationSupport, role=role)
            publishWCEConference.save()
            err = {'error_message': "Conference/Symposium Organized in WCE Added Successfully."}
            return render(request, template_name, err)


##Guest Lectures organized in WCE
class wceguestlectures(View):
    def get(self, request, template_name='teacher/organizedActivities/wcegls.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allWCEGLs = WCEGL.objects.filter(user=user)
                countWCEGLs = len(allWCEGLs)
            except:
                allWCEGLs = None
                countWCEGLs = 0
            args = {}
            args["allWCEGLs"] = allWCEGLs
            args["countWCEGLs"] = countWCEGLs
            return render(request, template_name, args)




class addWCEGl(View):
    def get(self, request, template_name='teacher/organizedActivities/addWCEGL.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/organizedActivities/addWCEGL.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            user = request.user
            topic = request.POST.get('topic')
            domain = request.POST.get('domain')
            resourcepersonname = request.POST.get('resourcepersonname')
            resourcepersonprofession = request.POST.get('resourcepersonprofession')
            date = request.POST.get('date')
            beneficiaries = request.POST.get(
                'beneficiaries')  # Use dropdown with 3 selects Students, Faculty, Non-teaching
            numberOfParticipants = request.POST.get('numberOfParticipants')
            publishGL = WCEGL(user=user, topic=topic, domain=domain, resourcepersonname=resourcepersonname,
                              resourcepersonprofession=resourcepersonprofession, date=date, beneficiaries=beneficiaries,
                              numberOfParticipants=numberOfParticipants)
            publishGL.save()
            err = {'error_message': "Guest Lecture Organized in WCE Added Successfully."}
            return render(request, template_name, err)

    ## STTP organized in WCE ##


class wcesttps(View):
    def get(self, request, template_name='teacher/organizedActivities/wcesttps.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                allWCESttps = WCESttp.objects.filter(user=user)
                countWCESttps = len(allWCESttps)
            except:
                allWCESttps = None
                countWCESttps = 0
            args = {}
            args["allWCESttps"] = allWCESttps
            args["countWCESttps"] = countWCESttps
            return render(request, template_name, args)

class addWCESttp(View):
    def get(self, request, template_name='teacher/organizedActivities/addWCESttp.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='teacher/organizedActivities/addWCESttp.html'):
        group = request.user.groups.all()[0].name
        if isFaculty(group) == 0:
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            user = request.user
            name = request.POST.get('name')
            domain = request.POST.get('domain')
            organizer = request.POST.get('organizer')
            location = request.POST.get('location')
            if (request.POST.get('mode') == "Online"):
                mode = True
            else:
                mode = False
            role = request.POST.get('role')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            numberOfParticipants = request.POST.get('numberOfParticipants')
            try:
                certBool = True
                certification = request.FILES['certification']
                certification = getFileUploadLink(certification)
                publishWCESttp = WCESttp(name=name, organizer=organizer, location=location, mode=mode,
                                         startDate=startDate,
                                         endDate=endDate, user=user, domain=domain, role=role,
                                         numberOfParticipants=numberOfParticipants,
                                         certification=certification, certBool=certBool)
                publishWCESttp.save()

            except:
                certification = "NA"
                certBool = False
                publishWCESttp = WCESttp(name=name, organizer=organizer, location=location, mode=mode,
                                         startDate=startDate,
                                         endDate=endDate, user=user, domain=domain, role=role,
                                         numberOfParticipants=numberOfParticipants,
                                         certification=certification, certBool=certBool)
                publishWCESttp.save()

            err = {'error_message': "STTP Added Successfully."}
            return render(request, template_name, err)


def delete_items(request, ido, pagetype):
    if request.method == 'POST':
        if pagetype == "courseBooks":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:

                thatCourseBook = CourseBook.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "CourseBook Deleted Successfully"
                try:
                    user = request.user
                    allCourseBooks = CourseBook.objects.filter(user=user)
                    countCourseBooks = len(allCourseBooks)
                except:
                    allCourseBooks = None
                    countCourseBooks = 0
                args = {}
                args["allCourseBooks"] = allCourseBooks
                args["countCourseBooks"] = countCourseBooks
                return redirect('../../courseBooks')

        elif pagetype == "degrees":

            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:
                thatDegree = Degree.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "Degree Deleted Successfully"
                try:
                    user = request.user
                    allDegrees = Degree.objects.filter(user=user)
                    countDegrees = len(allDegrees)
                except:
                    allDegrees = None
                    countDegrees = 0
                args = {}
                args["allDegrees"] = allDegrees
                args["countDegrees"] = countDegrees
                return redirect('../../degrees')

        elif pagetype == "courses":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:

                thatCourse = Coursera.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "Course Deleted Successfully"
                try:
                    user = request.user
                    allCourses = Coursera.objects.filter(user=user)
                    countCourses = len(allCourses)
                except:
                    allCourses = None
                    countCourses = 0
                args = {}
                args["allCourses"] = allCourses
                args["countCourses"] = countCourses
                return redirect('../../courses')

        elif pagetype == "fdp":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:

                thatFDP = FDP.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "FDP Deleted Successfully"
                try:
                    user = request.user
                    allFDPs = FDP.objects.filter(user=user)
                    countFDPs = len(allFDPs)
                except:
                    allFDPs = None
                    countFDPs = 0
                args = {}
                args["allFDPs"] = allFDPs
                args["countFDPs"] = countFDPs
                return redirect('../../fdp')

        elif pagetype == "papers":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:

                thatPaper = Paper.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "Paper Deleted Successfully"
                try:
                    user = request.user
                    allPapers = Paper.objects.filter(user=user)
                    countPapers = len(allPapers)
                    for i in allPapers:
                        mates = i.coauthor
                        mates = mates.split("$$$")
                        matees = ""
                        for j in range(len(mates)):
                            matees += mates[j]
                            if j == len(mates) - 1:
                                matees += "."
                            else:
                                matees += ", "
                        i.coauthor = matees
                except:
                    allPapers = None
                    countPapers = 0
                args = {}
                args["allPapers"] = allPapers
                args["countPapers"] = countPapers
                return redirect('../../papers')

        elif pagetype == "sttps":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:
                thatSttp = STTP.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "Sttp Deleted Successfully"
                try:
                    user = request.user
                    allSttps = STTP.objects.filter(user=user)
                    countSttps = len(allSttps)
                except:
                    allSttps = None
                    countSttps = 0
                args = {}
                args["allSttps"] = allSttps
                args["countSttps"] = countSttps
                return redirect('../../sttps')

        elif pagetype == "webinars":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:
                thatWebinar = Webi.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "Webinar Deleted Successfully"
                try:
                    user = request.user
                    allWebinars = Webi.objects.filter(user=user)
                    countWebinars = len(allWebinars)
                except:
                    allWebinars = None
                    countWebinars = 0
                args = {}
                args["allWebinars"] = allWebinars
                args["countWebinars"] = countWebinars
                return redirect('../../webinars')

        elif pagetype == "workshops":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:
                thatWorkshop = Work.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "Workshop Deleted Successfully"
                try:
                    user = request.user
                    allWorkshops = Work.objects.filter(user=user)
                    countWorkshops = len(allWorkshops)
                except:
                    allWorkshops = None
                    countWorkshops = 0
                args = {}
                args["allWorkshops"] = allWorkshops
                args["countWorkshops"] = countWorkshops
                return redirect('../../workshops')

        elif pagetype == "Conferences":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:
                thatWCEConference = WCEConference.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "WCE Conference Deleted Successfully"
                try:
                    user = request.user
                    allWCEConferences = WCEConference.objects.filter(user=user)
                    countWCEConferences = len(allWCEConferences)
                except:
                    allWCEConferences = None
                    countWCEConferences = 0
                args = {}
                args["allWCEConferences"] = allWCEConferences
                args["countWCEConferences"] = countWCEConferences
                return redirect('../../Conferences')

        elif pagetype == "Fdps":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:
                thatWCEFdp = WCEFdp.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "WCE Fdp Deleted Successfully"
                try:
                    user = request.user
                    allWCEFdps = WCEFdp.objects.filter(user=user)
                    countWCEFdps = len(allWCEFdps)
                except:
                    allWCEFdps = None
                    countWCEFdps = 0
                args = {}
                args["allWCEFdps"] = allWCEFdps
                args["countWCEFdps"] = countWCEFdps
                return redirect('../../Fdps')

        elif pagetype == "GLs":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:
                thatWCEGL = WCEGL.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "WCE Guest Lecture Deleted Successfully"
                try:
                    user = request.user
                    allWCEGLs = WCEGL.objects.filter(user=user)
                    countWCEGLs = len(allWCEGLs)
                except:
                    allWCEGLs = None
                    countWCEGLs = 0
                args = {}
                args["allWCEGLs"] = allWCEGLs
                args["countWCEGLs"] = countWCEGLs
                return redirect('../../GLs')

        elif pagetype == "Sttps":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:
                thatWCESttp = WCESttp.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "WCE STTP Deleted Successfully"
                try:
                    user = request.user
                    allWCESttps = WCESttp.objects.filter(user=user)
                    countWCESttps = len(allWCESttps)
                except:
                    allWCESttps = None
                    countWCESttps = 0
                args = {}
                args["allWCESttps"] = allWCESttps
                args["countWCESttps"] = countWCESttps
                return redirect('../../Sttps')

        elif pagetype == "Webinars":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:
                thatWCEWebinar = WCEWebinar.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "WCE Workshop Deleted Successfully"
                try:
                    user = request.user
                    allWCEWebinars = WCEWebinar.objects.filter(user=user)
                    countWCEWebinars = len(allWCEWebinars)
                except:
                    allWCEWebinars = None
                    countWCEWebinars = 0
                args = {}
                args["allWCEWebinars"] = allWCEWebinars
                args["countWCEWebinars"] = countWCEWebinars
                return redirect('../../Webinars')

        elif pagetype == "Workshops":
            group = request.user.groups.all()[0].name
            if isNotFaculty(group):
                return render(request, 'login.html')
            else:
                thatWCEWorkshop = WCEWork.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "WCE Workshop Deleted Successfully"
                try:
                    user = request.user
                    allWCEWorkshops = WCEWork.objects.filter(user=user)
                    countWCEWorkshops = len(allWCEWorkshops)
                except:
                    allWCEWorkshops = None
                    countWCEWorkshops = 0
                args = {}
                args["allWCEWorkshops"] = allWCEWorkshops
                args["countWCEWorkshops"] = countWCEWorkshops
                return redirect('../../Workshops')

    return render(request, 'delete_itemsIO.html', {'pagetype': pagetype})