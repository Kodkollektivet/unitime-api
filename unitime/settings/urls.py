"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework_swagger.views import get_swagger_view

from unitime import views


urlpatterns = [
    url(r'^unitime/admin/', admin.site.urls),

    url(r'^unitime/$', get_swagger_view(title='Unitime API')),

    url(r'^unitime/course/$', views.CourseListView.as_view(), name='all_courses'),
    url(r'^unitime/course/(?P<course_code>[\w-]+)/$', views.CourseView.as_view(), name='course_by_code'),
    url(r'^unitime/event/(?P<course_code>[\w-]+)/$', views.EventView.as_view(), name='events_by_code')
]
