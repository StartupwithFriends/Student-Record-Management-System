from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import signup, TimeTable, StudentClass, AddStudent, AddSubject, Result
from verify_email import verify_email
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

########## Home Page #########

# dashboard


@login_required
def index(request):
    # if request.user.is_authenticated:
    # post request not working

    # current logged in user
    user = request.user

    # total classes listed
    class_listed = StudentClass.objects.filter(user=user).count
    # total students count
    student_count = AddStudent.objects.filter(user=user).count
    # total subject counts
    subj_count = AddSubject.objects.filter(user=user).count
    # total subject count
    res = Result.objects.filter(user=user).count

    if request.method == 'POST':
        context = {'user': user, 'class_listed': class_listed,
                   'student_count': student_count, 'subj_count': subj_count, 'res': res}
        return render(request, 'dashboard/index.html', context)
    else:
        context = {'user': user, 'class_listed': class_listed,
                   'student_count': student_count, 'subj_count': subj_count, 'res': res}
        return render(request, 'dashboard/index.html', context)

########### student classes ##########

# create class


@login_required
def student_classes_create(request):
    if request.method == "POST":
        name = request.POST["className"]
        num = request.POST["classNum"]
        sec = request.POST["classSec"]
        # print(name, num, sec)
        class_ = StudentClass(className=name, classNum=num, classSec=sec)
        class_.user = request.user
        class_.save()
        done = "Record Created !!!"
        return render(request, 'studentClasses/CreateClass.html', {'user': request.user, 'done': done})
    return render(request, 'studentClasses/CreateClass.html', {'user': request.user})

# manage class


@login_required
def student_classes_manage(request):
    # info
    addcls = StudentClass.objects.filter(user=request.user)
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            addcls = StudentClass.objects.filter(Q(className__icontains=q) | Q(classNum__icontains=q) | Q(
                classSec__icontains=q))
            count = addcls.count()
            addcls.user = request.user
            return render(request, 'studentClasses/ManageClass.html', {'addcls': addcls, 'count': count})
        else:
            return render(request, 'studentClasses/ManageClass.html', {'addcls': addcls, 'count': 0})
            # return data on html
    return render(request, 'studentClasses/ManageClass.html', {'addcls': addcls, 'count': 0})

# edit class


@login_required
def editclass(request, id):
    info = StudentClass.objects.get(id=id)
    return render(request, 'studentClasses/updateClass.html', {'info': info})

# update class


@login_required
def updateClass(request, id):
    if request.method == "POST":
        info = StudentClass.objects.get(id=id)
        info.className = request.POST['className']
        info.classNum = request.POST['classNum']
        info.classSec = request.POST['classSec']
        info.save()
        return redirect('manageClass')
    return redirect('manageClass')


# delete record studentclass

@login_required
def student_classes_delete(request, id):
    # only get request working
    # if request.method == "POST":
    pi = StudentClass.objects.get(id=id)
    pi.delete()
    return redirect('manageClass')
########## User Authentication ##########

# signup


def _signup(request):
    # make a POST request
    if request.method == 'POST':
        # fetching all form details
        username = request.POST['username']
        first = request.POST['first_name']
        last = request.POST['last_name']
        email = request.POST['user_email']
        password = request.POST['user_password']
        password1 = request.POST['user_confirm_password']
        # img = request.POST['user_img']
        # profile_picture = request.FILES['user_img']
        # check username length and password
        if not username.isalpha():
            messages.info(request, "Username can't contain special characters")
            return redirect('signup')
        # len of username should be smaller than 20
        if len(username) > 20:
            messages.info(request, "Username too long")
            return redirect('signup')
        # if username already exists
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username taken')
            return redirect('signup')
        # check for email
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already taken')
            return redirect('signup')
        # if email is invalid
        if verify_email(email) != True:
            messages.info(request, "Enter a valid email")
            return redirect('signup')
        # if password field doesn't match
        if password != password1:
            messages.info(request, "Password doesn't match !")
            return redirect('signup')
        # else create a new account
        else:
            # creating the user model
            user = User.objects.create_user(
                username=username, password=password, email=email)
            # set form password to user password
            user.set_password(password)
            # by default with user model in django
            user.first_name = first
            # by default with user model in django
            user.last_name = last
            # user profile picture
            # user.picture = img
            # save the user here
            user.save()
            # if condition true redirect to login page
            return redirect('login')
            # messages.info(request, f"User is created for {first} {last}")
    else:
        return render(request, 'user/Signup/signup.html')

# login


def _login(request):
    # make a POST request
    if request.method == 'POST':
        # fetching user credentials
        username = request.POST['username']
        password = request.POST['password']
        # checking the credentials
        user = auth.authenticate(username=username, password=password)
        # check is user already exists
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        # check if user exists
        else:
            messages.info(request, "Invalid Credentials !")
            return redirect('login')

    return render(request, 'user/Login_v2/index.html')

# logout


@login_required
def _logout(request):
    # if user is authenticated or logged in
    # redirect user to login page after logout
    if request.user.is_authenticated:
        # post request working
        if request.method == 'POST':
            auth.logout(request)
            return redirect('login')
        # get request working
        else:
            auth.logout(request)
            return redirect('login')
    # if user not authenticated
    else:
        return redirect('login')

# recover password


@login_required
def recover_password(request):
    return render(request, 'user/forgotpassword.html')

# change password


@login_required
def reset_password(request):
    return render(request, 'user/reset/reset.html')


########### Time Table ###########

# global variable
x = 0


@login_required
# time table
def time_table(request):
    global x
    # fetch all timetable columns
    # tt = TimeTable.objects.all()
    # fetch all timetable form column
    if request.method == "POST":
        day = request.POST['day']
        p1 = request.POST['period1']
        p2 = request.POST['period2']
        p3 = request.POST['period3']
        p4 = request.POST['period4']
        p5 = request.POST['period5']
        p6 = request.POST['period6']
        # tt is TimeTable instance
        tt = TimeTable(day=day, period1=p1, period2=p2,
                       period3=p3, period4=p4, period5=p5, period6=p6)
        tt.user = request.user
        tt.save()
    # TimeTable database all info
    user = request.user
    # fetch specific user timetable data
    td = TimeTable.objects.filter(user=user)[0:8]
    td_count = TimeTable.objects.all().count
    x += 1
    context = {'user': request.user, 'td': td, 'td_count': td_count, 'x': x}
    return render(request, 'timetable/index.html', context)

# change time table


@login_required
def change_time_table(request, id):
    tt = TimeTable.objects.filter(id=id)
    context = {'user': request.user, 'tt': tt}
    return render(request, 'timetable/change_timetable.html', context)


# update time table
@login_required
def update_time_table(request, id):
    # update the record here
    time_table = TimeTable.objects.get(id=id)
    # update day ??
    # update periods acc to days
    time_table.period1 = request.POST['p1']
    time_table.period2 = request.POST['p2']
    time_table.period3 = request.POST['period3']
    time_table.period4 = request.POST['period4']
    time_table.period5 = request.POST['period5']
    time_table.period6 = request.POST['period6']
    time_table.save()
    print("changed successfully !")
    return redirect('Timetable')


########## Student ##########

# add student


@login_required
def add_student(request):
    # there is a bug while adding record here
    # two record gets added and deleted together
    context = {'user': request.user}
    if request.method == "POST":
        name = request.POST['full_name']
        roll = request.POST['roll']
        email = request.POST['mail']
        gen = request.POST['gender']
        # class not working here
        cla_ss = request.POST['class']
        dob = request.POST['birthday']
        add_student = AddStudent(
            name=name, roll=roll, email=email, gender=gen, cla_ss=cla_ss, dob=dob)
        add_student.user = request.user
        add_student.save()
        done = "Record Created !!!"
        context = {'user': request.user, 'done': done}
        return render(request, 'student/addStudent.html', context)
    return render(request, 'student/addStudent.html', context)

# manage student


@login_required
def manage_student(request):
    addstu = AddStudent.objects.filter(user=request.user)
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            addstu = AddStudent.objects.filter(Q(name__icontains=q) | Q(roll__icontains=q) | Q(
                email__icontains=q) | Q(cla_ss__icontains=q) | Q(dob__icontains=q))
            count = addstu.count()
            addstu.user = request.user
            return render(request, 'student/manageStudent.html', {'addstu': addstu, 'count': count})

        else:
            count = 0
            addstu.user = request.user
            return render(request, 'student/manageStudent.html', {'addstu': addstu, 'count': count})
    return render(request, 'student/manageStudent.html', {'addstu': addstu, 'count': 0})


# update student

@login_required
def editstudent(request, id):
    addstu = AddStudent.objects.get(id=id)
    return render(request, 'student/updateStudent.html', {'addstu': addstu})

# delete student


@login_required
def delete_student(request, id):
    # get request working
    pi = AddStudent.objects.get(id=id)
    pi.delete()
    return redirect('managestudent')

# update student


def updatestudent(request, id):
    if request.method == 'POST':
        addstu = AddStudent.objects.get(id=id)
        addstu.name = request.POST['studentname']
        addstu.gender = request.POST['gender']
        addstu.cla_ss = request.POST['class']
        # this email field is added now -> Ayush
        addstu.email = request.POST['email']
        addstu.dob = request.POST['dob']
        addstu.roll = request.POST['rollno']
        addstu.save()
        print('record is updated !!!')
        addstu = AddStudent.objects.all()
        return redirect('managestudent')
    return redirect('managestudent')


########## Result ##########

# add result


@login_required
def add_result(request):
    context = {'user': request.user}
    if request.method == 'POST':
        # student info
        first_ = request.POST['first']
        last = request.POST['last']
        roll = request.POST['roll']
        # subjects marks
        eng = request.POST['eng']
        hin = request.POST['hin']
        maths = request.POST['maths']
        sci = request.POST['sci']
        sst = request.POST['sst']
        cs = request.POST['cs']
        # percentage
        percentage = (int(eng) + int(hin) + int(maths) +
                      int(sci) + int(sst) + int(cs)) / 6
        per = percentage[0:5]
        # result
        rs = Result(first_name=first_, last_name=last, roll=roll,
                    per=percentage, eng=eng, hin=hin, maths=maths,
                    sci=sci, sst=sst, cs=cs)
        rs.user = request.user
        rs.save()
        print('Data saved !')
    return render(request, 'result/result-1.html', context)

# show result


@login_required
def show_result(request):
    user = request.user
    rs = Result.objects.filter(user=user)
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            rs = Result.objects.filter(Q(first_name__icontains=q) | Q(
                last_name__icontains=q) | Q(roll__icontains=q) | Q(per__icontains=q))
            count = rs.count()
            rs.user = request.user
            context = {'user': user, 'count': count, 'rs': rs}
            return render(request, 'result/result-2.html', context)
        else:
            context = {'user': user, 'count': 0, 'rs': rs}
            return render(request, 'result/result-2.html', context)

    context = {'user': user, 'count': 0, 'rs': rs}
    return render(request, 'result/result-2.html', context)


# manage result


@login_required
def manage_result(request, id):
    user = request.user
    rs = Result.objects.filter(id=id)
    context = {'user': user, 'rs': rs}
    return render(request, 'result/result-3.html', context)

# delete result


@login_required
def delete_result(request, id):
    # get request working only
    pi = Result.objects.get(id=id)
    pi.delete()
    return redirect('showresult')

# Edit result


@login_required
def update_result(request, id):
    if request.method == 'POST':
        rs = Result.objects.get(id=id)
        rs.eng = request.POST['en']
        rs.hin = request.POST['hi']
        rs.maths = request.POST['math']
        rs.sci = request.POST['sci']
        rs.sst = request.POST['sst']
        rs.cs = request.POST['comp']
        # total sum of all fields
        # rs.per1 = int(rs.eng) + int(rs.hin) + int(rs.maths) + int(rs.sci) + int(rs.sst) + int(rs.cs)
        rs.per = (int(rs.eng) + int(rs.hin) + int(rs.maths) +
                  int(rs.sci) + int(rs.sst) + int(rs.cs)) / 6
        print(rs.per)
        if rs.per <= 100:
            rs.save()
        else:
            return HttpResponse('<h1>Invalid Input, Check your marks !!!</h1>')
        print('Data saved !')
    return redirect('showresult')

########### Subject  ############

# create subject


@login_required
def add_subject(request):
    user = request.user
    context = {'user': user}
    if request.method == "POST":
        name_ = request.POST['name']
        class_num = request.POST['class']
        roll = request.POST['roll']
        stream_name = request.POST['stream_name']
        no_of_subj = request.POST['subj_num']
        name_of_subj = request.POST['subj_name']
        add_student = AddSubject(name=name_, class_num=class_num, roll=roll, stream_name=stream_name,
                                 no_of_subj=no_of_subj, name_of_subj=name_of_subj)
        add_student.user = request.user
        add_student.save()
        done = "Record Created !!!"
        context = {'user': user, 'done': done}
        return render(request, 'subject/createSubject.html', context)
    return render(request, 'subject/createSubject.html', context)

# manageSubject


@login_required
def manage_subject(request):
    user = request.user
    subjects = AddSubject.objects.filter(user=user)
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            subjects = StudentClass.objects.filter(Q(Cname__icontains=q) | Q(class_num__icontains=q) | Q(
                roll__icontains=q) | Q(stream_name__icontains=q) | Q(no_of_subj__icontains=q) | Q(name_of_subj__icontains=q))
            count = subjects.count()
            subjects.user = request.user
            context = {'user': user, 'subjects': subjects, 'count': count}
            return render(request, 'subject/ManageSubject.html', context)
        else:
            subjects.user = request.user
            context = {'user': user, 'subjects': subjects, 'count': 0}
            return render(request, 'subject/ManageSubject.html', context)
    context = {'user': user, 'count': 0, 'subjects': subjects}
    return render(request, 'subject/ManageSubject.html', context)

# edit subject


@login_required
def edit_subject(request, id):
    sub = AddSubject.objects.get(id=id)
    context = {'user': request.user, 'sub': sub}
    return render(request, 'subject/Edit.html', context)


# update subject

@login_required
def update_subject(request, id):
    if request.method == 'POST':
        subj = AddSubject.objects.get(id=id)
        subj.name = request.POST['sname']
        subj.class_num = request.POST['cla_ss']
        subj.roll = request.POST['roll']
        subj.stream_name = request.POST['stream']
        subj.no_of_subj = request.POST['num']
        subj.name_of_subj = request.POST['subj_name']
        subj.save()
        return redirect('managesubject')
    return redirect('managesubject')

# delete subject


@login_required
def subject_delete(request, id):
    # get request working only
    pi = AddSubject.objects.get(id=id)
    pi.delete()
    return redirect('managesubject')


################################################## END #############################################################