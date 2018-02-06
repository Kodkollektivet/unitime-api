import json

from django.test import TestCase
from rest_framework.test import APIClient, APITestCase

from unitime.models import Course


class TestFixture(TestCase):
    fixtures = ['unitime.json']

    def test_fixture(self):
        '''Make sure that database contains data.'''
        self.assertTrue(len(Course.objects.all()) > 0)


class TestCourseEndpoint(APITestCase):
    fixtures = ['unitime.json']

    def test_course_post(self):
        factory = APIClient()
        response = factory.post('/api/course/', {'course': '2DV50E'}, format='json')
        self.assertTrue(response.status_code, 200)


class TestLecturesEndpoint(APITestCase):
    fixtures = ['unitime.json']

    def test_lectures_post(self):
        factory = APIClient()
        response = factory.post('/api/lectures/', {'course': '2DV50E'}, format='json')
        self.assertTrue(response.status_code, 200)


class TestCoursesEndpoint(APITestCase):
    fixtures = ['unitime.json']

    def test_courses_list_endpoint(self):
        factory = APIClient()
        response = factory.get('/api/courses/', format='json')
        self.assertTrue(response.status_code, 200)
