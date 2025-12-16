from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Student, Faculty, Subject, Attendance, Enrollment, ExamResult
from .forms import StudentForm, FacultyForm, SubjectForm

# --- Authentication & Core ---

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif hasattr(request.user, 'faculty'):
            return redirect('faculty_dashboard')
        elif hasattr(request.user, 'student'):
            return redirect('student_dashboard')
    return render(request, 'core/home.html')

class CustomLoginView(auth_views.LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(auth_views.LogoutView):
    next_page = 'login'

# --- Admin Views ---

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
        
    context = {
        'student_count': Student.objects.count(),
        'faculty_count': Faculty.objects.count(),
        'subject_count': Subject.objects.count(),
    }
    return render(request, 'core/dashboard_admin.html', context)

@login_required
def add_student(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = StudentForm()
    return render(request, 'core/form.html', {'form': form, 'title': 'Add Student'})

@login_required
def add_faculty(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = FacultyForm()
    return render(request, 'core/form.html', {'form': form, 'title': 'Add Faculty'})

@login_required
def add_subject(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = SubjectForm()
    return render(request, 'core/form.html', {'form': form, 'title': 'Add Subject'})

# --- Faculty Views ---

@login_required
def faculty_dashboard(request):
    try:
        faculty = request.user.faculty
        subjects = faculty.subjects.all()
    except:
        subjects = []
    # If not a faculty but trying to access, maybe redirect? 
    # For now, if no faculty profile, just show empty.
    return render(request, 'core/dashboard_faculty.html', {'subjects': subjects})

@login_required
def mark_attendance(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    # Ensure current user is the faculty for this subject? (Enhancement)
    
    students = Student.objects.filter(enrollment__subject=subject) # Get enrolled students
    
    if request.method == 'POST':
        date = request.POST.get('date')
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    subject=subject,
                    date=date,
                    defaults={'status': status}
                )
        return redirect('faculty_dashboard')
    
    return render(request, 'core/mark_attendance.html', {
        'subject': subject,
        'students': students,
        'date': timezone.now().date()
    })

@login_required
def add_result(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    students = Student.objects.filter(enrollment__subject=subject)

    if request.method == 'POST':
        student_id = request.POST.get('student')
        marks = request.POST.get('marks')
        total = request.POST.get('total')
        
        student = Student.objects.get(id=student_id)
        ExamResult.objects.create(
            student=student,
            subject=subject,
            marks_obtained=marks,
            total_marks=total
        )
        return redirect('faculty_dashboard')

    return render(request, 'core/add_result.html', {'subject': subject, 'students': students})

# --- Student Views ---

@login_required
def student_dashboard(request):
    try:
        student = request.user.student
        enrollments = Enrollment.objects.filter(student=student)
        
        # Calculate overall attendance
        total_attendance = Attendance.objects.filter(student=student).count()
        present_attendance = Attendance.objects.filter(student=student, status='Present').count()
        attendance_percent = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0
        
        # Get results
        results = ExamResult.objects.filter(student=student)
        
        context = {
            'student': student,
            'enrollments': enrollments,
            'attendance_percent': round(attendance_percent, 1),
            'results': results,
        }
    except:
        context = {}
        
    return render(request, 'core/dashboard_student.html', context)

@login_required
def enroll_course(request):
    try:
        student = request.user.student
        # Get subjects not already enrolled
        current_enrollments = Enrollment.objects.filter(student=student).values_list('subject_id', flat=True)
        available_subjects = Subject.objects.exclude(id__in=current_enrollments)
        
        if request.method == 'POST':
            subject_ids = request.POST.getlist('subjects')
            for subject_id in subject_ids:
                subject = Subject.objects.get(id=subject_id)
                Enrollment.objects.create(student=student, subject=subject)
            return redirect('student_dashboard')
            
        return render(request, 'core/enroll_course.html', {'available_subjects': available_subjects})
    except:
        return redirect('home')

