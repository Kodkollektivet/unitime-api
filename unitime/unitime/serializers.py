from rest_framework import serializers

from unitime.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ('id', 'created', 'modified')