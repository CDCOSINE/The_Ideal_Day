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
from django.db.models.functions import Coalesce


class view_plan(APIView):
    
    
    def get(self,request):

        #model = Interval.objects.all()
        
        weekdays = ['Mon','Tue','Wed','Thurs','Fri','Sat','Sun']

        dict_of_dicts = {}

        dict_of_dicts = {key:None for key in weekdays}


        #list_sample = ['Start Time','End Time','Bandwidth','Task Name','Score','Status']

        properties = ['start_time','end_time','time_diff','task','score','status']


        for w_id in range(0,7):
            model = Interval.objects.filter(week_id = w_id)
            model = model.order_by(Coalesce('start_time','start_time').asc())
            list_model = []
            list_temp = []
            print(model)
            for row in model:
                for element in vars(row).values():
                    if element == True:
                        element = u'\u2713'
                    if element == False:
                        element = u'\u2717'
                    list_temp.append(element)
                
                list_model.append(list_temp[3:])

                list_temp = []
            
            
            dict_of_dicts[weekdays[w_id]] = list_model

        return render(request,'temp1.html',dict_of_dicts)

