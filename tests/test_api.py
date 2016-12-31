import json

from django.core.urlresolvers import resolve

from rest_framework.test import APITestCase


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

    def test_home(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_course_list(self):
        response = self.client.get('/unitime/course/')
        self.assertEquals(response.status_code, 200)
