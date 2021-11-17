import os
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views import generic
from django.views.generic.base import View
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
import shortuuid
from django.http import HttpResponseRedirect
from student.models import student
from teacher.models import faculty as teacher
# from .forms import GeneralForm
from student.models import student as Student
from teacher.models import faculty


# Create your views here.
def home(request):
    return render(request, 'CoeusHome.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        group = None
        if user is not None:
            if user.is_active:
                login(request, user)
                userr = Group.objects.filter(user=user)
                group = user.groups.all()[0].name
                if group == 'faculty_group':
                    return redirect('teacher:facultyHome')
                if group == 'student_group':
                    return redirect('student:studentHome')
                if group == 'HOD_group':
                    return redirect('HOD:HODHome')
                if group == 'classTeacher_group':
                    return redirect('classteacher:ClassTeacherHome')
                else:
                    return render(request, 'CoeusHome.html', {})
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return render(request, 'CoeusHome.html', {})


def belongsto(request, user):
    group = request.user.groups.all()[0].name
    if group == 'faculty_group':
        return render(request, 'facultyprofile.html', {'faculty': request.user.faculty})
    if group == 'student_group':
        return render(request, 'studentprofile.html', {'student': request.user.student})

    else:
        return render(request, 'CoeusHome.html', {})


# Change password for student and faculty
class changePassword(View):

    def get(self, request, template_name="changepassword.html"):
        return render(request, template_name)

    def post(self, request, template_name="changepassword.html"):
        currPassword = request.POST.get('currentPassword')
        newPassword = request.POST.get('newPassword')
        confPassword = request.POST.get('reNewPassword')

        try:
            matchcheck = check_password(currPassword, request.user.password)
            if matchcheck is False:
                err = {}
                err["error_message"] = "Entered Current Password is Incorrect. Please Retry."
                return render(request, template_name, err)
            if newPassword != confPassword:
                err = {}
                err["error_message"] = "Entered New Passwords don't Match. Please Retry."
                return render(request, template_name, err)
        except:
            err = {}
            err["error_message"] = "Refresh the Page to change the Password Again."
            return render(request, template_name, err)

        # U = User.objects.get(username=request.user.username)
        U = request.user
        U.set_password(newPassword)
        U.save()
        update_session_auth_hash(request, U)
        err = {}
        # err["student"] = stud
        err["error_message"] = "Password changed successfully."
        group = request.user.groups.all()[0].name
        if group == 'faculty_group':
            return render(request, 'facultyprofile.html', {'faculty': request.user.faculty})
        if group == 'student_group':
            return render(request, 'studentprofile.html', {'student': request.user.student})
