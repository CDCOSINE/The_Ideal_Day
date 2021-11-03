from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from PIL import Image

from rest_framework.response import Response

from .models import Interval

from .serializers import *
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from datetime import datetime
from django.http import HttpResponse
from wsgiref.util import FileWrapper


class view_plan(APIView):
    
    def get(self,request):
        model = Interval.objects.all()
        return render(request,'temp1.html')

