from io import TextIOWrapper

from django.shortcuts import render
import csv
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import Group
from HOD.models import courseexitsurvey as CourseES
from HOD.models import deptfeedbacksurvey as DeptFS
from HOD.models import gradexitsurvey as GradES

# teacher models

from teacher.models import wcefdp as WCEFdp
from teacher.models import iofdp as FDP
from teacher.models import ioworkshops as atWork
from teacher.models import wceworkshops as orWork
from teacher.models import iopaper as pubPaper
from teacher.models import wceguestlectures as GL
from teacher.models import iocourses as comCourse
from teacher.models import ioworkshops as atWebi
from teacher.models import wcewebinars as orWebi
from teacher.models import wcesttp as orSttp
from teacher.models import iosttp as atSttp
from teacher.models import faculty as Facu
from teacher.models import wcefdp as orFdp

# student models 

from student.models import student as Stu
from student.models import paperpublications as stuPapers
from student.models import courses as stuOnlineCourses
from student.models import competitions as stuComps
from student.models import teamMember as TeamMember
from student.models import internship as Interns
from student.models import placements as stuPlacements
from student.models import startUp as Startups
from student.models import gre as GRE
from student.models import toefl as TOEFL
from student.models import gate as GATE
from student.models import project as Proj
from student.models import teamMember as tMemba
from student.models import webinars as Webi
from student.models import workshops as Work

# classTeacher Models

from classteacher.models import PEs
from classteacher.models import PETakenByStudent

from django.contrib.auth.models import User as User
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
import shortuuid
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q

import requests

def getFileUploadLink(file):
    site = 'https://asia-south1-coeus-1482f.cloudfunctions.net/api/upload-file'
    up = {'file':(file.name, file.read(), "multipart/form-data")}
    resp = requests.post(site, files=up).json()
    return resp['link']

def isNotHOD(group_name):
    if group_name == 'HOD_group':
        return False
    else:
        return True

def HODHome(request):
    group = request.user.groups.all()[0].name
    if isNotHOD(group):
        return render(request, 'login.html')
    args = {}
    args["isHOD"] = True
    return render(request, 'HOD/HODhome.html', args)


class courseES(View):
    def get(self, request, template_name='HOD/courseES.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            user = request.user
            allCourseES = CourseES.objects.filter(user=user)
            countCourseES = len(allCourseES)
        except:
            allCourseES = None
            countCourseES = 0
        args = {}
        args["allCourseES"] = allCourseES
        args["countCourseES"] = countCourseES
        args["isHOD"] = True
        return render(request, template_name, args)


class addFaculty(View):
    def get(self, request, template_name='HOD/AddFaculty.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name="HOD/AddFaculty.html"):
        uploadcsv = request.FILES['uploadcsv']
        uploadcsv = TextIOWrapper(uploadcsv.file, encoding=request.encoding)
        file_reader = csv.reader(uploadcsv, delimiter=',')
        counter = 0
        cantBeAdded = []
        for row in file_reader:
            # do something with row data.
            if counter == 0:
                counter += 1
                continue
            username = row[0]
            first_name = row[1]
            last_name = row[2]
            dept = row[3]
            degree = row[4]
            desig = row[5]
            profile = row[6]
            email = row[7]
            password = row[8]
            try:
                # create user

                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    # print(user)

                    # update student info and save
                    faculty = Facu.objects.get(user=user)
                    faculty.dept = dept
                    faculty.degree = degree
                    faculty.desig = desig
                    faculty.profile = profile

                    faculty.save()
                    # err = {'error_message': "Existing facultys Updated"}
                else:
                    user = User.objects.create_user(username, email, password, first_name=first_name,
                                                    last_name=last_name, )
                    user.save()
                    # create faculty
                    facultyData = Facu(user=user, dept=dept, degree=degree, desig=desig,
                                       profile=profile, )
                    facultyData.save()
                    # assign group
                    my_group = Group.objects.get(name='faculty_group')
                    my_group.user_set.add(user)
                    # err = {'error_message': "facultys Added successfully."}
            except:
                cantBeAdded.append(username)

        err = {'error_message': "facultys Added/Updated successfully.", 'cantBeAdded': cantBeAdded}
        return render(request, template_name, err)


class addCourseES(View):
    def get(self, request, template_name='HOD/addCourseES.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/addCourseES.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # username=request.POST.get('username')
        name = request.POST.get('name')
        coursecode = request.POST.get('coursecode')
        courseclass = request.POST.get('courseclass')
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        user = request.user

        try:
            uploadcourseexitsurvey = request.FILES['uploadcourseexitsurvey']
            uploadcourseexitsurvey = getFileUploadLink(uploadcourseexitsurvey)
            publishCourseES = CourseES(name=name, coursecode=coursecode, courseclass=courseclass, year=year, user=user,
                                       semester=semester, uploadcourseexitsurvey=uploadcourseexitsurvey)
            publishCourseES.save()

        except:
            uploadcourseexitsurvey = "NA"
            publishCourseES = CourseES(name=name, coursecode=coursecode, courseclass=courseclass, year=year, user=user,
                                       semester=semester, uploadcourseexitsurvey=uploadcourseexitsurvey)
            publishCourseES.save()

        err = {'error_message': "Course Exit Survey Added Successfully."}
        err["isHOD"] = True
        return render(request, template_name, err)


class deptFS(View):
    def get(self, request, template_name='HOD/deptFS.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            user = request.user
            allDeptFS = DeptFS.objects.filter(user=user)
            countDeptFS = len(allDeptFS)
        except:
            allDeptFS = None
            countDeptFS = 0
        args = {}
        args["allDeptFS"] = allDeptFS
        args["countDeptFS"] = countDeptFS
        args["isHOD"] = True
        return render(request, template_name, args)


class addDeptFS(View):
    def get(self, request, template_name='HOD/addDeptFS.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/addDeptFS.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # username=request.POST.get('username')
        deptname = request.POST.get('deptname')
        courseclass = request.POST.get('courseclass')
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        user = request.user

        try:
            uploaddeptexitsurvey = request.FILES['uploaddeptexitsurvey']
            uploaddeptexitsurvey = getFileUploadLink(uploaddeptexitsurvey)
            publishDeptES = DeptFS(deptname=deptname, courseclass=courseclass, year=year, user=user,
                                   semester=semester, uploaddeptexitsurvey=uploaddeptexitsurvey)
            publishDeptES.save()

        except:
            uploaddeptexitsurvey = "NA"
            publishDeptES = DeptFS(deptname=deptname, courseclass=courseclass, year=year, user=user,
                                   semester=semester, uploaddeptexitsurvey=uploaddeptexitsurvey)
            publishDeptES.save()

        err = {'error_message': "Department Feedback Survey Added Successfully."}
        err["isHOD"] = True
        return render(request, template_name, err)


class gradES(View):
    def get(self, request, template_name='HOD/gradES.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            user = request.user
            allGradES = GradES.objects.filter(user=user)
            countGradES = len(allGradES)
        except:
            allGradES = None
            countGradES = 0
        args = {}
        args["allGradES"] = allGradES
        args["countGradES"] = countGradES
        args["isHOD"] = True
        return render(request, template_name, args)


class addGradES(View):
    def get(self, request, template_name='HOD/addGradES.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/addGradES.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # username=request.POST.get('username')
        deptname = request.POST.get('deptname')
        startYear = request.POST.get('startYear')
        endYear = request.POST.get('endYear')
        user = request.user

        try:
            uploadgradexitsurvey = request.FILES['uploadgradexitsurvey']
            uploadgradexitsurvey = getFileUploadLink(uploadgradexitsurvey)
            publishGradES = GradES(deptname=deptname, startYear=startYear, endYear=endYear, user=user,
                                   uploadgradexitsurvey=uploadgradexitsurvey)
            publishGradES.save()

        except:
            uploadgradexitsurvey = "NA"
            publishGradES = GradES(deptname=deptname, startYear=startYear, endYear=endYear, user=user,
                                   uploadgradexitsurvey=uploadgradexitsurvey)
            publishGradES.save()

        err = {'error_message': "Graduation Exit Survey Added Successfully."}
        err["isHOD"] = True
        return render(request, template_name, err)


############################Queries for Individual Faculty####################################

class FDPqueries(View):
    def get(self, request, template_name='HOD/facultyQueries/fdpquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="faculty_group")
            usersList = group.user_set.all()
        except:
            group = None
            usersList = None
        args = {}
        args["group"] = group
        args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/facultyQueries/fdpquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        email = request.POST.get('email')
        option = request.POST.get('option')
        year = request.POST.get('year')
        red = "FDPqueryResult/" + email + "/" + option + "/" + year
        return redirect(red)


class FDPqueryResult(View):
    def get(self, request, email, option, year, template_name='HOD/facultyQueries/fdpresult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        user = User.objects.get(email=email)
        if option == "Organized":
            try:
                allOrFDPs = WCEFdp.objects.filter(user=user, endDate__year=year)
                countOrFdps = len(allOrFDPs)
            except:
                allOrFDPs = None
                countOrFdps = 0
            args = {}
            args["allOrFDPs"] = allOrFDPs
            args["countOrFdps"] = countOrFdps
            args["user"] = user
            args["isHOD"] = True
            args["option"] = True
            args["year"] = year
            return render(request, "HOD/facultyQueries/fdpresult.html", args)
        elif option == "Attended":
            try:
                allAtFDPs = FDP.objects.filter(user=user, endDate__year=year)
                countAtFdps = len(allAtFDPs)
            except:
                allAtFDPs = None
                countAtFdps = 0
            args = {}
            args["allAtFDPs"] = allAtFDPs
            args["countAtFdps"] = countAtFdps
            args["user"] = user
            args["isHOD"] = True
            args["option"] = False
            args["year"] = year
            try:
                group = Group.objects.get(name="faculty_group")
                usersList = group.user_set.all()
            except:
                group = None
                usersList = None
            args["group"] = group
            args["usersList"] = usersList
            args["isHOD"] = True
            return render(request, "HOD/facultyQueries/fdpresult.html", args)
        return render(request, template_name)

    def post(self, request, year, email, option):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="FDPs.csv"'
        user = User.objects.get(email=email)

        writer = csv.writer(response)

        if option == "Organized":
            try:
                allOrFDPs = WCEFdp.objects.filter(user=user, endDate__year=year)
                # countOrFdps = len(allOrFDPs)
            except:
                allOrFDPs = None
                # countOrFdps = 0
            writer.writerow(["Faculty Name", "FDP Title", "Domain", "Location", "Start Date", "End Date",
                             "Number of Participants", "Organized/Delivered By", "Organized/Attended"])
            for i in allOrFDPs:
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.location, str(i.startDate.day) +
                     "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                     str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year),
                     i.numberOfParticipants, i.organizer, "Organized"])

        elif option == "Attended":
            try:
                allAtFDPs = FDP.objects.filter(user=user, endDate__year=year)
                # countAtFdps = len(allAtFDPs)
            except:
                allAtFDPs = None
                # countAtFdps = 0

            try:
                group = Group.objects.get(name="faculty_group")
                # usersList = group.user_set.all()
            except:
                group = None
                # usersList = None
            writer.writerow(
                ["Faculty Name", "FDP Title", "Domain", "Location", "Organized By", "Start Date", "End Date", "Mode", "Organized/Attended"])
            for i in allAtFDPs:
                if i.mode:
                    mode = "Online"
                else:
                    mode = "Offline"
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.location, i.organizer,
                     str(i.startDate.day) +
                     "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                     str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), mode, "Attended"])

        return response


class Workqueries(View):
    def get(self, request, template_name='HOD/facultyQueries/workquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="faculty_group")
            usersList = group.user_set.all()
        except:
            group = None
            usersList = None
        args = {}
        args["group"] = group
        args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/facultyQueries/workquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        email = request.POST.get('email')
        option = request.POST.get('option')
        year = request.POST.get('year')
        red = "WorkshopqueryResult/" + email + "/" + option + "/" + year
        return redirect(red)


class WorkshopqueryResult(View):
    def get(self, request, email, option, year, template_name='HOD/facultyQueries/workresult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        user = User.objects.get(email=email)
        if option == "Organized":
            try:
                allOrWorks = orWork.objects.filter(user=user, endDate__year=year)
                countOrWorks = len(allOrWorks)
            except:
                allOrWorks = None
                countOrWorks = 0
            args = {}
            args["allOrWorks"] = allOrWorks
            args["countOrWorks"] = countOrWorks
            args["user"] = user
            args["isHOD"] = True
            args["option"] = True
            args["year"] = year
            return render(request, "HOD/facultyQueries/workresult.html", args)
        elif option == "Attended":
            try:
                allAtWorks = atWork.objects.filter(user=user, endDate__year=year)
                countAtWorks = len(allAtWorks)
            except:
                allAtWorks = None
                countAtWorks = 0
            args = {}
            args["allAtWorks"] = allAtWorks
            args["countAtWorks"] = countAtWorks
            args["user"] = user
            args["isHOD"] = True
            args["option"] = False
            args["year"] = year
            return render(request, "HOD/facultyQueries/workresult.html", args)
        return render(request, template_name)

    def post(self, request, year, email, option):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')

        if option == "Organized":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="FacultyWorkshopsOrganizedfile.csv"'
            user = User.objects.get(email=email)
            writer = csv.writer(response)
            writer.writerow(
                ["Faculty Name", "Workshop Name", "Domain", "Organizer", "Location", "Mode", "Role", "Start Date",
                 "End Date", "Number of Participants", "Organized/Attended"])
            try:
                allOrWorks = orWork.objects.filter(user=user, endDate__year=year)
                countOrWorks = len(allOrWorks)
            except:
                allOrWorks = None
                countOrWorks = 0
            for i in allOrWorks:
                if i.mode:
                    mode = "Online"
                else:
                    mode = "Offline"
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.organizer, i.location, mode,
                     i.role, str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                     str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year),
                     i.numberOfParticipants, "Organized" ])

        elif option == "Attended":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="FacultyWorkshopsAttendedfile.csv"'
            user = User.objects.get(email=email)

            writer = csv.writer(response)
            writer.writerow(
                ["Faculty Name", "Workshop Name", "Domain", "Organizer", "Location", "Mode", "Start Date",
                 "End Date", "Organized/Attended"])
            try:
                allAtWorks = atWork.objects.filter(user=user, endDate__year=year)
                countAtWorks = len(allAtWorks)
            except:
                allAtWorks = None
                countAtWorks = 0
            for i in allAtWorks:
                if i.mode:
                    mode = "Online"
                else:
                    mode = "Offline"
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.organizer, i.location, mode,
                     str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                     str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), "Attended" ])

        return response


class Paperqueries(View):
    def get(self, request, template_name='HOD/facultyQueries/paperquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="faculty_group")
            usersList = group.user_set.all()
        except:
            group = None
            usersList = None
        args = {}
        args["group"] = group
        args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/facultyQueries/paperquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        email = request.POST.get('email')
        year = request.POST.get('year')
        st = "PaperqueryResult/" + email + "/" + year
        return redirect(st)


class PaperqueryResult(View):
    def get(self, request, email, year, template_name='HOD/facultyQueries/paperresult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        user = User.objects.get(email=email)
        try:
            allPubPapers = pubPaper.objects.filter(user=user, year=year)
            countPubPapers = len(allPubPapers)
        except:
            allPubPapers = None
            countPubPapers = 0
        args = {}
        args["allPubPapers"] = allPubPapers
        args["countPubPapers"] = countPubPapers
        args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, "HOD/facultyQueries/paperresult.html", args)

    def post(self, request, year, email):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="PublishedPapersfile.csv"'
        thatUser = User.objects.filter(email=email)
        thatUser = thatUser[0]
        allPubPapers = pubPaper.objects.filter(year=year, user=thatUser)
        writer = csv.writer(response)
        writer.writerow(["Name", "Paper Title", "Mode", "Conference Name", "startDate", "endDate", "location", "level",
                         "PeerReviewed/Referred", "publicationtype", "index", "volumenumber", "issuenumber",
                         "isbnissndoi",
                         "pagefrom", "pageto", "month", "year"])

        for i in allPubPapers:
            if i.mode:
                mode = "Online"
            else:
                mode = "Offline"
            if i.level:
                level = "International"
            else:
                level = "National"
            if i.publicationPorR:
                publicationPorR = "Peer-Reviewed"
            else:
                publicationPorR = "Referred"
            writer.writerow(
                [i.user.first_name + " " + i.user.last_name, i.papertitle, mode, i.confname,
                 str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                 str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year),
                 i.location, level, publicationPorR, i.publicationtype, i.index, i.volumenumber, i.issuenumber,
                 i.isbnissndoi, i.pagefrom, i.pageto, i.month, i.year])
        return response


class GLqueries(View):
    def get(self, request, template_name='HOD/facultyQueries/glquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="faculty_group")
            usersList = group.user_set.all()
        except:
            group = None
            usersList = None
        args = {}
        args["group"] = group
        args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/facultyQueries/glquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        email = request.POST.get('email')
        year = request.POST.get('year')
        user = User.objects.get(email=email)
        try:
            allGLs = GL.objects.filter(user=user, date__year=year)
            countGLs = len(allGLs)
        except:
            allGLs = None
            countGLs = 0
        args = {}
        args["allGLs"] = allGLs
        args["countGLs"] = countGLs
        args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        st = "GuestLecturequeryResult/" + email + "/" + year
        return redirect(st)
        return render(request, template_name, args)


class GuestLecturequeryResult(View):
    def get(self, request, email, year, template_name='HOD/facultyQueries/glresult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        user = User.objects.get(email=email)
        try:
            allGLs = GL.objects.filter(user=user, date__year=year)
            countGLs = len(allGLs)
        except:
            allGLs = None
            countGLs = 0
        args = {}
        args["allGLs"] = allGLs
        args["countGLs"] = countGLs
        args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, "HOD/facultyQueries/glresult.html", args)

    def post(self, request, year, email):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="GuestLecturesOrganizedfile.csv"'
        thatUser = User.objects.filter(email=email)
        thatUser = thatUser[0]

        allGLs = GL.objects.filter(date__year=year, user=thatUser)
        writer = csv.writer(response)
        writer.writerow(
            ["Faculty Name", "Topic", "Domain", "Resource Person Name", "Resource Person Profession", "Date",
             "Beneficiaries", "Number Of Participants"])
        for i in allGLs:
            writer.writerow(
                [i.user.first_name + " " + i.user.last_name, i.topic, i.domain, i.resourcepersonname,
                 i.resourcepersonprofession, str(i.date.day) + "/" + str(i.date.month) + "/" + str(i.date.year), i.beneficiaries, i.numberOfParticipants])
        return response


class Coursequeries(View):
    def get(self, request, template_name='HOD/facultyQueries/coursequery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="faculty_group")
            usersList = group.user_set.all()
        except:
            group = None
            usersList = None
        args = {}
        args["group"] = group
        args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/facultyQueries/coursequery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        email = request.POST.get('email')
        year = request.POST.get('year')
        user = User.objects.get(email=email)
        red = "OnlineCoursequeryResult/" + email + "/" + year
        return redirect(red)


class OnlineCoursequeryResult(View):
    def get(self, request, email, year, template_name='HOD/facultyQueries/courseresult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        user = User.objects.get(email=email)
        try:
            allcomCourses = comCourse.objects.filter(endDate__year=year, user=user)
            countcomCourses = len(allcomCourses)
        except:
            allcomCourses = None
            countcomCourses = 0
        args = {}
        args["allcomCourses"] = allcomCourses
        args["countcomCourses"] = countcomCourses
        args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year, email):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="OnlineCoursesCompletedfile.csv"'
        thatUser = User.objects.filter(email=email)
        thatUser = thatUser[0]
        allcomCourses = comCourse.objects.filter(endDate__year=year, user=thatUser)
        writer = csv.writer(response)
        writer.writerow(
            ["Faculty Name", "Course Name", "Domain", "Platform", "Duration weeks", "End Date", "In or Outside WCE"])
        for i in allcomCourses:
            if i.inorout:
                inorout = "In WCE"
            else:
                inorout = "Outside WCE"
            writer.writerow(
                [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.platform, i.durationweeks,
                 str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), inorout])
        return response


class Webinarqueries(View):
    def get(self, request, template_name='HOD/facultyQueries/webinarquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="faculty_group")
            usersList = group.user_set.all()
        except:
            group = None
            usersList = None
        args = {}
        args["group"] = group
        args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/facultyQueries/webinarquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        email = request.POST.get('email')
        option = request.POST.get('option')
        year = request.POST.get('year')
        red = "WebinarqueryResult/" + email + "/" + option + "/" + year
        return redirect(red)


class WebinarqueryResult(View):
    def get(self, request, email, option, year, template_name='HOD/facultyQueries/webinarresult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        user = User.objects.get(email=email)
        if option == "Organized":
            try:
                allOrWebis = orWebi.objects.filter(user=user, endDate__year=year)
                countOrWebis = len(allOrWebis)
            except:
                allOrWebis = None
                countOrWebis = 0
            args = {}
            args["allOrWebis"] = allOrWebis
            args["countOrWebis"] = countOrWebis
            args["user"] = user
            args["isHOD"] = True
            args["option"] = True
            args["year"] = year
            return render(request, "HOD/facultyQueries/webinarresult.html", args)
        elif option == "Attended":
            try:
                allAtWebis = atWebi.objects.filter(user=user, endDate__year=year)
                countAtWebis = len(allAtWebis)
            except:
                allAtWebis = None
                countAtWebis = 0
            args = {}
            args["allAtWebis"] = allAtWebis
            args["countAtWebis"] = countAtWebis
            args["user"] = user
            args["isHOD"] = True
            args["option"] = False
            args["year"] = year
            try:
                group = Group.objects.get(name="faculty_group")
                usersList = group.user_set.all()
            except:
                group = None
                usersList = None
            args["group"] = group
            args["usersList"] = usersList
            args["isHOD"] = True
            return render(request, "HOD/facultyQueries/webinarresult.html", args)
        return render(request, template_name)

    def post(self, request, year, email, option):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')

        if option == "Organized":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="FacultyWebinarsOrganizedfile.csv"'
            user = User.objects.get(email=email)
            writer = csv.writer(response)
            writer.writerow(
                ["Faculty Name", "Webinar Name", "Domain", "Organizer", "Location", "Mode", "Role", "Start Date",
                 "End Date", "Number of Participants", "Organized/Attended" ])
            try:
                allOrWebis = orWebi.objects.filter(user=user, endDate__year=year)
                countOrWebis = len(allOrWebis)
            except:
                allOrWebis = None
                countOrWebis = 0
            for i in allOrWebis:
                if i.mode:
                    mode = "Online"
                else:
                    mode = "Offline"
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.organizer, i.location, mode,
                     i.role, str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                     str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year),
                     i.numberOfParticipants,"Organized" ])

        elif option == "Attended":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="FacultyWebinarsAttendedfile.csv"'
            user = User.objects.get(email=email)

            writer = csv.writer(response)
            writer.writerow(
                ["Faculty Name", "Webinar Name", "Domain", "Organizer", "Location", "Mode", "Start Date",
                 "End Date", "In Or Outside WCE", "Organized/Attended" ])
            try:
                allAtWebis = atWebi.objects.filter(user=user, endDate__year=year)
                countAtWebis = len(allAtWebis)
            except:
                allAtWebis = None
                countAtWebis = 0
            try:
                group = Group.objects.get(name="faculty_group")
                usersList = group.user_set.all()
            except:
                group = None
                usersList = None
            for i in allAtWebis:
                if i.mode:
                    mode = "Online"
                else:
                    mode = "Offline"
                if i.inorout:
                    inorout = "In WCE"
                else:
                    inorout = "Outside WCE"
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.organizer, i.location, mode,
                     str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                     str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), inorout, "Attended"])

        return response


class Sttpqueries(View):
    def get(self, request, template_name='HOD/facultyQueries/sttpquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="faculty_group")
            usersList = group.user_set.all()
        except:
            group = None
            usersList = None
        args = {}
        args["group"] = group
        args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/facultyQueries/sttpquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        email = request.POST.get('email')
        option = request.POST.get('option')
        year = request.POST.get('year')
        red = "SttpqueryResult/" + email + "/" + option + "/" + year
        return redirect(red)


class SttpqueryResult(View):
    def get(self, request, email, option, year, template_name='HOD/facultyQueries/sttpresult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        user = User.objects.get(email=email)
        if option == "Organized":
            try:
                allOrSttps = orSttp.objects.filter(user=user, endDate__year=year)
                countOrSttps = len(allOrSttps)
            except:
                allOrSttps = None
                countOrSttps = 0
            args = {}
            args["allOrSttps"] = allOrSttps
            args["countOrSttps"] = countOrSttps
            args["user"] = user
            args["isHOD"] = True
            args["option"] = True
            args["year"] = year
            return render(request, "HOD/facultyQueries/sttpresult.html", args)
        elif option == "Attended":
            try:
                allAtSttps = atSttp.objects.filter(user=user, endDate__year=year)
                countAtSttps = len(allAtSttps)
            except:
                allAtSttps = None
                countAtSttps = 0
            args = {}
            args["allAtSttps"] = allAtSttps
            args["countAtSttps"] = countAtSttps
            args["user"] = user
            args["isHOD"] = True
            args["option"] = False
            args["year"] = year
            try:
                group = Group.objects.get(name="faculty_group")
                usersList = group.user_set.all()
            except:
                group = None
                usersList = None
            args["group"] = group
            args["usersList"] = usersList
            args["isHOD"] = True
            return render(request, "HOD/facultyQueries/sttpresult.html", args)
        return render(request, template_name)

    def post(self, request, year, email, option):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')

        if option == "Organized":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="FacultySttpsOrganizedfile.csv"'
            user = User.objects.get(email=email)
            writer = csv.writer(response)
            writer.writerow(
                ["Faculty Name", "STTP Name", "Domain", "Organizer", "Location", "Mode", "Role", "Start Date",
                 "End Date", "Number of Participants", "Organized/Attended"])
            try:
                allOrSttps = orSttp.objects.filter(user=user, endDate__year=year)
                countOrSttps = len(allOrSttps)
            except:
                allOrSttps = None
                countOrSttps = 0
            for i in allOrSttps:
                if i.mode:
                    mode = "Online"
                else:
                    mode = "Offline"
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.organizer, i.location, mode,
                     i.role, str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                     str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year),
                     i.numberOfParticipants, "Organized" ])

        elif option == "Attended":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="FacultySttpsAttendedfile.csv"'
            user = User.objects.get(email=email)

            writer = csv.writer(response)
            writer.writerow(
                ["Faculty Name", "STTP Name", "Domain", "Organizer", "Location", "Mode", "Start Date",
                 "End Date", "In Or Outside WCE", "Organized/Attended"])
            try:
                allAtSttps = atSttp.objects.filter(user=user, endDate__year=year)
                countAtSttps = len(allAtSttps)
            except:
                allAtSttps = None
                countAtSttps = 0
            try:
                group = Group.objects.get(name="faculty_group")
                usersList = group.user_set.all()
            except:
                group = None
                usersList = None
            for i in allAtSttps:
                if i.mode:
                    mode = "Online"
                else:
                    mode = "Offline"
                if i.inorout:
                    inorout = "In WCE"
                else:
                    inorout = "Outside WCE"
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.organizer, i.location, mode,
                     str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                     str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), inorout, "Attended"])

        return response


################# department queries views ################################

class PaperDeptQueries(View):
    def get(self, request, template_name='HOD/deptQueries/deptPaperQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/deptQueries/deptPaperQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        year = request.POST.get('year')
        st = "Paperqueriesresult/" + year
        return redirect(st)


class PaperDeptQueriesResult(View):
    def get(self, request, year, template_name='HOD/deptQueries/deptPaperQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            allPubPapers = pubPaper.objects.filter(year=year)
            # countPubPapers = len(allPubPapers)
            requiredPapers = []
            for i in allPubPapers:
                # Facu
                devilsCreek = Facu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredPapers.append(i)
            countPubPapers = len(requiredPapers)
        except:
            requiredPapers = None
            countPubPapers = 0
        args = {}
        args["requiredPapers"] = requiredPapers
        args["countPubPapers"] = countPubPapers
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="DepartmentalPublishedPapersfile.csv"'
        allPubPapers = pubPaper.objects.filter(year=year)
        writer = csv.writer(response)
        writer.writerow(["Name", "Paper Title", "Mode", "Conference Name", "startDate", "endDate", "location", "level",
                         "publicationPorR", "publicationtype", "index", "volumenumber", "issuenumber", "isbnissndoi",
                         "pagefrom", "pageto", "month", "year"])
        for i in allPubPapers:
            if i.level:
                level = "International"
            else:
                level = "National"
            if i.mode:
                mode = "Online"
            else:
                mode = "Offline"
            if i.publicationPorR:
                publicationPorR = "Peered-reviewed"
            else:
                publicationPorR = "Referred"
            writer.writerow(
                [i.user.first_name + " " + i.user.last_name, i.papertitle, mode, i.confname,
                 str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                 str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year),
                 i.location, level, publicationPorR, i.publicationtype, i.index, i.volumenumber, i.issuenumber,
                 i.isbnissndoi, i.pagefrom, i.pageto, i.month, i.year])
        return response


class FdpDeptQueries(View):
    def get(self, request, template_name='HOD/deptQueries/deptFdpQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/deptQueries/deptFdpQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        year = request.POST.get('year')
        st = "Fdpqueriesresult/" + year
        return redirect(st)


class FdpDeptQueriesResult(View):
    def get(self, request, year, template_name='HOD/deptQueries/deptFdpQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            allOrFdps = orFdp.objects.filter(endDate__year=year)
            requiredFdps = []
            for i in allOrFdps:
                # Facu
                devilsCreek = Facu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredFdps.append(i)
            countOrFdps = len(requiredFdps)
        except:
            requiredFdps = None
            countOrFdps = 0
        args = {}
        args["requiredFdps"] = requiredFdps
        args["countOrFdps"] = countOrFdps
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="DepartmentalFPDsOrganizedfile.csv"'
        allOrFdps = orFdp.objects.filter(endDate__year=year)
        writer = csv.writer(response)
        writer.writerow(["Name", "Title", "domain", "organizer", "location", "mode", "role", "startDate", "endDate",
                         "numberOfParticipants", ])
        for i in allOrFdps:
            if i.mode:
                mode = "Online"
            else:
                mode = "Offline"
            writer.writerow(
                [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.organizer, i.location, mode, i.role,
                 str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                 str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), i.numberOfParticipants, ])
        return response


class WorkDeptQueries(View):
    def get(self, request, template_name='HOD/deptQueries/deptWorkQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/deptQueries/deptWorkQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        year = request.POST.get('year')
        st = "Workshopqueriesresult/" + year
        return redirect(st)


class WorkDeptQueriesResult(View):
    def get(self, request, year, template_name='HOD/deptQueries/deptWorkQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            allOrWorks = orWork.objects.filter(endDate__year=year)
            requiredWorks = []
            for i in allOrWorks:
                # Facu
                devilsCreek = Facu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredWorks.append(i)
            countOrWorks = len(requiredWorks)
        except:
            requiredWorks = None
            countOrWorks = 0
        args = {}
        args["requiredWorks"] = requiredWorks
        args["countOrWorks"] = countOrWorks
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="DepartmentalWorkshopsOrganizedfile.csv"'
        allOrWorks = orWork.objects.filter(endDate__year=year)
        writer = csv.writer(response)
        writer.writerow(["Name", "Title", "domain", "organizer", "location", "mode", "role", "startDate", "endDate",
                         "numberOfParticipants", ])
        for i in allOrWorks:
            if i.mode:
                mode = "Online"
            else:
                mode = "Offline"
            writer.writerow(
                [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.organizer, i.location, mode, i.role,
                 str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                 str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), i.numberOfParticipants, ])
        return response


class GlDeptQueries(View):
    def get(self, request, template_name='HOD/deptQueries/deptGlQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/deptQueries/deptGlQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        year = request.POST.get('year')
        st = "GuestLecturequeriesresult/" + year
        return redirect(st)


class GlDeptQueriesResult(View):
    def get(self, request, year, template_name='HOD/deptQueries/deptGlQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            allOrGls = GL.objects.filter(date__year=year)
            requiredGls = []
            for i in allOrGls:
                # Facu
                devilsCreek = Facu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredGls.append(i)
            countOrGls = len(requiredGls)
        except:
            requiredGls = None
            countOrGls = 0
        args = {}
        args["requiredGls"] = requiredGls
        args["countOrGls"] = countOrGls
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="DepartmentalGuestLecturesOrganizedfile.csv"'
        allOrGls = GL.objects.filter(date__year=year)
        writer = csv.writer(response)
        writer.writerow(
            ["Name", "Topic", "Domain", "Resource person name", "Resource person profession", "Date", "Beneficiaries",
             "Number Of Participants"])
        for i in allOrGls:
            writer.writerow(
                [i.user.first_name + " " + i.user.last_name, i.topic, i.domain, i.resourcepersonname,
                 i.resourcepersonprofession, str(i.date.day) + "/" + str(i.date.month) + "/" + str(i.date.year),
                 i.beneficiaries, i.numberOfParticipants])
        return response


class WebiDeptQueries(View):
    def get(self, request, template_name='HOD/deptQueries/deptWebiQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/deptQueries/deptWebiQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        year = request.POST.get('year')
        st = "Webinarqueriesresult/" + year
        return redirect(st)


class WebiDeptQueriesResult(View):
    def get(self, request, year, template_name='HOD/deptQueries/deptWebiQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            allOrWebis = orWebi.objects.filter(endDate__year=year)
            requiredWebis = []
            for i in allOrWebis:
                # Facu
                devilsCreek = Facu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredWebis.append(i)
            countOrWebis = len(requiredWebis)
        except:
            requiredWebis = None
            countOrWebis = 0
        args = {}
        args["requiredWebis"] = requiredWebis
        args["countOrWebis"] = countOrWebis
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="DepartmentalWebinarsOrganizedfile.csv"'
        allOrWebis = orWebi.objects.filter(endDate__year=year)
        writer = csv.writer(response)
        writer.writerow(["Name", "Title", "Domain", "organizer", "location", "Mode", "Role", "Start Date", "End Date",
                         "Number Of Participants", ])
        for i in allOrWebis:
            if i.mode:
                mode = "Online"
            else:
                mode = "Offline"
            writer.writerow(
                [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.organizer, i.location, mode, i.role,
                 str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                 str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), i.numberOfParticipants, ])
        return response


class CourseDeptQueries(View):
    def get(self, request, template_name='HOD/deptQueries/deptCourseQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/deptQueries/deptCourseQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        year = request.POST.get('year')
        st = "Coursequeriesresult/" + year
        return redirect(st)


class CourseDeptQueriesResult(View):
    def get(self, request, year, template_name='HOD/deptQueries/deptCourseQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            allComCourses = comCourse.objects.filter(endDate__year=year)
            requiredCourses = []
            for i in allComCourses:
                # Facu
                devilsCreek = Facu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredCourses.append(i)
            countComCourses = len(requiredCourses)
        except:
            requiredCourses = None
            countComCourses = 0
        args = {}
        args["requiredCourses"] = requiredCourses
        args["countComCourses"] = countComCourses
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="DepartmentalOnlineCoursesCompletedfile.csv"'
        allComCourses = comCourse.objects.filter(endDate__year=year)
        writer = csv.writer(response)
        writer.writerow(
            ["Name", "Title", "Domain", "Platform", "Duration weeks", "End Date",
             ])
        for i in allComCourses:
            writer.writerow(
                [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.platform, i.durationweeks,
                 str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), ])
        return response


class SttpDeptQueries(View):
    def get(self, request, template_name='HOD/deptQueries/deptSttpQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/deptQueries/deptSttpQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        year = request.POST.get('year')
        st = "Sttpqueriesresult/" + year
        return redirect(st)


class SttpDeptQueriesResult(View):
    def get(self, request, year, template_name='HOD/deptQueries/deptSttpQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            allOrSttps = orSttp.objects.filter(endDate__year=year)
            requiredSttps = []
            for i in allOrSttps:
                # Facu
                devilsCreek = Facu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredSttps.append(i)
            countOrSttps = len(requiredSttps)
        except:
            requiredSttps = None
            countOrSttps = 0
        args = {}
        args["requiredSttps"] = requiredSttps
        args["countOrSttps"] = countOrSttps
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="DepartmentalSTTPsOrganizedfile.csv"'
        allOrSttps = orSttp.objects.filter(endDate__year=year)
        writer = csv.writer(response)
        writer.writerow(
            ["Name", "Title", "Domain", "Organizer", "Location", "Mode", "Role", "Start Date", "End Date",
             "numberOfParticipants", ])
        for i in allOrSttps:
            if i.mode:
                mode = "Online"
            else:
                mode = "Offline"
            writer.writerow(
                [i.user.first_name + " " + i.user.last_name, i.name, i.domain, i.organizer, i.location, mode, i.role,
                 str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                 str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), i.numberOfParticipants, ])
        return response


##################################### Student Queries ###################################################################
class stuPaperQueries(View):
    def get(self, request, template_name='HOD/studentQueries/stupaperquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/stupaperquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        year = request.POST.get('year')
        st = "PaperqueryResult/" + year
        return redirect(st)


class stuPaperQueryResult(View):
    def get(self, request, year, template_name='HOD/studentQueries/stupaperresult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # user = User.objects.get(email=email)
        try:
            allPubPapers = stuPapers.objects.filter(year=year)
            requiredPapers = []
            for i in allPubPapers:
                # Facu
                devilsCreek = Stu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredPapers.append(i)
            countPubPapers = len(requiredPapers)
        except:
            requiredPapers = None
            countPubPapers = 0
        args = {}
        args["requiredPapers"] = requiredPapers
        args["countPubPapers"] = countPubPapers
        # args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="PublishedPapersfile.csv"'
        allsstuPapers = stuPapers.objects.filter(year=year)
        writer = csv.writer(response)
        writer.writerow(["Student Name", "Paper Title", "PRN", "Conference Name", "Location", "Index", "Level", "Mode",
                         "PeerReviewed OR Referred", "Publication Type", "ISBN/ISSN/DOI", "Start Date",  "End Date", "Month", "Year"])
        for i in allsstuPapers:
            devilsCreek = Stu.objects.filter(user=i.user)
            devilsCreek = devilsCreek[0]
            if devilsCreek.dept == 'CSE':
                if i.level:
                    level = "International"
                else:
                    level = "National"
                if i.mode:
                    mode = "Online"
                else:
                    mode = "Offline"
                if i.publicationPorR:
                    publicationPorR = "Peer-Reviewed"
                else:
                    publicationPorR = "Referred"
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.papertitle, i.user.student.PRN, i.confname,
                     i.location, i.index, level, mode, publicationPorR, i.publicationtype, i.isbnissndoi, str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                     str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year),i.month,
                     i.year, ])
        return response


class stuOnlineCourseQueries(View):
    def get(self, request, template_name='HOD/studentQueries/stuonlinecoursequery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/stuonlinecoursequery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        year = request.POST.get('year')
        st = "OnlineCoursequeryResult/" + year
        return redirect(st)


class stuOnlineCourseQueryResult(View):
    def get(self, request, year, template_name='HOD/studentQueries/stuonlinecourseresult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # user = User.objects.get(email=email)
        try:
            allOnlineCourses = stuOnlineCourses.objects.filter(endDate__year=year)
            requiredOnlineCourses = []
            for i in allOnlineCourses:
                devilsCreek = Stu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredOnlineCourses.append(i)
            countOnlineCourses = len(requiredOnlineCourses)
        except:
            requiredOnlineCourses = None
            countOnlineCourses = 0
        args = {}
        args["requiredOnlineCourses"] = requiredOnlineCourses
        args["countOnlineCourses"] = countOnlineCourses
        # args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # year2 = request.POST.get('year2')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stuOnlineCoursesfile.csv"'
        allOnlineCourses = stuOnlineCourses.objects.filter(endDate__year=year)
        writer = csv.writer(response)
        writer.writerow(["Student Name", "Course Name", "PRN", "Domain", "Platform", "Start Date", "End Date"])
        for i in allOnlineCourses:
            devilsCreek = Stu.objects.filter(user=i.user)
            devilsCreek = devilsCreek[0]
            if devilsCreek.dept == 'CSE':
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.name, i.user.student.PRN, i.domain, i.platform,
                     str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                     str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), ])
        return response


class stuCompQueries(View):
    def get(self, request, template_name='HOD/studentQueries/stucompquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/stucompquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        year = request.POST.get('year')
        st = "CompetitionqueryResult/" + year
        return redirect(st)


class stuCompQueryResult(View):
    def get(self, request, year, template_name='HOD/studentQueries/stucompresult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # user = User.objects.get(email=email)
        try:
            compObjs = stuComps.objects.filter(endDate__year=year, winner=True)
            requiredComps = []
            certsList = []
            for i in compObjs:
                devilsCreek = Stu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    # cert = i.tMemba.all()
                    # certsList.append(cert)
                    requiredComps.append(i)
            countComps = len(requiredComps)
        except:
            requiredComps = None
            countComps = 0

        requiredCerts = []

        for i in requiredComps:
            uss = i.user
            myMan = TeamMember.objects.filter(comps=i)
            myMan = myMan[0]
            requiredCerts.append(myMan)

        print(requiredCerts)

        args = {}

        aayushOP = []

        for mk in range(len(requiredComps)):
            lst = []
            lst.append(requiredComps[mk])
            lst.append(requiredCerts[mk])
            aayushOP.append(lst)

        args["requiredComps"] = aayushOP

        # args["requiredCerts"] = requiredCerts
        # args["requiredComps"] = requiredComps
        # args["certsList"] = certsList
        args["countComps"] = countComps
        # args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # year2 = request.POST.get('year2')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stuCompetitionsfile.csv"'
        allstuPlacementss = stuComps.objects.filter(endDate__year=year, winner=True)
        writer = csv.writer(response)
        writer.writerow(["Student Name", "Competition Name", "PRN", "Organised By", "Location", "Mode", "Project",
                         "Winner/Participant", "Start Date", "End Date", ])
        for i in allstuPlacementss:
            devilsCreek = Stu.objects.filter(user=i.user)
            devilsCreek = devilsCreek[0]
            if devilsCreek.dept == 'CSE':
                if i.winner:
                    winner = "Winner"
                else:
                    winner = "Participant"
                if i.mode:
                    mode = "Online"
                else:
                    mode = "Offline"
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.compname, i.user.student.PRN, i.organizer,
                     i.location,
                     mode, i.projectTitle, winner,
                     str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                     str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), ])
        return response


class InternshipQueries(View):
    def get(self, request, template_name='HOD/studentQueries/InternshipQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/InternshipQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        year = request.POST.get('year')
        type2 = request.POST.get('type2')
        st = "InternshipqueryResult/" + year + "/" + type2
        return redirect(st)


class InternshipQueryResult(View):
    def get(self, request, year, type2, template_name='HOD/studentQueries/InternshipQueryResult.html'):
        group = request.user.groups.all()[0].name
        try:
            if isNotHOD(group):
                return render(request, 'login.html')
            if type2 == "Winter":
                internshipObjs = Interns.objects.filter(endDate__year=year, internshipType=True)
            elif type2 == "Summer":
                internshipObjs = Interns.objects.filter(endDate__year=year, internshipType=False)
            else:
                internshipObjs = Interns.objects.filter(endDate__year=year)
            requiredInterns = []
            for i in internshipObjs:
                devilsCreek = Stu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredInterns.append(i)
            countInterns = len(requiredInterns)
        except:
            requiredInterns = None
            countInterns = 0
        args = {}
        args["requiredInterns"] = requiredInterns
        args["countInterns"] = countInterns
        # args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year, type2):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # year2 = request.POST.get('year2')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="internshipsfile.csv"'
        if type2 == "Winter":
            internshipObjs = Interns.objects.filter(endDate__year=year, internshipType=True)
        elif type2 == "Summer":
            internshipObjs = Interns.objects.filter(endDate__year=year, internshipType=False)
        else:
            internshipObjs = Interns.objects.filter(endDate__year=year)
        writer = csv.writer(response)
        writer.writerow(
            ["Student Name", "Company Name", "Start Date", "End Date", "Domain", "Details", "Mode", "Type"])
        for i in internshipObjs:
            devilsCreek = Stu.objects.filter(user=i.user)
            devilsCreek = devilsCreek[0]
            if devilsCreek.dept == 'CSE':
                if i.mode == True:
                    mas = "Online"
                else:
                    mas = "On-Site"
                if i.internshipType == True:
                    type = "Winter"
                else:
                    type = "Summer"
                writer.writerow([i.user.first_name + " " + i.user.last_name, i.companyName,
                                 str(i.startDate.day) + "/" + str(i.startDate.month) + "/" + str(i.startDate.year),
                                 str(i.endDate.day) + "/" + str(i.endDate.month) + "/" + str(i.endDate.year), i.domain,
                                 i.details, mas, type])
        return response


class PlacementQueries(View):
    def get(self, request, template_name='HOD/studentQueries/PlacementQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/PlacementQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        year = request.POST.get('year')
        st = "PlacementqueryResult/" + year
        return redirect(st)


class PlacementQueryResult(View):
    def get(self, request, year, template_name='HOD/studentQueries/PlacementQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # user = User.objects.get(email=email)
        try:
            allPlacements = stuPlacements.objects.filter(yearPlaced=year)
            requiredPlacements = []
            for i in allPlacements:
                devilsCreek = Stu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredPlacements.append(i)
            countPlacements = len(requiredPlacements)
        except:
            requiredPlacements = None
            countPlacements = 0
        args = {}
        args["requiredPlacements"] = requiredPlacements
        args["countPlacements"] = countPlacements
        # args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # year2 = request.POST.get('year2')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stuPlacementsfile.csv"'
        allstuPlacementss = stuPlacements.objects.filter(yearPlaced=year)
        writer = csv.writer(response)
        writer.writerow(["Student Name", "Company Name", "Year Placed", "Domain", "CTC", "Role"])
        for i in allstuPlacementss:
            devilsCreek = Stu.objects.filter(user=i.user)
            devilsCreek = devilsCreek[0]
            if devilsCreek.dept == 'CSE':
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.companyName, i.yearPlaced, i.domain, i.ctc, i.role])
        return response


class StartupQueries(View):
    def get(self, request, template_name='HOD/studentQueries/StartupQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/StartupQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        year = request.POST.get('year')
        st = "StartupqueryResult/" + year
        return redirect(st)


class StartupQueryResult(View):
    def get(self, request, year, template_name='HOD/studentQueries/StartupQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # user = User.objects.get(email=email)
        try:
            allStartups = Startups.objects.filter(year=year)
            requiredStartups = []
            for i in allStartups:
                devilsCreek = Stu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredStartups.append(i)
            countStartups = len(requiredStartups)
        except:
            requiredStartups = None
            countStartups = 0
        args = {}
        args["requiredStartups"] = requiredStartups
        args["countStartups"] = countStartups
        # args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # year2 = request.POST.get('year2')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Startupsfile.csv"'
        allStartupss = Startups.objects.filter(year=year)
        writer = csv.writer(response)
        writer.writerow(["Student Name", "Company Name", "Year", "Registration Number", "Domain", "Supporting Agency"])
        for i in allStartupss:
            devilsCreek = Stu.objects.filter(user=i.user)
            devilsCreek = devilsCreek[0]
            if devilsCreek.dept == 'CSE':
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.companyName, i.year, i.registrationNumber, i.domain,
                     i.supportingAgency])
        return response


class GREQueries(View):
    def get(self, request, template_name='HOD/studentQueries/GREQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/GREQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        year = request.POST.get('year')
        st = "GREqueryResult/" + year
        return redirect(st)


class GREQueryResult(View):
    def get(self, request, year, template_name='HOD/studentQueries/GREQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # user = User.objects.get(email=email)
        try:
            allGREs = GRE.objects.filter(testDate__year=year)
            requiredGREs = []
            for i in allGREs:
                devilsCreek = Stu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredGREs.append(i)
            countGREs = len(requiredGREs)
        except:
            requiredGREs = None
            countGREs = 0
        args = {}
        args["requiredGREs"] = requiredGREs
        args["countGREs"] = countGREs
        # args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # year2 = request.POST.get('year2')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="GREfile.csv"'
        allGREs = GRE.objects.filter(testDate__year=year)
        writer = csv.writer(response)
        writer.writerow(["Student Name", "Registration Number", "Test Date", "Marks", "Total Marks"])
        for i in allGREs:
            devilsCreek = Stu.objects.filter(user=i.user)
            devilsCreek = devilsCreek[0]
            if devilsCreek.dept == 'CSE':
                writer.writerow([i.user.first_name + " " + i.user.last_name, i.regNo,
                                 str(i.testDate.day) + "/" + str(i.testDate.month) + "/" + str(i.testDate.year),
                                 i.marks, i.totalMarks])
        return response


class TOEFLQueries(View):
    def get(self, request, template_name='HOD/studentQueries/TOEFLQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/TOEFLQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        year = request.POST.get('year')
        st = "TOEFLqueryResult/" + year
        return redirect(st)


class TOEFLQueryResult(View):
    def get(self, request, year, template_name='HOD/studentQueries/TOEFLQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # user = User.objects.get(email=email)
        try:
            allTOEFLs = TOEFL.objects.filter(testDate__year=year)
            requiredTOEFLs = []
            for i in allTOEFLs:
                devilsCreek = Stu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredTOEFLs.append(i)
            countTOEFLs = len(requiredTOEFLs)
        except:
            requiredTOEFLs = None
            countTOEFLs = 0
        args = {}
        args["requiredTOEFLs"] = requiredTOEFLs
        args["countTOEFLs"] = countTOEFLs
        # args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # year2 = request.POST.get('year2')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="TOEFLfile.csv"'
        allTOEFLs = TOEFL.objects.filter(testDate__year=year)
        writer = csv.writer(response)
        writer.writerow(["Student Name", "Registration Number", "Test Date", "Marks", "Total Marks"])
        for i in allTOEFLs:
            devilsCreek = Stu.objects.filter(user=i.user)
            devilsCreek = devilsCreek[0]
            if devilsCreek.dept == 'CSE':
                writer.writerow([i.user.first_name + " " + i.user.last_name, i.regNo,
                                 str(i.testDate.day) + "/" + str(i.testDate.month) + "/" + str(i.testDate.year),
                                 i.marks, i.totalMarks])
        return response


class GATEQueries(View):
    def get(self, request, template_name='HOD/studentQueries/GATEQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/GATEQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        year = request.POST.get('year')
        st = "GATEqueryResult/" + year
        return redirect(st)


class GATEQueryResult(View):
    def get(self, request, year, template_name='HOD/studentQueries/GATEQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # user = User.objects.get(email=email)
        try:
            allGATEs = GATE.objects.filter(testDate__year=year, qualified=True)
            requiredGATEs = []
            for i in allGATEs:
                devilsCreek = Stu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredGATEs.append(i)
            countGATEs = len(requiredGATEs)
        except:
            requiredGATEs = None
            countGATEs = 0
        args = {}
        args["requiredGATEs"] = requiredGATEs
        args["countGATEs"] = countGATEs
        # args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # year2 = request.POST.get('year2')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="GATEfile.csv"'
        allGATEs = GATE.objects.filter(testDate__year=year, qualified=True)
        writer = csv.writer(response)
        writer.writerow(["Student Name", "Seat Number", "Test Date", "Marks", "Rank", "Qualified", ])
        for i in allGATEs:
            if i.qualified:
                qualified = "Yes"
            else:
                qualified = "No"
            devilsCreek = Stu.objects.filter(user=i.user)
            devilsCreek = devilsCreek[0]
            if devilsCreek.dept == 'CSE':
                writer.writerow([i.user.first_name + " " + i.user.last_name, i.seatNo,
                                 str(i.testDate.day) + "/" + str(i.testDate.month) + "/" + str(i.testDate.year),
                                 i.marks, i.rank, qualified, ])
        return response


class ProjectQueries(View):
    def get(self, request, template_name='HOD/studentQueries/projectquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/projectquery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        year = request.POST.get('year')
        st = "SocialProjectqueryResult/" + year
        return redirect(st)


class ProjectQueryResult(View):
    def get(self, request, year, template_name='HOD/studentQueries/socialprojectqueryresult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # user = User.objects.get(email=email)
        try:
            allProjects = Proj.objects.filter(year=year, socialCause=True)
            requiredProjects = []
            for i in allProjects:
                devilsCreek = Stu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredProjects.append(i)
            countProjects = len(requiredProjects)
        except:
            requiredProjects = None
            countProjects = 0
        args = {}
        args["requiredProjects"] = requiredProjects
        args["countProjects "] = countProjects
        # args["user"] = user
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="projectfile.csv"'
        allProjects = Proj.objects.filter(year=year, socialCause=True)
        writer = csv.writer(response)
        writer.writerow(
            ["Student Name", "Project Title", "Year", "Domain", "Semester", "Guide Name", "Cause", "Customer"])
        for i in allProjects:
            devilsCreek = Stu.objects.filter(user=i.user)
            devilsCreek = devilsCreek[0]
            if devilsCreek.dept == 'CSE':
                writer.writerow([i.user.first_name + " " + i.user.last_name, i.title, str(i.year), i.domain, i.semester,
                                 i.guideName, i.cause, i.customer])
        return response


# remaining to change in post function of projectresult

class GraduationQueries(View):
    def get(self, request, template_name='HOD/studentQueries/graduationQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/graduationQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        yearOfEnrollment = request.POST.get('yearOfEnrollment')
        yearOfGraduation = request.POST.get('yearOfGraduation')
        st = "GraduationQueryResult/" + yearOfEnrollment + "-" + yearOfGraduation
        return redirect(st)


class GraduationQueryResult(View):
    def get(self, request, yearOfEnrollment, yearOfGraduation,
            template_name='HOD/studentQueries/graduationQueryResult.html'):
        global countGrads, requiredGrads
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # user = User.objects.get(email=email)
        try:
            allGrads = Stu.objects.filter(yearOfEnrollment=yearOfEnrollment, yearOfGraduation=yearOfGraduation)
            requiredGrads = []
            for i in allGrads:
                devilsCreek = Stu.objects.filter(user=i.user)
                devilsCreek = devilsCreek[0]
                if devilsCreek.dept == 'CSE':
                    requiredGrads.append(i)
            countGrads = len(requiredGrads)
        except:
            requiredGrads = None
            countGrads = 0
        args = {}
        args["requiredGrads"] = requiredGrads
        args["countGrads"] = countGrads
        # args["user"] = user
        args["isHOD"] = True
        args["yearOfEnrollment"] = yearOfEnrollment
        args["yearOfGraduation"] = yearOfGraduation
        return render(request, template_name, args)

    def post(self, request, yearOfEnrollment, yearOfGraduation):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="graduation.csv"'
        allGrads = Stu.objects.filter(yearOfEnrollment=yearOfEnrollment, yearOfGraduation=yearOfGraduation)
        writer = csv.writer(response)
        writer.writerow(
            ["Student Name", "PRN", "Year of Enrollment", "Year of Graduation"])
        for i in allGrads:
            devilsCreek = Stu.objects.filter(user=i.user)
            devilsCreek = devilsCreek[0]
            if devilsCreek.dept == 'CSE':
                writer.writerow(
                    [i.user.first_name + " " + i.user.last_name, i.PRN, i.yearOfEnrollment, i.yearOfGraduation])
        return response


class studentsUpdated(View):
    def get(self, request, template_name='HOD/studentQueries/studentsUpdated.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/studentsUpdated.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        year = request.POST.get('year')
        st = "studentsUpdatedResult/" + year
        return redirect(st)


class studentsUpdatedResult(View):
    def get(self, request, year, template_name='HOD/studentQueries/studentsUpdatedResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            allUsers = User.objects.filter(last_login__year=year)
            requiredGREs = []
            for i in allUsers:
                devilsCreek = Stu.objects.filter(user=i)
                try:
                    devilsCreek = devilsCreek[0]
                except:
                    continue
                if devilsCreek.dept == 'CSE':
                    requiredGREs.append(Stu.objects.filter(user=i)[0])
            countGREs = len(requiredGREs)
        except:
            requiredGREs = None
            countGREs = 0
        args = {}
        args["requiredGREs"] = requiredGREs
        args["countGREs"] = countGREs
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="StudentsUpdatedDetailsfile.csv"'
        allUsers = User.objects.filter(last_login__year=year)
        writer = csv.writer(response)
        writer.writerow(["Student Name", "PRN", "Email"])
        for i in allUsers:
            devilsCreek = Stu.objects.filter(user=i)
            try:
                devilsCreek = devilsCreek[0]
            except:
                continue
            if devilsCreek.dept == 'CSE':
                val = Stu.objects.filter(user=i)[0]
                writer.writerow([val.user.first_name + " " + val.user.last_name, val.PRN, val.user.email])
        return response


class studentsNotUpdated(View):
    def get(self, request, template_name='HOD/studentQueries/studentsNotUpdated.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
        except:
            group = None
        args = {}
        args["group"] = group
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/studentsNotUpdated.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        year = request.POST.get('year')
        st = "studentsNotUpdatedResult/" + year
        return redirect(st)


class studentsNotUpdatedResult(View):
    def get(self, request, year, template_name='HOD/studentQueries/studentsNotUpdatedResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            allUsers = User.objects.filter(~Q(last_login__year=year))
            requiredGREs = []
            for i in allUsers:
                devilsCreek = Stu.objects.filter(user=i)
                try:
                    devilsCreek = devilsCreek[0]
                except:
                    continue
                if devilsCreek.dept == 'CSE':
                    requiredGREs.append(Stu.objects.filter(user=i)[0])
            countGREs = len(requiredGREs)
        except:
            requiredGREs = None
            countGREs = 0
        args = {}
        args["requiredGREs"] = requiredGREs
        args["countGREs"] = countGREs
        args["isHOD"] = True
        args["year"] = year
        return render(request, template_name, args)

    def post(self, request, year):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="StudentsNotUpdatedDetailsfile.csv"'
        allUsers = User.objects.filter(~Q(last_login__year=year))
        writer = csv.writer(response)
        writer.writerow(["Student Name", "PRN", "Email"])
        for i in allUsers:
            devilsCreek = Stu.objects.filter(user=i)
            try:
                devilsCreek = devilsCreek[0]
            except:
                continue
            if devilsCreek.dept == 'CSE':
                val = Stu.objects.filter(user=i)[0]
                writer.writerow([val.user.first_name + " " + val.user.last_name, val.PRN, val.user.email])
        return response


# In DEPT Queries########################################
# Names of PE offered in a specific sem of a specific year
class PEQueries(View):
    def get(self, request, template_name='HOD/deptQueries/PEQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            group = Group.objects.get(name="student_group")
            # usersList = group.user_set.all()
        except:
            group = None
            # usersList = None
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/deptQueries/PEQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        acadYear = request.POST.get('acadYear')  # FY SY etc
        year = request.POST.get('year')  # 2020 2021 etc
        sem = request.POST.get('sem')
        st = "PEQueryResult/" + year + "/" + acadYear + "/" + sem
        return redirect(st)


class PEQueryResult(View):
    def get(self, request, acadYear, sem, year, template_name='HOD/deptQueries/PEQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            allPEs = PEs.objects.filter(acadYear=acadYear, sem=sem, year=year)
            requiredPEs = allPEs[::1]
            countPEs = len(requiredPEs)
        except:
            requiredPEs = None
            allPEs = None
            countPEs = 0
        args = {}
        args["requiredPEs"] = requiredPEs
        args["countPEs"] = countPEs
        args["isHOD"] = True
        args["acadYear"] = acadYear
        args["sem"] = sem
        args["year"] = year
        return render(request, template_name, args)


##############Put in Student Queries##########
# a) Number of students enrolled for specific PE in a specific semester in a specific year.
# b) Details of students enrolled for a specific PE in a specific semester in a specific year.(Keep this list downloadable)
class PEStuQueries(View):
    def get(self, request, template_name='HOD/studentQueries/PEStuQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            allPEs = PEs.objects.all()
            requiredPEs = allPEs[::1]
            countPEs = len(requiredPEs)
        except:
            requiredPEs = None
            allPEs = None
            countPEs = 0
        args = {}
        args["requiredPEs"] = requiredPEs
        args["countPEs"] = countPEs
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/PEStuQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        # email = request.POST.get('email')
        acadYear = request.POST.get('acadYear')  # FY SY etc
        year = request.POST.get('year')  # 2020 2021 etc
        sem = request.POST.get('sem')
        courseCode = request.POST.get('courseCode')
        st = "PEStuQueryResult/" + year + "/" + acadYear + "/" + sem + "/" + courseCode
        return redirect(st)


class PEStuQueryResult(View):
    def get(self, request, acadYear, sem, year, courseCode, template_name='HOD/studentQueries/PEStuQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        try:
            allPEs = PEs.objects.filter(acadYear=acadYear, sem=sem, year=year, courseCode=courseCode)
            courseName: object = allPEs[0].courseName
            requiredPEs = []
            for i in allPEs:
                devilsCreek = PETakenByStudent.objects.filter(PE=i)
                for j in devilsCreek:
                    requiredPEs.append(j)
            countPEs = len(requiredPEs)
        except:
            requiredPEs = None
            allPEs = None
            courseName = None
            countPEs = 0
        args = {}
        args["requiredPEs"] = requiredPEs
        args["countPEs"] = countPEs
        args["isHOD"] = True
        args["acadYear"] = acadYear
        args["sem"] = sem
        args["year"] = year
        args["courseCode"] = courseCode
        args["courseName"] = courseName
        return render(request, template_name, args)

    def post(self, request, acadYear, sem, year, courseCode, template_name='HOD/studentQueries/PEStuQueryResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="PE.csv"'
        writer = csv.writer(response)
        writer.writerow(["Student Name", "PRN", "PE Name", "PE Code", "Academic Year", "Semester", "Year"])
        try:
            allPEs = PEs.objects.filter(acadYear=acadYear, sem=sem, year=year, courseCode=courseCode)
            requiredPEs = []
            for i in allPEs:
                devilsCreek = PETakenByStudent.objects.filter(PE=i)
                # print(devilsCreek)
                for j in devilsCreek:
                    requiredPEs.append(j)
        except:
            requiredPEs = None
        for i in requiredPEs:
            writer.writerow(
                [i.student.user.first_name + " " + i.student.user.last_name, i.student.PRN, i.PE.courseName,
                 i.PE.courseCode, i.PE.acadYear, i.PE.sem, i.PE.year])
        return response


###################Complete Data of Individual Student###############################
class completeSTUQuery(View):
    def get(self, request, template_name='HOD/studentQueries/completeSTUQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        args["group"] = group
        # args["usersList"] = usersList
        args["isHOD"] = True
        return render(request, template_name, args)

    def post(self, request, template_name='HOD/studentQueries/completeSTUQuery.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        PRN = request.POST.get('PRN').upper()
        st = "completeSTUResult/" + PRN
        return redirect(st)


class completeSTUResult(View):
    def get(self, request, PRN, template_name='HOD/studentQueries/completeSTUResult.html'):
        group = request.user.groups.all()[0].name
        if isNotHOD(group):
            return render(request, 'login.html')
        args = {}
        try:

            stuObj = Stu.objects.get(PRN=PRN)
            userObj = stuObj.user

            try:

                allCourses = stuOnlineCourses.objects.filter(user=userObj)
                countCourses = len(allCourses)
            except:
                allCourses = None
                countCourses = 0

            args["allCourses"] = allCourses
            args["countCourses"] = countCourses

            try:
                allWebinars = Webi.objects.filter(user=userObj)
                countWebinars = len(allWebinars)
            except:
                allWebinars = None
                countWebinars = 0

            args["allWebinars"] = allWebinars
            args["countWebinars"] = countWebinars

            try:
                allWorkshops = Work.objects.filter(user=userObj)
                countWorkshops = len(allWorkshops)
            except:
                allWorkshops = None
                countWorkshops = 0

            args["allWorkshops"] = allWorkshops
            args["countWorkshops"] = countWorkshops

            try:
                allCompetitions = stuComps.objects.filter(user=userObj)
                countCompetitions = len(allCompetitions)
            except:
                allCompetitions = None
                countCompetitions = 0

            args["allCompetitions"] = allCompetitions
            args["countCompetitions"] = countCompetitions

            try:
                allPapers = stuPapers.objects.filter(user=userObj)
                countPapers = len(allPapers)
            except:
                allPapers = None
                countPapers = 0

            args["allPapers"] = allPapers
            args["countPapers"] = countPapers

            try:
                allTOEFL = TOEFL.objects.filter(user=userObj)
                countTOEFL = len(allTOEFL)
            except:
                allTOEFL = None
                countTOEFL = 0

            args["allTOEFL"] = allTOEFL
            args["countTOEFL"] = countTOEFL

            try:

                allGATE = GATE.objects.filter(user=userObj)
                countGATE = len(allGATE)
            except:
                allGATE = None
                countGATE = 0

            args["allGATE"] = allGATE
            args["countGATE"] = countGATE

            try:
                allGRE = GRE.objects.filter(user=userObj)
                countGRE = len(allGRE)
            except:
                allGRE = None
                countGRE = 0

            args["allGRE"] = allGRE
            args["countGRE"] = countGRE

            try:
                allInternship = Interns.objects.filter(user=userObj)
                countInternship = len(allInternship)
            except:
                allInternship = None
                countInternship = 0

            args["allInternship"] = allInternship
            args["countInternship"] = countInternship

            try:

                allStartUp = Startups.objects.filter(user=userObj)
                countStartUp = len(allStartUp)
            except:
                allStartUp = None
                countStartUp = 0

            args["allStartUp"] = allStartUp
            args["countStartUp"] = countStartUp

            try:
                allPlacements = stuPlacements.objects.filter(user=userObj)
                countPlacements = len(allPlacements)
            except:
                allPlacements = None
                countPlacements = 0

            args["allPlacements"] = allPlacements
            args["countPlacements"] = countPlacements

            try:
                allProjects = Proj.objects.filter(user=userObj)
                countProjects = len(allProjects)
            except:
                allProjects = None
                countProjects = 0

            args["allProjects"] = allProjects
            args["countProjects"] = countProjects

            try:
                allPEs = PETakenByStudent.objects.filter(student=stuObj)
                countPEs = len(allPEs)
            except:
                allPEs = None
                countPEs = 0

            args["allPEs"] = allPEs
            args["countPEs"] = countPEs
            countStu = 1
        except:
            countStu = 0
            userObj = None
        # logic -> count =0 no student exist
        args["countStu"] = countStu
        args["isHOD"] = True
        args['userObj'] = userObj

        return render(request, template_name, args)


def delete_items(request, ido, pagetype):
    if request.method == 'POST':
        if pagetype == "CourseExitSurveys":
            group = request.user.groups.all()[0].name
            if isNotHOD(group):
                return render(request, 'login.html')
            else:
                thatCourse = CourseES.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "Course Exit Survey Deleted Successfully"
                try:
                    user = request.user
                    allCourseES = CourseES.objects.filter(user=user)
                    countCourseES = len(allCourseES)
                except:
                    allCourseES = None
                    countCourseES = 0
                args = {}
                args["allCourseES"] = allCourseES
                args["countCourseES"] = countCourseES
                return redirect('../../CourseExitSurveys')

        elif pagetype == "DepartmentFeedbackSurveys":
            group = request.user.groups.all()[0].name
            if isNotHOD(group):
                return render(request, 'login.html')
            else:
                thatCourse = DeptFS.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "Dept Feedback Survey Deleted Successfully"
                try:
                    user = request.user
                    allDeptFS = DeptFS.objects.filter(user=user)
                    countDeptFS = len(allDeptFS)
                except:
                    allDeptFS = None
                    countDeptFS = 0
                args = {}
                args["allDeptFS"] = allDeptFS
                args["countDeptFS"] = countDeptFS
                return redirect('../../DepartmentFeedbackSurveys')

        elif pagetype == "GraduationExitSurveys":
            group = request.user.groups.all()[0].name
            if isNotHOD(group):
                return render(request, 'login.html')
            else:
                thatCourse = GradES.objects.filter(id=ido).delete()
                args = {}
                args["error_message"] = "Graduation Exit Survey Deleted Successfully"
                try:
                    user = request.user
                    allGradES = GradES.objects.filter(user=user)
                    countGradES = len(allGradES)
                except:
                    allGradES = None
                    countGradES = 0
                args = {}
                args["allGradES"] = allGradES
                args["countGradES"] = countGradES
                return redirect('../../GraduationExitSurveys')

    return render(request, 'delete_itemsIO.html', {'pagetype': pagetype})
