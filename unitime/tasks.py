from __future__ import absolute_import
import os
import re
import time
import logging

from django.conf import settings

from celery import Celery
from celery.schedules import crontab
from celery import shared_task


log = logging.getLogger(__name__)


@shared_task
def update(course_code):
    from unitime.models import Course, CourseOffering, CourseCode, Lecture
    try:
        CourseCode.objects.update_or_create(course_code=course_code)
        Course.update_remote(course_code)
        course = Course.objects.get(code=course_code)
        CourseOffering.update_remote(course)
        Lecture.update_remote(course)
        return True
    except Exception as e:
        log.debug(e)
        return False


def get_courses_from_file():
    from unitime.models import CourseCode
    from unitime.forms import CourseCodeForm
    log.debug('Importing course codes from file.')
    with open(settings.BASE_DIR+'/course_codes.txt') as f:
        for line in f:
            try:
                course = line
                course = re.sub('\n', '', course)
                form = CourseCodeForm({'course': course})
                if form.is_valid():
                    c = form.cleaned_data['course']
                    CourseCode.objects.update_or_create(course_code=c)
            except Exception as e:
                log.debug(e)


@shared_task
def daily_update():
    import time
    from django.core.mail import send_mail
    from unitime.models import Room, CourseCode, Course, CourseOffering, Lecture
    log.debug('Starting daily update.')
    start_time = time.time()
    Room.update_remote()
    get_courses_from_file()

    for course_code in CourseCode.objects.all():
        Course.update_remote(course_code.course_code)

    for course in Course.objects.all():
        CourseOffering.update_remote(course)
        Lecture.update_remote(course)

    elapsed_time = time.time() - start_time
    try:
        send_mail(
            'Unitime daily_update is done.',
            'Unitime daily_update is done. \nExecution took: {:.1f} sec.'.format(elapsed_time),
            'unitime@kodkollektivet.se',
            ['jherrlin@gmail.com'],
            fail_silently=False,
        )
    except Exception as e:
        log.debug(e)
    log.debug('Daily update done. Execution took: {:.1f} sec.'.format(elapsed_time))
