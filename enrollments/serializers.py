from rest_framework import serializers
from enrollments.models import Enrollment, LessonProgress
from courses.serializers import CourseSerializer


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = [
            'id',
            'lesson',
            'is_completed',
            'completed_at',
        ]
        read_only_fields = ['id', 'completed_at']


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
    progress = LessonProgressSerializer(many=True, read_only=True)
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'student',
            'course',
            'course_id',
            'status',
            'progress',
            'enrolled_at',
            'completed_at',
        ]
        read_only_fields = ['id', 'student', 'enrolled_at', 'completed_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['student'] = request.user
        return super().create(validated_data)