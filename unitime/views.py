from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from unitime.models import Lecture, Course, CourseCode, CourseOffering
from unitime.serializers import LectureSerializer
from unitime.forms import CourseCodeForm


class Lectures(APIView):
    def post(self, request):
        form = CourseCodeForm(request.data)
        if form.is_valid():
            obj, created = CourseCode.objects.get_or_create(course_code=form.cleaned_data['course'])
            try:
                course = Course.objects.get(code=obj.course_code)
                CourseOffering.update_remote(course)
                Lecture.update_remote(course)
                lectures = Lecture.objects.filter(
                    course=course,
                    start_datetime__gt=timezone.now() - timezone.timedelta(days=1)
                ).order_by('start_datetime')
                serializer = LectureSerializer(lectures, many=True)
                return JsonResponse(serializer.data, safe=False)

            except Exception:
                return HttpResponse('Course doesnt exists.')

        else:
            return HttpResponse(form.errors.as_json(),
                                content_type='application/json',
                                status=404)
