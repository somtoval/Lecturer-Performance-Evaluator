from django.db import models
from django.contrib.auth.models import User

class Lecturer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CourseOfStudy(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=20, unique=True)
    level = models.IntegerField()
    course_of_study = models.ForeignKey(CourseOfStudy, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.get_full_name()

class Classroom(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_of_study = models.ForeignKey(CourseOfStudy, on_delete=models.CASCADE)
    level = models.IntegerField()
    day = models.CharField(max_length=10)
    time = models.TimeField()
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.name} - {self.course_of_study.name} - Level {self.level}"

class Comment(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=10, choices=[('positive', 'Positive'), ('negative', 'Negative')])

    def __str__(self):
        return f"{self.student.user.get_full_name()} on {self.classroom.course.name}"
