import json
import datetime
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
        route = resolve('/unitime/event/1dv702/')
        self.assertEqual(route.func.__name__, 'EventView')


class TestApiEndpointsReturnCode(APITestCase):
    """Test status codes on different endpoints."""

    def test_home(self):
        """Test response to swagger home."""
        response = self.client.get('/unitime/')
        self.assertEqual(response.status_code, 200)

    def test_course_list(self):
        """Test the endpoint."""
        response = self.client.get('/unitime/course/')
        self.assertEqual(response.status_code, 200)


class TestApiEndpointData(APITestCase):
    """Test JSON data responses from endpoints."""

    def setUp(self):
        semester = ''
        if datetime.datetime.now().isocalendar()[1] <= 7:
            semester = 'VT' + datetime.datetime.now().strftime('%y')
        else:
            semester = 'HT' + datetime.datetime.now().strftime('%y')

        self.course1 = Course.objects.create(
            name_en = 'Internet Security',
            name_sv = 'Internetsäkerhet',
            syllabus_sv = 'http://api.kursinfo.lnu.se/GenerateDocument.ashx?templatetype=coursesyllabus&code=2DV702&documenttype=pdf&lang=sv',
            syllabus_en = 'http://api.kursinfo.lnu.se/GenerateDocument.ashx?templatetype=coursesyllabus&code=2DV702&documenttype=pdf&lang=en',
            course_code = '1DV701',
            course_id = 251445,
            course_reg = 'U6Q05',
            course_points = '7,5 hp',
            course_location = 'Växjö',
            course_language = 'Engelska',
            course_speed = '50%',
            semester = semester,
            url = 'http://lnu.se/education/exchange-students/courses/2DV702?l=en'
        )

    def test_working_course(self):
        response = self.client.get('/unitime/course/1DV701/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['course_code'], '1DV701')

    def test_course_not_found(self):
        """If we cant find course.
        Give a proper error message."""
        response = self.client.get('/unitime/course/1DV666/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.dumps(response.json()), json.dumps({'message': 'Can not find course 1DV666'}))

    def test_invalid_course_format(self):
        """When requesting a not valid pattern for the course.
        Return a proper error message."""
        response = self.client.get('/unitime/course/1DV666777/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.dumps(response.json()), json.dumps({'message': 'Invalid search format!'}))

    def test_head_course_list(self):
        """When doing a HEAD request to /course/ give the numbers
        of courses that we have in the DB."""
        response = self.client.head('/unitime/course/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers['content-length'][1], '1')
