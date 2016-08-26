from django.db import models
import pprint


class TimeStampedModel(models.Model):
    """Gives the model created and modified timestamps"""
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = 'modified'
        ordering = ('-modified', '-created')


class Course(TimeStampedModel):
    name_en = models.CharField(max_length=254, blank=True)  # The en name of the course
    name_sv = models.CharField(max_length=254, blank=True)  # The sv name of the course
    syllabus_sv = models.CharField(max_length=254, blank=True)
    syllabus_en = models.CharField(max_length=254, blank=True)
    course_code = models.CharField(max_length=10)  # ex 1DV008
    course_id = models.CharField(max_length=15, blank=True, unique=True)  # ex: 60380
    course_reg = models.CharField(max_length=15, blank=True, unique=True)  # ex: 67504
    course_points = models.CharField(max_length=15, default='')
    course_location = models.CharField(max_length=254, default='')
    course_language = models.CharField(max_length=100, default='')
    course_speed = models.CharField(max_length=20, default='')
    semester = models.CharField(max_length=6)       # HT16 / VT16
    url = models.CharField(max_length=254, blank=True)   # html url

    def __eq__(self, other):
        return self.course_code == other.course_code

    def __str__(self):
        return 'Course(course_code={}, course_id={}, course_reg={}'.format(self.course_code,
                                                                           self.course_id,
                                                                           self.course_reg)

    def __repr__(self):
        return pprint.pformat(self.__dict__, indent=4)
