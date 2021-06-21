"""mySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# url patterns
urlpatterns = [

    # default root
    path('', views._login, name="dashboard"),

    path('signup', views._signup, name="signup"),

    path('dashboard', views.index, name="dashboard"),

    # add class
    path('addclass',
         views.student_classes_create, name="createClass"),

    # Class list
    path('classlist',
         views.student_classes_manage, name="manageClass"),

    # Update class
    path('updateClass/<int:id>', views.updateClass, name="updateClass"),

    # delete record
    path('deleteClass/<int:id>', views.student_classes_delete, name="deleteClass"),

    # edit class
    path('editclass/<int:id>', views.editclass, name='editclass'),

    # login
    path('login', views._login, name="login"),

    # logout
    path('logout', views._logout, name='logout'),

    # recover password
    path('forgotpassword', views.recover_password, name="forgotpassword"),

    # change password
    path('resetpassword', views.reset_password, name="resetpassword"),

    # add student
    path('addstudent', views.add_student, name="addstudent"),

    # manage student
    path('managestudent', views.manage_student, name="managestudent"),

    # delete subject
    path('deletestudent/<int:id>', views.delete_student, name="deletestudent"),

    # edit student
    path('editstudent/<int:id>', views.editstudent, name='editstudent'),

    # update student
    path('updatestudent/<int:id>', views.updatestudent, name='updatestudent'),

    # add result
    path('addresult', views.add_result, name="addresult"),

    # show result
    path('showresult', views.show_result, name="showresult"),

    # manage result
    path('manageresult/<int:id>', views.manage_result, name="manageresult"),

    # delete result
    path('deleteresult/<int:id>', views.delete_result, name="deleteresult"),

    # update result
    path("updateresult/<int:id>", views.update_result, name="updateresult"),

    # time table
    path('timetable', views.time_table, name="Timetable"),

    # change time table
    path('changetimetable/<int:id>',
         views.change_time_table, name="changeTimetable"),

    # update time table
    path('updatetimetable/<int:id>',
         views.update_time_table, name="updateTimetable"),

    # add subject
    path('createsubject', views.add_subject, name="createsubject"),

    # manage subject
    path('managesubject', views.manage_subject, name="managesubject"),

    # edit subject
    path('editsubject/<int:id>', views.edit_subject, name="editsubject"),

    # update subject
    path('updatesubject/<int:id>', views.update_subject, name="updatesubject"),

    # delete subject
    path('deletesubject/<int:id>', views.subject_delete, name="deletesubject"),

    ################# reset passsword views ###################

    # path("password_reset", views.password_reset_request, name="password_reset"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # media folder
