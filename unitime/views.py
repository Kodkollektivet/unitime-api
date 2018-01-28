from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from unitime.models import Course, Lecture, CourseCode, CourseOffering
from unitime.serializers import LectureSerializer, CourseSerializer
from unitime.forms import CourseCodeForm
from unitime.tasks import update


def get_course(course_code):
    counter = 0
    while True:
        try:
            course = Course.objects.get(code=course_code)
            return course
        except Course.DoesNotExist as e:
            Course.update_remote(course_code)
            if counter > 2:
                break
        counter = counter + 1
    return None


class LecturesView(APIView):
    def post(self, request):
        form = CourseCodeForm(request.data)
        if form.is_valid():
            course_code = form.cleaned_data['course']
            update.delay(course_code)
            course = get_course(course_code)
            if course:
                lectures = Lecture.objects.filter(
                    course=course,
                    start_datetime__gt=timezone.now() - timezone.timedelta(days=1)
                ).order_by('start_datetime')
                serializer = LectureSerializer(lectures, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                return HttpResponse('Course doesnt exists.')
        else:
            return HttpResponse(form.errors.as_json(),
                                content_type='application/json',
                                status=404)


class CourseView(APIView):
    def post(self, request):
        form = CourseCodeForm(request.data)
        if form.is_valid():
            course_code = form.cleaned_data['course']
            CourseCode.objects.update_or_create(course_code=course_code)
            course = get_course(course_code)
            if course:
                serializer = CourseSerializer(course, many=False)
                return JsonResponse(serializer.data, safe=False)
            else:
                return HttpResponse('Course not found')
        else:
            return HttpResponse(form.errors.as_json(),
                                content_type='application/json',
                                status=404)
