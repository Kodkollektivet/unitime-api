import json

from django.core.urlresolvers import resolve

from rest_framework.test import APITestCase

class TestApiViewsFunctionNames(APITestCase):
    """Test urls related to their function names."""

    def test_all_courses(self):
        route = resolve('/course/')
        self.assertEqual(route.func.__name__, 'all_courses')

    def test_specific_courses(self):
        route = resolve('/course/1dv702/')
        self.assertEqual(route.func.__name__, 'course_by_code')
