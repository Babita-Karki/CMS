from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, Faculty, Subject, Attendance, ExamResult

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'

class FacultySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Faculty
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.user.username')
    subject_name = serializers.ReadOnlyField(source='subject.name')

    class Meta:
        model = Attendance
        fields = '__all__'

class ExamResultSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.user.username')
    subject_name = serializers.ReadOnlyField(source='subject.name')

    class Meta:
        model = ExamResult
        fields = '__all__'
