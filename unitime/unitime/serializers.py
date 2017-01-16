from rest_framework import serializers

from unitime.models import Course, CourseCode


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ('id', 'created', 'modified')


class CourseCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCode
        exclude = ('id',)
