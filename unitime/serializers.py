from rest_framework import serializers

from unitime.models import Course, Lecture, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ('id', 'created', 'modified')


class LectureSerializer(serializers.ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = Lecture
        #exclude = ('id', 'created', 'modified', 'course', 'course_offering')
        fields = (
            'start_datetime',
            'end_datetime',
            'teacher',
            'info',
            'description',
            'room'
        )
