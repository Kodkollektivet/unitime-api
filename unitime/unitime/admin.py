from django.contrib import admin

from unitime.models import Course


class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_per_page = 500
    search_fields = ['name_en', 'name_sv', 'course_code', 'course_id', 'course_reg', 'semester', 'course_location', 'created', 'modified']
    list_display = ('name_en', 'name_sv', 'course_code', 'course_id', 'course_reg', 'semester', 'course_location', 'created', 'modified')


admin.site.register(Course, CourseAdmin)