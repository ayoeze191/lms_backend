from rest_framework import serializers
from .models import Course, Faculty, Department, AcademicSession, Semester


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name', 'code', 'created_at']
        read_only_fields = ['id', 'created_at']


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    faculty_id = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(),
        source='faculty',
        write_only=True
    )

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'faculty', 'faculty_id', 'created_at']
        read_only_fields = ['id', 'created_at']


class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ['id', 'name', 'start_date', 'end_date', 'is_current', 'created_at']
        read_only_fields = ['id', 'created_at']


class SemesterSerializer(serializers.ModelSerializer):
    session = AcademicSessionSerializer(read_only=True)
    session_id = serializers.PrimaryKeyRelatedField(
        queryset=AcademicSession.objects.all(),
        source='session',
        write_only=True
    )

    class Meta:
        model = Semester
        fields = [
            'id',
            'session',
            'session_id',
            'semester_type',
            'is_current',
            'registration_open',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True
    )
    semester = SemesterSerializer(read_only=True)
    semester_id = serializers.PrimaryKeyRelatedField(
        queryset=Semester.objects.all(),
        source='semester',
        write_only=True
    )
    lecturer_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'code',
            'description',
            'credit_units',
            'level',
            'is_active',
            'department',
            'department_id',
            'semester',
            'semester_id',
            'lecturer',
            'lecturer_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_lecturer_name(self, obj):
        if obj.lecturer:
            return f"{obj.lecturer.username}"
        return None