import json
import datetime

from django.core.urlresolvers import resolve
from rest_framework.test import APITestCase

from unitime.models import Course, CourseCode


class TestApiViewsFunctionNames(APITestCase):
    """Test urls related to their function names."""

    def test_all_courses(self):
        route = resolve('/api/course/')
        self.assertEqual(route.func.__name__, 'CourseListView')

    def test_specific_course(self):
        route = resolve('/api/course/1dv702/')
        self.assertEqual(route.func.__name__, 'CourseView')

    def test_events_for_course(self):
        route = resolve('/api/event/1dv702/')
        self.assertEqual(route.func.__name__, 'EventView')

    def test_events_for_multi_courses_POST(self):
        route = resolve('/api/event/')
        self.assertEqual(route.func.__name__, 'EventView')

    def test_course_codes_GET(self):
        route = resolve('/api/codes/')
        self.assertEqual(route.func.__name__, 'CourseCodeView')


class TestApiEndpointsReturnCode(APITestCase):
    """Test status codes on different endpoints."""

    def test_docs(self):
        """Test response to docs endpoint."""
        response = self.client.get('/docs/')
        self.assertEqual(response.status_code, 200)

    def test_course_list(self):
        """Test the endpoint."""
        response = self.client.get('/api/course/')
        self.assertEqual(response.status_code, 200)

    def test_admin_url(self):
        """Test admin url."""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Redirects


class TestApiEventViewPost(APITestCase):
    def test_events_with_multi_course(self):
        response = self.client.post('/api/event/', data={'courses': ['1dv701', '1dv702']})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_events_with_2_course_one_has_no_events(self):
        response = self.client.post('/api/event/', data={'courses': ['1dv701', 'satan']})
        self.assertEqual(len(response.data), 2)
        data = list(filter(lambda x: x['course'] == 'satan', response.data))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('course' in data[0])
        self.assertTrue('events' in data[0])
        self.assertEqual(len(data[0]['events']), 0)

    def test_events_with_3_course_one_has_no_events(self):
        response = self.client.post('/api/event/', data={'courses': ['1dv701', 'satan', '1dv702']})
        self.assertEqual(len(response.data), 3)
        data = list(filter(lambda x: x['course'] == 'satan', response.data))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('course' in data[0])
        self.assertTrue('events' in data[0])
        self.assertEqual(len(data[0]['events']), 0)
        for d in response.data:
            self.assertTrue('course' in d)
            self.assertTrue('events' in d)


class TestAlamonApiEventViewPost(APITestCase):
    """Special endpoint for the iOS framework, Alamonfire."""

    def test_alamon_events_with_multi_course(self):
        """Special endpoint for the iOS framework, Alamonfire."""
        response = self.client.post('/api/alamon/event/', data={'courses': '1dv701, 1dv702'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_alamon_events_with_2_course_one_has_no_events(self):
        """Special endpoint for the iOS framework, Alamonfire."""
        response = self.client.post('/api/alamon/event/', data={'courses': '1dv701, satan'})
        self.assertEqual(len(response.data), 2)
        data = list(filter(lambda x: x['course'] == 'satan', response.data))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('course' in data[0])
        self.assertTrue('events' in data[0])
        self.assertEqual(len(data[0]['events']), 0)

    def test_alamon_events_with_3_course_one_has_no_events(self):
        """Special endpoint for the iOS framework, Alamonfire."""
        response = self.client.post('/api/alamon/event/', data={'courses': '1dv701, satan,1dv702'})
        self.assertEqual(len(response.data), 3)
        data = list(filter(lambda x: x['course'] == 'satan', response.data))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('course' in data[0])
        self.assertTrue('events' in data[0])
        self.assertEqual(len(data[0]['events']), 0)
        for d in response.data:
            self.assertTrue('course' in d)
            self.assertTrue('events' in d)


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
        response = self.client.get('/api/course/1DV701/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['course_code'], '1DV701')

    def test_course_not_found(self):
        """If we cant find course.
        Give a proper error message."""
        response = self.client.get('/api/course/1DV666/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.dumps(response.json()), json.dumps({'message': 'Can not find course 1DV666'}))

    def test_invalid_course_format(self):
        """When requesting a not valid pattern for the course.
        Return a proper error message."""
        response = self.client.get('/api/course/1DV666777/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.dumps(response.json()), json.dumps({'message': 'Invalid search format!'}))

    def test_head_course_list(self):
        """When doing a HEAD request to /course/ give the numbers
        of courses that we have in the DB."""
        response = self.client.head('/api/course/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers['content-length'][1], '1')


class TestApiEndpointCourseCode(APITestCase):
    """Test JSON data responses from endpoints."""

    def setUp(self):
        [CourseCode.objects.create(course_code=i) for i in ['1DV701', '1DV702']]

    def test_course_codes_list(self):
        response = self.client.get('/api/codes/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.data['course_codes'], list))
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(len(response.data['course_codes']), 2)
        self.assertTrue('1DV702' in response.data['course_codes'])


class TestApiEndpointRoom(APITestCase):
    """Test JSON data responses from endpoints."""

    def test_single_room(self):
        """The room string as a little hidden."""
        response = self.client.post('/api/room/', data={'room': 'Datorsal D1142V'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_multi_rooms_string(self):
        response = self.client.post('/api/room/',
                                    data={'room': 'Datorsal D1142V (PC), Datorsal D1170A_V'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.data[0], dict))
        room = response.data[0]
        self.assertTrue('name' in room)
        self.assertTrue('floor' in room)
        self.assertTrue('lat' in room)
        self.assertTrue('lon' in room)
        self.assertTrue('city' in room)

    def test_multi_rooms(self):
        for i in ['Dacke', 'IKEA', 'Myrdal', 'Södrasalen']:
            response = self.client.post('/api/room/', data={'room': i})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(response.data[0], dict))
            room = response.data[0]
            self.assertTrue('name' in room)
            self.assertTrue('floor' in room)
            self.assertTrue('lat' in room)
            self.assertTrue('lon' in room)
            self.assertTrue('city' in room)
