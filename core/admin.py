from django.contrib import admin
from .models import Student, Faculty, Attendance, ExamResult

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Attendance)
admin.site.register(ExamResult)

