from django.contrib.auth.models import User
from .models import Student, Classroom, Comment
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ['reg_no', 'course_of_study', 'level', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        # Create the User
        user = User.objects.create_user(
            username=validated_data['reg_no'],  # Use reg_no as username
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # Create the Student
        student = Student.objects.create(
            user=user,
            reg_no=validated_data['reg_no'],
            level=validated_data['level'],
            course_of_study=validated_data['course_of_study']
        )

        return student

class LoginSerializer(serializers.Serializer):
    reg_no = serializers.CharField()
    password = serializers.CharField()

class ClassroomSerializer(serializers.ModelSerializer):
    # to display names instead of IDs (e.g., course name, lecturer name),
    course = serializers.CharField(source='course.name')
    lecturer = serializers.CharField(source='lecturer.user.get_full_name')
    course_of_study = serializers.CharField(source='course_of_study.name')

    class Meta:
        model = Classroom
        fields = ['id', 'course', 'course_of_study', 'level', 'day', 'time', 'lecturer']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'student', 'lecturer', 'classroom', 'text', 'created_at']
        read_only_fields = ['created_at']