# -*- coding:utf-8 -*-
import re

from django import forms
from django.core.validators import RegexValidator


class CourseCodeForm(forms.Form):
    course = forms.CharField(
        min_length=6,
        max_length=6
    )
