from rest_framework import serializers

from students.models import Course, Student


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ("id", "name")


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")
