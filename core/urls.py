from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Dashboards
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),

    # Admin Actions
    path('add/student/', views.add_student, name='add_student'),
    path('add/faculty/', views.add_faculty, name='add_faculty'),
    path('add/subject/', views.add_subject, name='add_subject'),

    # Faculty Actions
    path('mark_attendance/<int:subject_id>/', views.mark_attendance, name='mark_attendance'),
    path('add_result/<int:subject_id>/', views.add_result, name='add_result'),

    # Student Actions
    path('enroll/', views.enroll_course, name='enroll_course'),
]
