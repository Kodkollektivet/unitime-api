from django.contrib import admin
from unitime.models import CourseCode, Course, CourseOffering, Lecture, Room


class CourseCodeAdmin(admin.ModelAdmin):
    model = CourseCode
    list_per_page = 50
    search_fields = ['course_code']
    list_display = ('course_code',)

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_per_page = 50
    search_fields = (
        'code',
        'name',
        'speed',
        'points'
    )

    list_display = (
        'code',
        'name',
        'speed',
        'points'
    )

class CourseOfferingAdmin(admin.ModelAdmin):
    model = CourseOffering
    list_per_page = 50
    list_display = (
        'offering_id',
        'registration_id',
        'year',
        'semester',
        'course'
    )

class LectureAdmin(admin.ModelAdmin):
    model = Lecture
    list_display = (
        'start_datetime',
        'end_datetime',
        'teacher',
        'room'
    )

class RoomAdmin(admin.ModelAdmin):
    model = Room
    list_display = (
        'name',
        'floor',
        'lat',
        'lon'
    )
    search_fields = (
        'name',
        'floor',
        'lat',
        'lon'
    )

admin.site.register(CourseCode, CourseCodeAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseOffering, CourseOfferingAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Room, RoomAdmin)
