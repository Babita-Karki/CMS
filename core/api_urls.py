from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    StudentViewSet, FacultyViewSet, SubjectViewSet, 
    AttendanceViewSet, ExamResultViewSet
)

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'faculty', FacultyViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'results', ExamResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
