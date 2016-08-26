from django.conf.urls import url

from unitime import views

urlpatterns = [
    url(r'^course/$', views.CourseListView.as_view(), name='all_courses'),
    url(r'^course/(?P<code_in>[\w-]+)/$', views.CourseView.as_view(), name='course_by_code'),
    #url(r'^event/(?P<code_in>[\w-]+)/$', views.EventView.as_view(), name='events_by_code'),
    #url(r'^room/$', views.RoomListView.as_view(), name='rooms'),
    #url(r'^codes/$', views.CourseCodeView.as_view(), name='codes'),
    #url(r'^news/$', views.NewsView.as_view(), name='news'),
]