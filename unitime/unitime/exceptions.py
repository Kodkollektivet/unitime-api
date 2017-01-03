import json

from django.http import HttpResponse


def cant_find_course(code):
    return HttpResponse(
            json.dumps({'message': 'Can not find course {}'.format(code)}),
            content_type='application/json',
            status=404)


def invalid_search_format():
    return HttpResponse(
            json.dumps({'message': 'Invalid search format!'}),
            content_type='application/json',
            status=404)


# Cant get event, we dont have the course in out db
def event_course_cant_be_found_in_db():
    return HttpResponse(
            json.dumps({'message': 'We dont have the course in our db!'}),
            content_type='application/json',
            status=404)


def cant_find_room():
    return HttpResponse(
            json.dumps({'message': 'Cant find room!'}),
            content_type='application/json',
            status=404)


def cant_find_events():
    return HttpResponse(
            json.dumps({'message': 'Cant find any schedule for this course!'}),
            content_type='application/json',
            status=404)
