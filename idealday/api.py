from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import response

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
        return render(request,'view_plan.html',dict_of_dicts)

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
        #print('add-get')
        return render(request,'add_interval.html')
    def post(self,request):
        #Interval.objects.all().delete()
        return self.get(request)

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

        return render(request,'today.html',dictt)

    
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

class analytics(APIView):

    def get(self,request):

        # show tasks in priority order
        list_of_tasks = []
        scores = []
        all_task_mon = Interval.objects.filter(week_id = 0)
        all_task_mon = all_task_mon.order_by(Coalesce('score','score').desc())

        for task in all_task_mon:
            task_dict = vars(task)
            list_of_tasks.append(task_dict['task'])
            scores.append(task_dict['score'])
        
        
        freq = {key:0 for key in list_of_tasks}

        for w_id in range(0,7):
            all_task_today = Interval.objects.filter(week_id = w_id)
            for task in all_task_today:
                task_dict = vars(task)
                if task_dict['status']==True:
                    freq[task_dict['task']] += 1

        response_dict = {}

        response_dict['task_list'] = [ [list_of_tasks[i],scores[i]] for i in range(len(scores)) ]
        
        freq_ky_sorted = sorted(freq, key=freq.get, reverse=True)
        
        freq_list = [ [x,freq[x]] for x in freq_ky_sorted]
        response_dict['freq'] = freq_list



        ## task completed 7 times
        task_comp_7 = []
        for task in freq_ky_sorted:
            if freq[task]==7:
                task_comp_7.append([task,7])
            else:
                break


        # task completed maximum times(done atleast 1 and atmax 6)
        task_comp_max = []
        if len(task_comp_7) == 0:
            it = 0
            task = freq_ky_sorted[it]
            mx_freq = freq[task]

            if mx_freq > 0 :
                while it < len(freq_ky_sorted) and freq[task] == mx_freq:
                    task_comp_max.append([task,mx_freq])
                    it += 1
                    task = freq_ky_sorted[it]
        else:
            task_comp_max = task_comp_7

        ## task completed 0 times
        task_comp_0 = []
        for it in range(len(freq_ky_sorted)-1,-1,-1):
            if freq[  freq_ky_sorted[it] ]==0:
                task_comp_0.append([freq_ky_sorted[it],0])
            else:
                break

        # task completed minimum times(done atleast 1)
        task_comp_min = []
        
        if len(task_comp_0) == 0:
            it = len(freq_ky_sorted)-1
            task = freq_ky_sorted[it]
            mn_freq = freq[task]

            if mn_freq < 7 :
                while it >= 0 and freq[task] == mn_freq:
                    task_comp_min.append([task,mn_freq])
                    it -= 1
                    task = freq_ky_sorted[it]
        else:
            task_comp_min = task_comp_0

        response_dict['comp_7'] = task_comp_7
        response_dict['comp_0'] = task_comp_0
        response_dict['comp_mx'] = task_comp_max
        response_dict['comp_mn'] = task_comp_min

        return render(request,'analytics_sample.html',response_dict)

    def post(self,request):
        return self.get(request)
