from rest_framework import serializers
from .models import Enrollment, Result
from courses.serializers import CourseSerializer


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = [
            'id',
            'ca_score',
            'exam_score',
            'total_score',
            'grade',
            'grade_point',
            'is_published',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'total_score', 'grade', 'grade_point', 'created_at', 'updated_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=__import__(
            'courses.models',
            fromlist=['Course']
        ).Course.objects.all(),
        source='course',
        write_only=True
    )
    result = ResultSerializer(read_only=True)
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'student',
            'student_name',
            'course',
            'course_id',
            'status',
            'result',
            'enrolled_at',
            'approved_at',
            'rejected_at',
            'rejection_reason',
        ]
        read_only_fields = [
            'id',
            'student',
            'status',
            'enrolled_at',
            'approved_at',
            'rejected_at',
        ]

    def get_student_name(self, obj):
        return obj.student.username

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['student'] = request.user
        return super().create(validated_data)