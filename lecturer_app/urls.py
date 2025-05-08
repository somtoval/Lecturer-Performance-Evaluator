from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ClassroomByStudentView,
    SubmitReviewView,
    CommentListView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('classroom/<int:user_id>/', ClassroomByStudentView.as_view(), name='classroom-by-student'),
    path('submitreview/', SubmitReviewView.as_view(), name='submit-review'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
]
