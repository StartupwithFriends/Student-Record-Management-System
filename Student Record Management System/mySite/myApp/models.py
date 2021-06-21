from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# sign up user account


class signup(models.Model):
    # firstname
    firstName = models.CharField(max_length=50)
    # lastname
    lastName = models.CharField(max_length=50)
    # username
    username = models.CharField(User, max_length=50, default=None)
    # email
    email = models.EmailField()
    # password
    password = models.CharField(max_length=50)
    # user image -> not yet storing in Users database
    # img = models.ImageField(upload_to="pics", blank=True, default='dashboard/profile.png')

    # return object firstName in admin
    def __str__(self):
        return self.firstName


# Time Table
class TimeTable(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    day = models.CharField(max_length=50)
    period1 = models.CharField(max_length=50)
    period2 = models.CharField(max_length=50)
    period3 = models.CharField(max_length=50)
    period4 = models.CharField(max_length=50)
    period5 = models.CharField(max_length=50)
    period6 = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user

# Student Class


class StudentClass(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    className = models.CharField(max_length=50)
    classNum = models.CharField(max_length=50)
    classSec = models.CharField(max_length=50)

    def __str__(self):
        return self.user

# Add student model


class AddStudent(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    roll = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    gender = models.CharField(max_length=50)
    cla_ss = models.CharField(max_length=50)
    dob = models.DateField()

    def __str__(self):
        return self.user

# Add subject model


class AddSubject(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    class_num = models.CharField(max_length=50)
    roll = models.CharField(max_length=50)
    stream_name = models.CharField(max_length=50)
    no_of_subj = models.CharField(max_length=50)
    name_of_subj = models.CharField(max_length=50)

    def __str__(self):
        return self.user

# Result model


class Result(models.Model):
    # user info
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    roll = models.CharField(max_length=50)
    # percentage
    per = models.FloatField()
    # Subjects
    # all below integer fields
    eng = models.IntegerField()
    hin = models.IntegerField()
    maths = models.IntegerField()
    sci = models.IntegerField()
    sst = models.IntegerField()
    cs = models.IntegerField()

    def __str__(self):
        return self.user
