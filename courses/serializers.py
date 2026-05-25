from rest_framework import serializers
from .models import Course, Category
from user.serializer import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    class Meta:
        model = Course
        fields = [
            'id',
            'instructor',
            'category',
            'category_id',
            'title',
            'description',
            'thumbnail',
            'level',
            'status',
            'price',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'instructor', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['instructor'] = request.user
        return super().create(validated_data)