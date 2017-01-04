from django.contrib import admin

from unitime.models import Course, CourseCode


class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_per_page = 500
    search_fields = [
        'name_en', 'name_sv', 'course_code',
        'course_id', 'course_reg', 'semester',
        'course_location', 'created', 'modified']
    list_display = (
        'name_en', 'name_sv', 'course_code',
        'course_id', 'course_reg', 'semester',
        'course_location', 'created', 'modified')


class CourseCodeAdmin(admin.ModelAdmin):
    model = CourseCode
    list_per_page = 500
    search_fields = ['course_code']
    list_display = ('course_code',)


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseCode, CourseCodeAdmin)
