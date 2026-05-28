from rest_framework import serializers
from django.contrib.auth import get_user_model
from courses.serializers import DepartmentSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password',
            'confirm_password',
            'role',
            'student_id',
            'staff_id',
            'department',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', User.Role.STUDENT),
            student_id=validated_data.get('student_id', None),
            staff_id=validated_data.get('staff_id', None),
            department=validated_data.get('department', None),
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'role',
            'bio',
            'avatar',
            'phone',
            'department',
            'student_id',
            'staff_id',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']