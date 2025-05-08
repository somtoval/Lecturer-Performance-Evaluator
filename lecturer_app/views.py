from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer, ClassroomSerializer, CommentSerializer
from rest_framework import views, generics, status, response
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Student, Classroom, Course, Comment
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from datetime import datetime
from .pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

# AUTH
# sign-up
class RegisterView(views.APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# sign-in
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            reg_no = serializer.validated_data['reg_no']
            password = serializer.validated_data['password']

            try:
                user_obj = Student.objects.get(reg_no=reg_no)
                username = user_obj.user.username
            except Student.DoesNotExist:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# sign-out
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or token already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)


# classroombystudent: returns that day's course according to the user id passed, also check if the person is an admin so tha it will route to another page adminpage( meaning ever admin user will be created from admin panel and set to admin)
class ClassroomByStudentView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Redirect if admin
        if user.is_staff or user.is_superuser:
            # return Response({"redirect": "adminpage"})
            return Response({"error": "User is not a student"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure user is a student
        try:
            student = user.student
        except Student.DoesNotExist:
            return Response({"error": "User is not a student"}, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.today().strftime('%A')  # 'Monday', 'Tuesday', etc.

        classrooms = Classroom.objects.filter(
            course_of_study=student.course_of_study,
            level=student.level,
            day__iexact=today
        )

        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# submitreview: submits students review on a particular course
class SubmitReviewView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Review submitted successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# admin view to return all commens with pagination and we should be able to filter naegative or postive sentimnt and the level and classroom and course
class CommentFilter(django_filters.FilterSet):
    sentiment = django_filters.ChoiceFilter(choices=[('positive', 'Positive'), ('negative', 'Negative')])
    level = django_filters.NumberFilter(field_name="classroom__level", lookup_expr='exact')
    classroom = django_filters.ModelChoiceFilter(queryset=Classroom.objects.all())
    course = django_filters.ModelChoiceFilter(field_name='classroom__course', queryset=Course.objects.all())

    class Meta:
        model = Comment
        fields = ['sentiment', 'level', 'classroom', 'course']

# List view to return comments with pagination and filtering
class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = CommentFilter
    ordering_fields = ['created_at', 'sentiment']  # Allow ordering by sentiment and created_at
    ordering = ['-created_at']  # Default ordering (newest first)
    pagination_class = PageNumberPagination  # Use pagination



# admin crud for lecturer

# admin crud for course

# admin crud for classroom

# admin crud for classroom