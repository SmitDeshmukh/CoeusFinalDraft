from django.views.generic.base import View
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from student.models import courses as Coursera
from student.models import webinars as Webi
from student.models import workshops as Work
from student.models import competitions as Compe
from student.models import teamMember as Memba
from student.models import paperpublications as Paper
from student.models import author as Author
from student.models import student as Student
from student.models import toefl
from student.models import gate
from student.models import gre
from student.models import internship as Internship
from student.models import placements as Place
from student.models import startUp
from student.models import project as Proj
from classteacher.models import PETakenByStudent
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
import shortuuid
import requests


# if group == :
#     return render(request, 'student/home.html', {'student': userr, user: user})
# if group == 'HOD_group':
#     return render(request, 'HOD/HODhome.html', {'HOD': userr, user:user})

def getFileUploadLink(file):
    site = 'https://asia-south1-coeus-1482f.cloudfunctions.net/api/upload-file'
    up = {'file':(file.name, file.read(), "multipart/form-data")}
    resp = requests.post(site, files=up).json()
    return resp['link']

def isNotStudent(group_name):
    if group_name == 'student_group':
        return False
    else:
        return True


# Create your views here.
def studentHome(request):
    group = request.user.groups.all()[0].name
    if isNotStudent(group):
        return render(request, 'login.html')
    else:
        return render(request, 'student/home.html', {})


class studentformView(View):

    def get(self, request, template_name='student/stureg.html'):
        return render(request, template_name)

    def post(self, request, template_name='student/stureg.html'):
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        PRN = request.POST.get('PRN')
        yearOfEnrollment = request.POST.get('yearOfEnrollment')
        if request.POST.get('isDA') == "YES":
            isDA = True
        else:
            isDA = False
        year = request.POST.get('year')  # current year
        yearOfGraduation = request.POST.get('yearOfGraduation')
        dept = request.POST.get('dept')
        email = request.POST.get('email')
        password = request.POST.get('password')
        semester = request.POST.get('semester')
        confPassword = request.POST.get('conf_password')

        if password != confPassword:
            err = {'error_message': "Passwords don't match. Please Try Again."}
            return render(request, 'student/stureg.html', err)

        try:
            user = User.objects.create_user(username, email, password, first_name=first_name,
                                            last_name=last_name,)
            user.save()
        except:
            err = {}
            err['error_message'] = "Account with this Username or Email already Exists."
            return render(request, template_name, err)

        #try:
        studentData = Student(user=user, PRN=PRN, dept=dept, yearOfEnrollment=yearOfEnrollment, year=year,
                                  yearOfGraduation=yearOfGraduation, isDA=isDA, semester=semester, )
        studentData.save()
        # except:
        #     err = {}
        #     err['error_message'] = "Account with this PRN already Exists."
        #     return render(request, template_name, err)

        my_group = Group.objects.get(name='student_group')
        my_group.user_set.add(user)

        err = {}
        err['error_message'] = "Registration Successful. Please Login."
        return render(request, template_name, err)


########################################################################################################################

class courses(View):
    def get(self, request, template_name='student/courses.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
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

    def post(self, request, template_name='student/courses.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            ido = request.POST.get('ido')
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
            args["allCourses"] = allCourses
            args["countCourses"] = countCourses
            return render(request, template_name, args)


class addCourse(View):
    def get(self, request, template_name='student/addCourse.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            return render(request, template_name)

    def post(self, request, template_name='student/addCourse.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            # username=request.POST.get('username')
            name = request.POST.get('name')
            domain = request.POST.get('domain')
            platform = request.POST.get('platform')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            user = request.user

            try:
                certBool = True
                certification = request.FILES['certification']
                certification = getFileUploadLink(certification)
                publishCourse = Coursera(name=name, domain=domain, platform=platform, startDate=startDate,
                                         endDate=endDate,
                                         user=user, certification=certification, certBool=certBool)
                publishCourse.save()

            except:
                certification = "NA"
                certBool = False
                publishCourse = Coursera(name=name, domain=domain, platform=platform, startDate=startDate,
                                         endDate=endDate,
                                         user=user, certification=certification, certBool=certBool)
                publishCourse.save()

            err = {'error_message': "Course Added Successfully."}
            return render(request, template_name, err)


########################################################################################################################

class webinars(View):
    def get(self, request, template_name='student/webinars.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
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

    def post(self, request, template_name='student/webinars.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            ido = request.POST.get('ido')
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
            args["allWebinars"] = allWebinars
            args["countWebinars"] = countWebinars
            return render(request, template_name, args)


class addWebinar(View):
    def get(self, request, template_name='student/addWebinar.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        return render(request, template_name)

    def post(self, request, template_name='student/addWebinar.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        # username=request.POST.get('username')
        name = request.POST.get('name')
        organizer = request.POST.get('organizer')
        location = request.POST.get('location')
        if request.POST.get('mode') == "Online":
            mode = True
        else:
            mode = False
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        user = request.user

        try:
            certBool = True
            certification = request.FILES['certification']
            certification = getFileUploadLink(certification)
            publishWebinar = Webi(name=name, organizer=organizer, location=location, mode=mode, startDate=startDate,
                                  endDate=endDate, user=user, certification=certification, certBool=certBool)
            publishWebinar.save()

        except:
            certification = "NA"
            certBool = False
            publishWebinar = Webi(name=name, organizer=organizer, location=location, mode=mode, startDate=startDate,
                                  endDate=endDate, user=user, certification=certification, certBool=certBool)
            publishWebinar.save()

        err = {'error_message': "Webinar Added Successfully."}
        return render(request, template_name, err)


########################################################################################################################

class workshops(View):
    def get(self, request, template_name='student/workshops.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
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

    def post(self, request, template_name='student/workshops.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            ido = request.POST.get('ido')
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
            args["allWorkshops"] = allWorkshops
            args["countWorkshops"] = countWorkshops
            return render(request, template_name, args)


class addWorkshop(View):
    def get(self, request, template_name='student/addWorkshop.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        return render(request, template_name)

    def post(self, request, template_name='student/addWorkshop.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        # username=request.POST.get('username')
        name = request.POST.get('name')
        organizer = request.POST.get('organizer')
        location = request.POST.get('location')
        if request.POST.get('mode') == "Online":
            mode = True
        else:
            mode = False
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        user = request.user

        try:
            certBool = True
            certification = request.FILES['certification']
            certification = getFileUploadLink(certification)
            publishWorkshop = Work(name=name, organizer=organizer, location=location, mode=mode, startDate=startDate,
                                   endDate=endDate, user=user, certification=certification, certBool=certBool)
            publishWorkshop.save()

        except:
            certification = "NA"
            certBool = False
            publishWorkshop = Work(name=name, organizer=organizer, location=location, mode=mode, startDate=startDate,
                                   endDate=endDate, user=user, certification=certification, certBool=certBool)
            publishWorkshop.save()

        err = {'error_message': "Workshop Added Successfully."}
        return render(request, template_name, err)


########################################################################################################################

class competitions(View):
    def get(self, request, template_name='student/competitions.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        try:
            user = request.user
            allCompetitions = Memba.objects.filter(user=user)
            countCompetitions = len(allCompetitions)
        except:
            allCompetitions = None
            countCompetitions = 0
        args = {}
        args["allCompetitions"] = allCompetitions
        args["countCompetitions"] = countCompetitions
        return render(request, template_name, args)

    def post(self, request, template_name='student/competitions.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            ido = request.POST.get('ido')
            thatComp = Compe.objects.filter(id=ido).delete()
            args = {}
            args["error_message"] = "Competition Deleted Successfully"
            try:
                user = request.user
                allCompetitions = Memba.objects.filter(user=user)
                countCompetitions = len(allCompetitions)
            except:
                allCompetitions = None
                countCompetitions = 0
            args["allCompetitions"] = allCompetitions
            args["countCompetitions"] = countCompetitions
            return render(request, template_name, args)


class addCompetition(View):
    def get(self, request, template_name='student/addCompetition.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        return render(request, template_name)

    def post(self, request, template_name='student/addCompetition.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        # username=request.POST.get('username')
        compname = request.POST.get('compname')
        organizer = request.POST.get('organizer')
        location = request.POST.get('location')
        if request.POST.get('mode') == "Online":
            mode = True
        else:
            mode = False
        projectTitle = request.POST.get('projectTitle')
        description = request.POST.get('description')
        startDate = request.POST.get('startdate')
        endDate = request.POST.get('enddate')
        winner = request.POST.get('winner')
        user = request.user
        if winner == "Winner":
            winner = True
        else:
            winner = False
        # certification = request.POST.get('certification')

        # check if certification exists
        # try:
        #    certification = request.FILES['certification']
        #    fs = FileSystemStorage()
        #    filename = fs.save(shortuuid.uuid(), certification)
        #    url = fs.url(filename)
        #    certification = url
        #    certBool = True
        #    publishCompetition = Compe(compname=compname, organizer=organizer, projectTitle=projectTitle, description=description, location=location, mode=mode, startdate=startdate, enddate=enddate, winner=winner, user=user, certification=certification, certBool=certBool)
        #    publishCompetition.save()

        # except:
        #    certification = "NA"
        #    certBool = False
        #    publishCompetition = Compe(compname=compname, organizer=organizer, projectTitle=projectTitle, description=description, location=location, mode=mode, startdate=startdate, enddate=enddate, winner=winner, user=user, certification=certification, certBool=certBool)
        #    publishCompetition.save()

        publishCompetition = Compe(compname=compname, organizer=organizer, projectTitle=projectTitle,
                                   description=description, location=location, mode=mode, startDate=startDate,
                                   endDate=endDate, winner=winner, user=user)
        publishCompetition.save()

        # To Do: check if a similar Competition Already Exists.. Lets do this sometime later. It's Easy AF

        err = {'error_message': "Competition Added Successfully."}

        allMates = request.POST.get('allMates')
        allMates = allMates.rstrip()
        allMates = allMates.lstrip()
        allMates = allMates.split()

        # start adding all teammates with the associated competition
        currentCompetition = publishCompetition
        # add the adder
        adder = Memba(user=user, comps=currentCompetition)
        adder.save()
        # add other team-mates
        try:
            for mate in allMates:
                # get User Obj of mate: PNR
                mate = mate.upper()
                matePerson = Student.objects.filter(PRN=mate)
                matePerson = matePerson[0]
                matePerson = matePerson.user
                addMate = Memba(user=matePerson, comps=currentCompetition)
                addMate.save()

        except:
            err = {'error_message': "Entered PRNs of Team-Mates are Incorrect."}
        print(allMates)
        return render(request, template_name, err)


class addCompetitionCertificate(View):
    def get(self, request, template_name='student/addCompetitionCertificate.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        args = {}
        try:
            user = request.user
            allCompetitions = Memba.objects.filter(user=user, certBool=False)
        except:
            allCompetitions = None

        args["allCompetitions"] = allCompetitions
        return render(request, template_name, args)

    def post(self, request, template_name='student/addCompetitionCertificate.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        user = request.user
        comps = request.POST.get('comp')
        certification = request.POST.get('certification')
        try:
            certBool = True
            certification = request.FILES['certification']
            certification = getFileUploadLink(certification)
            Memba.objects.filter(user=user, id=comps).update(certification=certification, certBool=certBool)

        except:
            certification = "NA"
            certBool = False
            Memba.objects.filter(user=user, id=comps).update(certification=certification, certBool=certBool)

        args = {}
        args["error_message"] = "Certificate Uploaded Successfully"
        return render(request, template_name, args)


########################################################################################################################

class papers(View):
    def get(self, request, template_name='student/papers.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        try:
            user = request.user
            allPapers = Author.objects.filter(user=user)
            countPapers = len(allPapers)
        except:
            allPapers = None
            countPapers = 0
        args = {}
        args["allPapers"] = allPapers
        args["countPapers"] = countPapers
        return render(request, template_name, args)


class addPaper(View):
    def get(self, request, template_name='student/addPaper.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        return render(request, template_name)

    def post(self, request, template_name='student/addPaper.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        # username=request.POST.get('username')
        user = request.user
        papertitle = request.POST.get('papertitle')
        if (request.POST.get('mode') == "Online"):
            mode = True
        else:
            mode = False
        confname = request.POST.get('confname')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        location = request.POST.get('location')
        if (request.POST.get('level') == "International"):
            level = True
        else:
            level = False
        if (request.POST.get('publicationPorR') == "Peered-reviewed"):
            publicationPorR = True
        else:
            publicationPorR = False
        publicationtype = request.POST.get('publicationtype')
        index = request.POST.get('index')
        volumenumber = request.POST.get('volumenumber')
        issuenumber = request.POST.get('issuenumber')
        isbnissndoi = request.POST.get('isbnissndoi')
        isbnNotUnique = Paper.objects.filter(isbnissndoi=isbnissndoi).exists()
        if isbnNotUnique:
            # isbn entry exists
            err = {'error_message': "Paper with this ISBN/ISSN/DOI entry already exists."}
            return render(request, template_name, err)

        pagefrom = request.POST.get('pagefrom')
        pageto = request.POST.get('pageto')
        month = request.POST.get('month')
        year = request.POST.get('year')
        paperurl = request.POST.get('paperurl')
        # try:
        publishPaper = Paper(user=user, papertitle=papertitle, mode=mode, confname=confname, startDate=startDate,
                             endDate=endDate, location=location,
                             level=level, publicationPorR=publicationPorR, publicationtype=publicationtype, index=index,
                             volumenumber=volumenumber,
                             issuenumber=issuenumber, isbnissndoi=isbnissndoi, pagefrom=pagefrom, pageto=pageto,
                             month=month, year=year, paperurl=paperurl)
        publishPaper.save()
        # except:
        #         err = {}
        #         err['error_message'] = "You have already uploaded this Paper."
        #         return render(request, template_name, err)

        # To Do: check if a similar Paper Already Exists.. Lets do this sometime later. It's Easy AF

        err = {'error_message': "Paper Added Successfully."}

        allMates = request.POST.get('allMates')
        allMates = allMates.rstrip()
        allMates = allMates.lstrip()
        allMates = allMates.split()

        # start adding all teammates with the associated competition
        currentPaper = publishPaper
        # add the adder
        adder = Author(user=user, papers=currentPaper)
        adder.save()
        # add other team-mates
        try:
            for mate in allMates:
                # get User Obj of mate: PNR
                mate = mate.upper()
                matePerson = Student.objects.filter(PRN=mate)
                matePerson = matePerson[0]
                matePerson = matePerson.user
                addMate = Author(user=matePerson, papers=currentPaper)
                # publishPaper.save()
                addMate.save()

        except:
            err = {'error_message': "Entered PRNs of Co-Authors are Incorrect."}
        print(allMates)
        return render(request, template_name, err)


################################################################################################

class TOEFL(View):
    def get(self, request, template_name='student/TOEFL.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        try:
            user = request.user
            allTOEFL = toefl.objects.filter(user=user)
            countTOEFL = len(allTOEFL)
        except:
            allTOEFL = None
            countTOEFL = 0
        args = {}
        args["allTOEFL"] = allTOEFL
        args["countTOEFL"] = countTOEFL
        return render(request, template_name, args)

    def post(self, request, template_name='student/TOEFL.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            ido = request.POST.get('ido')
            thatTOEFL = toefl.objects.filter(id=ido).delete()
            args = {}
            args["error_message"] = "TOEFL Details Deleted Successfully"
            try:
                user = request.user
                allTOEFLs = toefl.objects.filter(user=user)
                countTOEFLs = len(allTOEFLs)
            except:
                allTOEFLs = None
                countTOEFLs = 0
            args["allTOEFLs"] = allTOEFLs
            args["countTOEFLs"] = countTOEFLs
            return render(request, template_name, args)


class addTOEFL(View):
    def get(self, request, template_name="student/addTOEFL.html"):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        return render(request, template_name)

    def post(self, request, template_name='student/addTOEFL.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        # username=request.POST.get('username')
        regNo = request.POST.get('regNo')
        testDate = request.POST.get('testDate')
        marks = request.POST.get('marks')
        totalMarks = request.POST.get('totalMarks')
        user = request.user
        publishTOEFL = toefl(regNo=regNo, testDate=testDate, marks=marks, totalMarks=totalMarks, user=user)
        publishTOEFL.save()
        err = {'error_message': "TOEFL Info Added Successfully."}
        return render(request, template_name, err)


class GATE(View):
    def get(self, request, template_name='student/GATE.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        try:
            user = request.user
            allGATE = gate.objects.filter(user=user)
            countGATE = len(allGATE)
        except:
            allGATE = None
            countGATE = 0
        args = {}
        args["allGATE"] = allGATE
        args["countGATE"] = countGATE
        return render(request, template_name, args)

    def post(self, request, template_name='student/GATE.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            ido = request.POST.get('ido')
            thatGATE = gate.objects.filter(id=ido).delete()
            args = {}
            args["error_message"] = "GATE Details Deleted Successfully"
            try:
                user = request.user
                allGATEs = gate.objects.filter(user=user)
                countGATEs = len(allGATEs)
            except:
                allGATEs = None
                countGATEs = 0
            args["allGATEs"] = allGATEs
            args["countGATEs"] = countGATEs
            return render(request, template_name, args)


class addGATE(View):
    def get(self, request, template_name="student/addGATE.html"):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        return render(request, template_name)

    def post(self, request, template_name='student/addGATE.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        # username=request.POST.get('username')
        seatNo = request.POST.get('seatNo')
        qualified = request.POST.get('qualified')
        if qualified == "Yes":
            qualified = True
        else:
            qualified = False
        marks = request.POST.get('marks')
        rank = request.POST.get('rank')
        testDate = request.POST.get('testDate')
        user = request.user
        try:
            marksheetBool = True
            marksheet = request.FILES['marksheet']
            marksheet = getFileUploadLink(marksheet)
            publishGATE = gate(seatNo=seatNo, qualified=qualified, marks=marks, rank=rank, testDate=testDate, user=user,
                               marksheet=marksheet, marksheetBool=marksheetBool)
            publishGATE.save()

        except:
            marksheet = "NA"
            marksheetBool = False
            publishGATE = gate(seatNo=seatNo, qualified=qualified, marks=marks, rank=rank, testDate=testDate, user=user,
                               marksheet=marksheet, marksheetBool=marksheetBool)
            publishGATE.save()
        err = {'error_message': "GATE Info Added Successfully."}
        return render(request, template_name, err)


class GRE(View):
    def get(self, request, template_name='student/GRE.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        try:
            user = request.user
            allGRE = gre.objects.filter(user=user)
            countGRE = len(allGRE)
        except:
            allGRE = None
            countGRE = 0
        args = {}
        args["allGRE"] = allGRE
        args["countGRE"] = countGRE
        return render(request, template_name, args)

    def post(self, request, template_name='student/GRE.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            ido = request.POST.get('ido')
            thatGRE = gre.objects.filter(id=ido).delete()
            args = {}
            args["error_message"] = "GRE Details Deleted Successfully"
            try:
                user = request.user
                allGREs = gre.objects.filter(user=user)
                countGREs = len(allGREs)
            except:
                allGREs = None
                countGREs = 0
            args["allGREs"] = allGREs
            args["countGREs"] = countGREs
            return render(request, template_name, args)


class addGRE(View):
    def get(self, request, template_name="student/addGRE.html"):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        return render(request, template_name)

    def post(self, request, template_name='student/addGRE.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        regNo = request.POST.get('regNo')
        testDate = request.POST.get('testDate')
        marks = request.POST.get('marks')
        totalMarks = request.POST.get('totalMarks')
        user = request.user
        publishGRE = gre(regNo=regNo, testDate=testDate, marks=marks, totalMarks=totalMarks, user=user)
        publishGRE.save()
        err = {'error_message': "GRE Info Added Successfully."}
        return render(request, template_name, err)


class internship(View):
    def get(self, request, template_name='student/internship.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        try:
            user = request.user
            allInternship = Internship.objects.filter(user=user)
            countInternship = len(allInternship)
        except:
            allInternship = None
            countInternship = 0
        args = {}
        args["allInternship"] = allInternship
        args["countInternship"] = countInternship
        return render(request, template_name, args)

    def post(self, request, template_name='student/internship.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            ido = request.POST.get('ido')
            thatInternship = Internship.objects.filter(id=ido).delete()
            args = {}
            args["error_message"] = "Internship Details Deleted Successfully"
            try:
                user = request.user
                allInternships = Internship.objects.filter(user=user)
                countInternships = len(allInternships)
            except:
                allInternships = None
                countInternships = 0
            args["allInternships"] = allInternships
            args["countInternships"] = countInternships
            return render(request, template_name, args)


class addInternship(View):
    def get(self, request, template_name="student/addInternship.html"):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        return render(request, template_name)

    def post(self, request, template_name='student/addInternship.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        # username=request.POST.get('username')
        companyName = request.POST.get('companyName')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        domain = request.POST.get('domain')
        details = request.POST.get('details')
        if request.POST.get('mode') == "Online":
            mode = True
        else:
            mode = False

        if request.POST.get('internshipType') == "Winter":
            internshipType = True
        else:
            internshipType = False

        user = request.user

        try:
            certBool = True
            certification = request.FILES['certification']
            certification = getFileUploadLink(certification)
            internShip = Internship(companyName=companyName, internshipType=internshipType, domain=domain,
                                    details=details, mode=mode,
                                    startDate=startDate,
                                    endDate=endDate, user=user, certification=certification, certBool=certBool)
            internShip.save()

        except:
            certification = "NA"
            certBool = False
            internShip = Internship(companyName=companyName, internshipType=internshipType, domain=domain,
                                    details=details, mode=mode,
                                    startDate=startDate,
                                    endDate=endDate, user=user, certification=certification, certBool=certBool)
            internShip.save()

        err = {'error_message': "Internship Details Added Successfully."}
        return render(request, template_name, err)


class StartUp(View):
    def get(self, request, template_name='student/StartUp.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        try:
            user = request.user
            allStartUp = startUp.objects.filter(user=user)
            countStartUp = len(allStartUp)
        except:
            allStartUp = None
            countStartUp = 0
        args = {}
        args["allStartUp"] = allStartUp
        args["countStartUp"] = countStartUp
        return render(request, template_name, args)

    def post(self, request, template_name='student/StartUp.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            ido = request.POST.get('ido')
            thatStartUp = startUp.objects.filter(id=ido).delete()
            args = {}
            args["error_message"] = "StartUp Details Deleted Successfully"
            try:
                user = request.user
                allStartUp = startUp.objects.filter(user=user)
                countStartUp = len(allStartUp)
            except:
                allStartUp = None
                countStartUp = 0
            args["allStartUp"] = allStartUp
            args["countStartUp"] = countStartUp
            return render(request, template_name, args)


class addStartUp(View):
    def get(self, request, template_name="student/addStartUp.html"):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        return render(request, template_name)

    def post(self, request, template_name='student/addStartUp.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        companyName = request.POST.get('companyName')
        year = request.POST.get('year')
        registrationNumber = request.POST.get('registrationNumber')
        domain = request.POST.get('domain')
        supportingAgency = request.POST.get('supportingAgency')
        user = request.user
        publishStartUp = startUp(companyName=companyName, domain=domain, year=year, user=user,
                                 registrationNumber=registrationNumber, supportingAgency=supportingAgency)
        publishStartUp.save()
        err = {'error_message': "Start Up Info Added Successfully."}
        return render(request, template_name, err)


class placements(View):
    def get(self, request, template_name='student/placements.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        try:
            user = request.user
            allPlacements = Place.objects.filter(user=user)
            countPlacements = len(allPlacements)
        except:
            allPlacements = None
            countPlacements = 0
        args = {}
        args["allPlacements"] = allPlacements
        args["countPlacements"] = countPlacements
        return render(request, template_name, args)

    def post(self, request, template_name='student/placements.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            ido = request.POST.get('ido')
            thatPlacement = Place.objects.filter(id=ido).delete()
            args = {}
            args["error_message"] = "Placement Details Deleted Successfully"
            try:
                user = request.user
                allPlacements = Place.objects.filter(user=user)
                countPlacements = len(allPlacements)
            except:
                allPlacements = None
                countPlacements = 0
            args["allPlacements"] = allPlacements
            args["countPlacements"] = countPlacements
            return render(request, template_name, args)


class addPlacement(View):
    def get(self, request, template_name="student/addPlacement.html"):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        return render(request, template_name)

    def post(self, request, template_name='student/addPlacement.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        # username=request.POST.get('username')
        companyName = request.POST.get('companyName')
        yearPlaced = request.POST.get('yearPlaced')
        domain = request.POST.get('domain')
        ctc = request.POST.get('ctc')
        role = request.POST.get('role')
        user = request.user
        publishPlacement = Place(companyName=companyName, domain=domain, yearPlaced=yearPlaced, ctc=ctc, role=role,
                                 user=user)
        publishPlacement.save()
        err = {'error_message': "Placment INFO Added Successfully."}
        return render(request, template_name, err)


class projects(View):
    def get(self, request, template_name="student/projects.html"):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        try:
            user = request.user
            allProjects = Proj.objects.filter(user=user)
            countProjects = len(allProjects)
        except:
            allProjects = None
            countProjects = 0
        args = {}
        args["allProjects"] = allProjects
        args["countProjects"] = countProjects
        return render(request, template_name, args)

    def post(self, request, template_name='student/projects.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            ido = request.POST.get('ido')
            thatProject = Proj.objects.filter(id=ido).delete()
            args = {}
            args["error_message"] = "Project Details Deleted Successfully"
            try:
                user = request.user
                allProjects = Proj.objects.filter(user=user)
                countProjects = len(allProjects)
            except:
                allProjects = None
                countProjects = 0
            args["allProjects"] = allProjects
            args["countProjects"] = countProjects
            return render(request, template_name, args)


class addProject(View):
    def get(self, request, template_name="student/addProject.html"):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        return render(request, template_name)

    def post(self, request, template_name='student/addProject.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        # username=request.POST.get('username')
        user = request.user
        title = request.POST.get('title')
        guideName = request.POST.get('guideName')
        domain = request.POST.get('domain')
        semester = request.POST.get('semester')
        year = request.POST.get('year')
        if request.POST.get('socialCause') == "Yes":
            socialCause = True
        else:
            socialCause = False
        cause = request.POST.get('cause')
        customer = request.POST.get('customer')
        publishProject = Proj(user=user, title=title, guideName=guideName, domain=domain, semester=semester, year=year,
                              socialCause=socialCause, cause=cause, customer=customer)
        publishProject.save()
        err = {'error_message': "Project INFO Added Successfully."}
        return render(request, template_name, err)


##############Display Assigned PEs####################################
class PE(View):
    def get(self, request, template_name='student/PE.html'):
        group = request.user.groups.all()[0].name
        if isNotStudent(group):
            return render(request, 'login.html')
        else:
            try:
                user = request.user
                Studentobj = user.student
                allPEs = PETakenByStudent.objects.filter(student=Studentobj)
                countPEs = len(allPEs)
            except:
                allPEs = None
                countPEs = 0
            args = {}
            args["allPEs"] = allPEs
            args["countPEs"] = countPEs
            return render(request, template_name, args)

def delete_items(request, ido, pagetype):
    if request.method == 'POST':
        if pagetype == 'courses':
            group = request.user.groups.all()[0].name
            if isNotStudent(group):
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
                args["allCourses"] = allCourses
                args["countCourses"] = countCourses
                return redirect('../../courses')

        elif pagetype == "GATE":
            group = request.user.groups.all()[0].name
            if isNotStudent(group):
                return render(request, 'login.html')
            else:
                thatGATE = gate.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "GATE Details Deleted Successfully"
                try:
                    user = request.user
                    allGATEs = gate.objects.filter(user=user)
                    countGATEs = len(allGATEs)
                except:
                    allGATEs = None
                    countGATEs = 0
                args["allGATEs"] = allGATEs
                args["countGATEs"] = countGATEs
                return redirect('../../GATE')

        elif pagetype == "GRE":
            group = request.user.groups.all()[0].name
            if isNotStudent(group):
                return render(request, 'login.html')
            else:
                thatGRE = gre.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "GRE Details Deleted Successfully"
                try:
                    user = request.user
                    allGREs = gre.objects.filter(user=user)
                    countGREs = len(allGREs)
                except:
                    allGREs = None
                    countGREs = 0
                args["allGREs"] = allGREs
                args["countGREs"] = countGREs

                return redirect('../../GRE')

        elif pagetype == "Internship":
            group = request.user.groups.all()[0].name
            if isNotStudent(group):
                return render(request, 'login.html')
            else:

                thatInternship = Internship.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "Internship Details Deleted Successfully"
                try:
                    user = request.user
                    allInternships = Internship.objects.filter(user=user)
                    countInternships = len(allInternships)
                except:
                    allInternships = None
                    countInternships = 0
                args["allInternships"] = allInternships
                args["countInternships"] = countInternships

                return redirect('../../Internship')

        elif pagetype == "placement":
            group = request.user.groups.all()[0].name
            if isNotStudent(group):
                return render(request, 'login.html')
            else:

                thatPlacement = Place.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "Placement Details Deleted Successfully"
                try:
                    user = request.user
                    allPlacements = Place.objects.filter(user=user)
                    countPlacements = len(allPlacements)
                except:
                    allPlacements = None
                    countPlacements = 0
                args["allPlacements"] = allPlacements
                args["countPlacements"] = countPlacements

                return redirect('../../placement')

        elif pagetype == "projects":
            group = request.user.groups.all()[0].name
            if isNotStudent(group):
                return render(request, 'login.html')
            else:

                thatProject = Proj.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "Project Details Deleted Successfully"
                try:
                    user = request.user
                    allProjects = Proj.objects.filter(user=user)
                    countProjects = len(allProjects)
                except:
                    allProjects = None
                    countProjects = 0
                args["allProjects"] = allProjects
                args["countProjects"] = countProjects

                return redirect('../../projects')

        elif pagetype == "StartUp":
            group = request.user.groups.all()[0].name
            if isNotStudent(group):
                return render(request, 'login.html')
            else:

                thatStartUp = startUp.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "StartUp Details Deleted Successfully"
                try:
                    user = request.user
                    allStartUp = startUp.objects.filter(user=user)
                    countStartUp = len(allStartUp)
                except:
                    allStartUp = None
                    countStartUp = 0
                args["allStartUp"] = allStartUp
                args["countStartUp"] = countStartUp

                return redirect('../../StartUp')

        elif pagetype == "TOEFL":
            group = request.user.groups.all()[0].name
            if isNotStudent(group):
                return render(request, 'login.html')
            else:

                thatTOEFL = toefl.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "TOEFL Details Deleted Successfully"
                try:
                    user = request.user
                    allTOEFLs = toefl.objects.filter(user=user)
                    countTOEFLs = len(allTOEFLs)
                except:
                    allTOEFLs = None
                    countTOEFLs = 0
                args["allTOEFLs"] = allTOEFLs
                args["countTOEFLs"] = countTOEFLs

                return redirect('../../TOEFL')

        elif pagetype == "webinars":
            group = request.user.groups.all()[0].name
            if isNotStudent(group):
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
                args["allWebinars"] = allWebinars
                args["countWebinars"] = countWebinars

                return redirect('../../webinars')

        elif pagetype == "workshops":
            group = request.user.groups.all()[0].name
            if isNotStudent(group):
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
                args["allWorkshops"] = allWorkshops
                args["countWorkshops"] = countWorkshops

                return redirect('../../workshops')

    return render(request, 'delete_items.html', {'pagetype': pagetype})