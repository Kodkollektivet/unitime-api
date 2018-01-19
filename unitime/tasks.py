from __future__ import absolute_import
import os
import re
import time
import logging

from celery import Celery
from celery.schedules import crontab
from celery import shared_task


log = logging.getLogger(__name__)


def get_courses_from_file():
    from unitime.models import CourseCode
    log.debug('Importing course codes from file.')
    codes = []
    with open('/app/test_codes.txt') as f:
        for line in f:
            course = line
            course = re.sub('\n', '', course)
            try:
                cc = CourseCode(course_code=course)
                cc.save()
            except Exception as e:
                log.debug(e)


def get_rooms_from_remote():
    from unitime.models import Room
    from unitime.remote import get_rooms
    log.debug('Start getting remote rooms.')
    try:
        for room in get_rooms():
            Room.objects.update_or_create(name=room['name'], defaults=room)
    except Exception as e:
        log.debug(e)


def get_courses_to_db():
    from unitime.models import CourseCode, Course
    from unitime.remote import get_course, get_course_offerings

    if len(Course.objects.all()) == 0:
        get_courses_from_file()

    log.debug('Start getting remote courses.')
    try:
        for course_code in CourseCode.objects.all():
            course = get_course(course_code.course_code)
            if course:
                created, obj = Course.objects.update_or_create(code=course['code'], defaults=course)
    except Exception as e:
        log.debug(e)


def get_course_offerings_to_db():
    from unitime.models import CourseCode, Course, CourseOffering
    from unitime.remote import get_course, get_course_offerings
    log.debug('Start getting remote course offerings.')
    try:
        for course in Course.objects.all():
            for co in get_course_offerings(course.code):
                co['course'] = course
                obj, created = CourseOffering.objects.update_or_create(
                    offering_id = co['offering_id'],
                    registration_id = co['registration_id'],
                    year = co['year'],
                    defaults=co)
    except Exception as e:
        log.debug(e)



def get_all_lectures():
    from unitime.models import CourseCode, Course, CourseOffering, Lecture, Room
    from unitime.remote import get_course, get_course_offerings, get_lectures
    from django.utils.dateparse import parse_datetime
    log.debug('Start getting remote lectures.')
    try:
        for co in CourseOffering.objects.all():
            for lecture in get_lectures(co):
                if lecture['room']:
                    obj, created = Room.objects.get_or_create(name=lecture['room'])
                    lecture['room'] = obj
                lecture['course'] = co.course
                lecture['course_offering'] = co
                lecture['start_datetime'] = parse_datetime(lecture['start_datetime'])
                lecture['end_datetime'] = parse_datetime(lecture['end_datetime'])
                Lecture.objects.update_or_create(
                    start_datetime = lecture['start_datetime'],
                    course = lecture['course'],
                    defaults=lecture
                )
    except Exception as e:
        log.debug(e)


@shared_task
def execute_tasks():
    from django.core.mail import send_mail
    get_rooms_from_remote()
    get_courses_to_db()
    get_course_offerings_to_db()
    get_all_lectures()
    send_mail(
        'Unitime celery is done.',
        'Unitime celery is done.',
        'unitime@kodkollektivet.se',
        ['jherrlin@gmail.com'],
        fail_silently=False,
    )
