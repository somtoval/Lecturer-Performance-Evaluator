from django.contrib import admin
from .models import Lecturer, CourseOfStudy, Course, Student, Classroom, Comment

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(CourseOfStudy)
class CourseOfStudyAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'reg_no', 'level', 'course_of_study']
    search_fields = ['user__first_name', 'user__last_name', 'reg_no']

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['course', 'course_of_study', 'level', 'day', 'time', 'lecturer']
    list_filter = ['day', 'course_of_study', 'level']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['student', 'lecturer', 'classroom', 'created_at']
    list_filter = ['created_at']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'text']
