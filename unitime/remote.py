import requests
import re
from pprint import pprint as pp


def get_course(course_code) -> dict:
    course_code = course_code.upper()
    url = f'https://se.timeedit.net/web/lnu/db1/schema2/objects.txt?max=15&fr=t&partajax=t&im=f&sid=6&l=en_US&search_text={course_code}&types=5'
    try:
        req = requests.get(url, timeout=10)
        if req.status_code is 200:
            data = req.json()
            if data.get('count', 0) is not 0:
                course_id = data['ids'][-1]
                url = f'https://se.timeedit.net/web/lnu/db1/schema2/objects/{course_id}/o.json'
                req = requests.get(url, timeout=10)
                if req.status_code is 200:
                    data = req.json()
                    data = data['records'][0]['fields']
                    # pp(data)
                    return {
                        'code': course_code,              # code
                        'name': data[2]['values'][0],     # name
                        'speed': data[4]['values'][0],    # speed
                        'points': data[3]['values'][0],   # points
                        'syllabus': f'http://api.kursinfo.lnu.se/GenerateDocument.ashx?templatetype=coursesyllabus&code={course_code}&documenttype=pdf&lang=en'
                    }
    except Exception as e:
        pass

    return None


def get_course_offerings(course_code) -> list:
    course_code = course_code.upper()
    course_offerings = []
    url = f'https://se.timeedit.net/web/lnu/db1/schema2/objects.txt?max=15&fr=t&partajax=t&im=f&sid=6&l=en_US&search_text={course_code}&types=5'
    try:
        req = requests.get(url, timeout=10)
        if req.status_code is 200:
            data = req.json()
            if data.get('count', 0) is not 0:  # There are more than one course offering
                for course_id in data['ids']:
                    url = f'https://se.timeedit.net/web/lnu/db1/schema2/objects/{course_id}/o.json'
                    req = requests.get(url, timeout=10)
                    if req.status_code is 200:
                        data = req.json()
                        data = data['records'][0]['fields']
                        course_offerings.append({
                            'offering_id': course_id,                               # 0, id
                            'registration_id': data[6]['values'][0].split('-')[1],      # 1, registration_id
                            'year': data[6]['values'][0].split('-')[0][2:],  # 2, year, 18
                            'semester': data[6]['values'][0].split('-')[0][:2],  # 3, semester, HT
                        })

                # pp(course_offerings)
                return course_offerings
    except Exception as e:
        pass

    return []


def get_lectures(co) -> list:
    lectures = set()

    def _parse_room(room):
        match = re.search('[A-Z]+\d+[A-Z]+', room, re.IGNORECASE)
        if match:
            m = match.group()
            m = re.sub(r'_V$|_K$|V$|K$', '', m, flags=re.IGNORECASE)
            m = re.sub(r'A$|$B', '', m, flags=re.IGNORECASE)
            return m.upper()

    def _remote():
        try:
            url = f"https://se.timeedit.net/web/lnu/db1/schema2/s.json?object=courseevt_{co.semester}{co.year}-{co.registration_id}&tab=3"
            req = requests.get(url, timeout=10)
            if req.status_code is 200:
                data = req.json()
                # pp(data)
                if data['info']['reservationcount'] > 0:
                    for event in data['reservations']:
                        try:
                            lectures.add((
                                event['startdate'] + ' ' + event['starttime'],  # start_datetime
                                event['startdate'] + ' ' + event['endtime'],    # endtime
                                event['columns'][3],                            # teacher
                                _parse_room(event['columns'][2]),               # room
                                event['columns'][5],                            # info
                                event['columns'][8],                            # desc
                            ))

                        except Exception as e:
                            print(e)
        except Exception as e:
            print(e)

    def _lectures_to_dict():
        return [
            {
                'start_datetime': i[0],
                'end_datetime': i[1],
                'teacher': i[2],
                'room': i[3],
                'info': i[4],
                'description': i[5],
            } for i in lectures]

    _remote()
    if len(lectures) > 0:
        return _lectures_to_dict()
    else:
        return []


def get_rooms():
    rooms_set = set()
    rooms_lst = []

    def _parse():
        for room in rooms_set:
            rooms_lst.append({
                'name': room[0],
                'floor': room[1],
                'lat': room[2],
                'lon': room[3]
            })

    try:
        req = requests.get('http://karta.lnu.se/api/locations/', timeout=10)
        if req.status_code is 200:
            data = req.json()
            for room in data:
                name = room['Swedish_Main_Name']
                name = re.sub(r'_V$|_K$', '', name, flags=re.IGNORECASE)
                name = re.sub(r'V$|K$', '', name, flags=re.IGNORECASE)
                name = re.sub(r'A$|B$', '', name, flags=re.IGNORECASE)
                name = name.upper()
                rooms_set.add((
                    name,  # name
                    room['Floor_Number'],       # floor
                    room['Latitude'],
                    room['Longitude'],
                ))
    except Exception as e:
        print(e)

    _parse()
    return rooms_lst
