from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from timeedit_lnu_api import get_course

from unitime.models import Course
from unitime.forms import CourseForm
from unitime.serializers import CourseSerializer

from unitime import exceptions


KODKOLLEKTIVET_HEADER = {'Provided-By': 'kodkollektivet.se'}  # In header respons


class CourseListView(APIView):

    def get(self, request):
        courses = []
        for course in Course.objects.all():
            if course not in courses:
                courses.append(course)
        course_serializer = CourseSerializer(courses, many=True)

        return Response(course_serializer.data,
                        headers=KODKOLLEKTIVET_HEADER,
                        status=status.HTTP_200_OK)

    def head(self, request):
        headers = {'Content-Length': len(Course.objects.all()), 'Provided-By': 'kodkollektivet.se'}
        return Response(
            headers=headers,
            status=status.HTTP_200_OK)


class CourseView(APIView):

    def get(self, request, code_in):

        form = CourseForm({'course': code_in})

        if form.is_valid():
            code = form.cleaned_data['course'].upper()

            #save_course_code(code)  # Save code for future use

            # Does course already exists in DB
            if Course.objects.filter(course_code__exact=code).exists():
                course = Course.objects.filter(course_code__iexact=code).latest(field_name='modified')
                return Response(
                    CourseSerializer(course).data,
                    headers=KODKOLLEKTIVET_HEADER,
                    status=status.HTTP_200_OK)

            else:

                found_course = get_course(code)

                if found_course:
                    found_course = found_course[0]
                    course = Course.objects.filter(course_code__iexact=code).latest(field_name='modified')
                    return Response(
                        CourseSerializer(course).data,
                        headers=KODKOLLEKTIVET_HEADER,
                        status=status.HTTP_200_OK)

            return exceptions.can_find_course(code_in)

        else:
            return exceptions.invalid_search_format()