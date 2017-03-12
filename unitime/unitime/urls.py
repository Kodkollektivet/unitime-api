from django.conf.urls import url

from unitime import views

urlpatterns = [
    url(r'^course/$', views.CourseListView.as_view(), name='all_courses'),
    url(r'^course/(?P<course_code>[\w-]+)/$', views.CourseView.as_view(), name='course_by_code'),
    url(r'^event/$', views.EventView.as_view(), name='events_by_code'),
    url(r'^alamon/event/$', views.AlamonEventView.as_view(), name='alamon_events_by_code'),
    url(r'^event/(?P<course_code>[\w-]+)/$', views.EventView.as_view(), name='events_by_code'),
    url(r'^room/$', views.RoomView.as_view(), name='room'),
    url(r'^codes/$', views.CourseCodeView.as_view(), name='codes'),
]
