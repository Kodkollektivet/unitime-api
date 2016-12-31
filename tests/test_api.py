import json
from pprint import pprint as pp
from unittest import skip

from django.core.urlresolvers import resolve
from rest_framework.test import APITestCase

from unitime.models import Course


class TestApiViewsFunctionNames(APITestCase):
    """Test urls related to their function names."""

    def test_all_courses(self):
        route = resolve('/unitime/course/')
        self.assertEqual(route.func.__name__, 'CourseListView')

    def test_specific_course(self):
        route = resolve('/unitime/course/1dv702/')
        self.assertEqual(route.func.__name__, 'CourseView')

    def test_events_for_course(self):
        route = resolve('/event/1dv702/')
        self.assertEqual(route.func.__name__, 'EventView')


class TestApiEndpointsReturnCode(APITestCase):
    """Test status codes on different endpoints."""

    @skip("Work in progress.")
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_course_list(self):
        response = self.client.get('/unitime/course/')
        self.assertEqual(response.status_code, 200)


class TestApiEndpointData(APITestCase):
    """Test JSON data from endpoints."""

    def setUp(self):
        self.course1 = Course.objects.create(
            name_en = 'Internet Security',
            name_sv = 'Internetsäkerhet',
            syllabus_sv = 'http://api.kursinfo.lnu.se/GenerateDocument.ashx?templatetype=coursesyllabus&code=2DV702&documenttype=pdf&lang=sv',
            syllabus_en = 'http://api.kursinfo.lnu.se/GenerateDocument.ashx?templatetype=coursesyllabus&code=2DV702&documenttype=pdf&lang=en',
            course_code = '2DV702',
            course_id = 251445,
            course_reg = 'U6Q05',
            course_points = '7,5 hp',
            course_location = 'Växjö',
            course_language = 'Engelska',
            course_speed = '50%',
            semester = 'HT16',
            url = 'http://lnu.se/education/exchange-students/courses/2DV702?l=en'
        )

    def test_course(self):
        response = self.client.get('/unitime/course/2dv702/')
        self.assertEqual(response.data['course_code'], '2DV702')
        self.assertEqual(response.data['course_id'], '251445')
