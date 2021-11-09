from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from PIL import Image

from rest_framework.response import Response

from .models import Interval,WeekDay,Week_Plan

from .serializers import *
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from datetime import datetime
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.db.models.functions import Coalesce
from datetime import datetime

weekdays = ['Mon','Tue','Wed','Thurs','Fri','Sat','Sun']
weekdays_full = ['Monday','Tuesday','Wednessday','Thursday','Friday','Saturday','Sunday']
def render_time(time_str):
    hour = int(time_str[0:2])
    day = ""
    if hour < 12:
        day = "am"
    else:
        day = "pm"
    time_24_hr = time_str[0:2] +':'+time_str[2:]+' '+day
    
    return time_24_hr



class view_plan(APIView):
    
    
    def get(self,request):
        
        

        dict_of_dicts = {}

        dict_of_dicts = {key:None for key in weekdays}


        properties = ['start_time','end_time','time_diff','task','score','status']

        for w_id in range(0,7):
            model = Interval.objects.filter(week_id = w_id)
            model = model.order_by(Coalesce('start_time','start_time').asc())
            list_model = []
            list_temp = []
            correct = 0
            total = 0
            for row in model:
                for element in vars(row).values():
                    list_temp.append(element)
                
                list_temp = list_temp[3:]
                list_temp[0] = render_time(list_temp[0])
                list_temp[1] = render_time(list_temp[1])
                
                total = total + list_temp[4]

                if row.status:
                    correct = correct + list_temp[4]    
                    list_temp[5] = u'\u2713'
                else:
                    list_temp[5] = u'\u2717'
                list_model.append(list_temp)

                list_temp = []

            dict_of_dicts[weekdays[w_id]] = list_model
            if total !=0:
                
                score = "{:.2f}".format( 100*(correct/total) ) + '%'
               
            else:
                score = 'NA'
            dict_of_dicts[weekdays[w_id]+'_Sc'] = score
        
        dict_of_dicts['Score'] = score
        return render(request,'temp1.html',dict_of_dicts)

    def post(self,request):

        form_dict = request.POST
        time_dif = ( ( datetime.strptime(form_dict['end_time'],'%H%M') - datetime.strptime(form_dict['start_time'],'%H%M')).total_seconds() ) / 60
        
        if time_dif < 0:
            time_dif = (24 - ((0-time_dif)/60))*60

        for w_id in range(0,7):
            w = Week_Plan.objects.get(id=w_id)
            Interval.objects.create(week_id=w,start_time=form_dict['start_time'] , end_time=form_dict['end_time'], time_diff=time_dif,task=form_dict['task'], score=form_dict['Score'],status=False)
        return self.get(request)

class add_intrvl(APIView):
    
    def get(self,request):
        print('add-get')
        return render(request,'temp2.html')

class today(APIView):
    def get(self,request):
        day = datetime.today().weekday()
        model = Interval.objects.filter(week_id = day)
        print(type(model))
        model = model.order_by(Coalesce('start_time','start_time').asc())
        list_temp = []
        list_model = []
        correct = 0
        total = 0
        for row in model:
            for element in vars(row).values():
                list_temp.append(element)
                
            list_temp = list_temp[3:]
            list_temp[0] = render_time(list_temp[0])
            list_temp[1] = render_time(list_temp[1])
                
            total = total + list_temp[4]

            if row.status:
                correct = correct + list_temp[4] 
            list_model.append(list_temp)
            list_temp = []
        dictt = {}
        dictt['Today'] = weekdays_full[day]
        dictt['Today_Data'] = list_model

        return render(request,'temp3.html',dictt)

    
    def post(self,request):

        form_dict = request.POST
        day = datetime.today().weekday()
        week_tasks = Interval.objects.filter(week_id = day)
        listt = dict(form_dict.lists())['name1']
        for idx in listt:
            idx = int(idx)
            particular_task = week_tasks.filter(task = week_tasks[idx].task)
            particular_task.update(status = True)
        return self.get(request)

