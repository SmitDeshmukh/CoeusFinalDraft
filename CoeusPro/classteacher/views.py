import os
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic.base import View
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from classteacher.models import PETakenByStudent
import datetime
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from student.models import student as Student
from classteacher.models import PEs as PES
import csv
from io import TextIOWrapper


class ClassTeacherHome(View):
    def get(self, request, template_name="FacultyHome.html"):
        return render(request, template_name)


def isNotStudent(group_name):
    if group_name == 'student_group':
        return False
    else:
        return True


class addStudents(View):
    def get(self, request, template_name="AddStudents.html"):
        return render(request, template_name)

    def post(self, request, template_name="AddStudents.html"):
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
            PRN = row[3]
            year = row[4]  # current Year
            semester = row[5]
            yearOfEnrollment = row[6]
            yearOfGraduation = row[7]
            dept = row[8]
            email = row[9]
            password = row[10]
            isDA = row[11]
            if isDA == "YES":
                isDA = True
            else:
                isDA = False
            try:
                # create user

                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    # print(user)
                    # update student info and save
                    student = Student.objects.get(user=user)
                    student.PRN = PRN
                    student.year = year  # current year
                    student.semester = semester
                    student.yearOfEnrollment = yearOfEnrollment
                    student.yearOfGraduation = yearOfGraduation
                    student.dept = dept
                    student.isDA = isDA
                    student.save()
                    # err = {'error_message': "Existing Students Updated"}
                else:
                    user = User.objects.create_user(username, email, password, first_name=first_name,
                                                    last_name=last_name, )
                    user.save()
                    # create student
                    studentData = Student(user=user, PRN=PRN, dept=dept, year=year, semester=semester,
                                          yearOfEnrollment=yearOfEnrollment, yearOfGraduation=yearOfGraduation,
                                          isDA=isDA, )
                    studentData.save()
                    # assign group
                    my_group = Group.objects.get(name='student_group')
                    my_group.user_set.add(user)
                    # err = {'error_message': "Students Added successfully."}
            except:
                cantBeAdded.append(username)

        err = {'error_message': "Students Added/Updated successfully.", 'cantBeAdded': cantBeAdded}
        return render(request, template_name, err)


class viewPEs(View):
    def get(self, request, template_name='viewPEs.html'):
        group = request.user.groups.all()[0].name
        if group != 'classTeacher_group':
            return render(request, 'login.html')
        try:
            allPEs = PES.objects.all()
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
        group = request.user.groups.all()[0].name
        if group != 'classTeacher_group':
            return render(request, 'login.html')
        else:
            # ido = request.POST.get('ido')
            thatPE = PES.objects.filter(id=ido).delete()
            args = {}
            args["error_message"] = "PE Deleted Successfully"
            try:
                allPEs = PES.objects.all()
                countPEs = len(allPEs)
            except:
                allPEs = None
                countPEs = 0
            args = {}
            args["allPEs"] = allPEs
            args["countPEs"] = countPEs
            return redirect('../../viewPEs')
    return render(request, 'delete_items.html', {"pagetype":pagetype})


class addPEs(View):
    def get(self, request, template_name='PEs.html'):
        group = request.user.groups.all()[0].name
        if group != 'classTeacher_group':
            return render(request, 'login.html')
        return render(request, template_name)

    def post(self, request, template_name='PEs.html'):
        group = request.user.groups.all()[0].name
        if group != 'classTeacher_group':
            return render(request, 'login.html')
        year = request.POST.get('year')
        sem = request.POST.get('sem')
        courseName = request.POST.get('courseName')
        courseCode = request.POST.get('courseCode')
        acadYear = request.POST.get('acadYear')
        PESsaved = PES(year=year, sem=sem, courseName=courseName, courseCode=courseCode, acadYear=acadYear)
        PESsaved.save()
        err = {'error_message': "Professional Elective Added Successfully."}
        return render(request, template_name, err)

# class PE(View):
#     def get(self, request, template_name='student/PE.html'):
#         group = request.user.groups.all()[0].name
#         if isNotStudent(group):
#             return render(request, 'login.html')
#         else:
#             try:
#                 user = request.user
#                 Studentobj = user.student
#                 allPEs = PETakenByStudent.objects.filter(student=Studentobj)
#                 countPEs = len(allPEs)
#             except:
#                 allPEs = None
#                 countPEs = 0
#             args = {}
#             args["allPEs"] = allPEs
#             args["countPEs"] = countPEs
#             return render(request, template_name, args)


#########################Assinging PEs to Students through CSV################################
class assignPE(View):
    def get(self, request, template_name="AssignPEs.html"):
        return render(request, template_name)

    def post(self, request, template_name="AssignPEs.html"):
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
            PRN = row[0]
            courseCode = row[1]
            try:
                student = Student.objects.get(PRN=PRN)
                PEobj = PES.objects.get(courseCode=courseCode)
                PETakenByStudentobj = PETakenByStudent(PE=PEobj, student=student)
                PETakenByStudentobj.save()
            except:
                cantBeAdded.append(PRN)
        err = {'error_message': "PEs assigned Successfully.", 'cantBeAdded': cantBeAdded}
        return render(request, template_name, err)
