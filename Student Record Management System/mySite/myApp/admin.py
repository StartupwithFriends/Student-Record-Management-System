from django.contrib import admin
from .models import signup, Result, TimeTable, StudentClass, AddSubject, AddStudent

# Register your models here.

# signup model
admin.site.register(signup)
# timtable model
admin.site.register(TimeTable)
# studentclass model
admin.site.register(StudentClass)
# addStudent model
admin.site.register(AddStudent)
# addsubject model
admin.site.register(AddSubject)
# result
admin.site.register(Result)
