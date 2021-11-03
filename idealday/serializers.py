
from rest_framework import serializers
from idealday.models import WeekDay,Week_Plan,week_list
from datetime import datetime
from django.core.validators import RegexValidator

week_list = ['Mon','Tue','Wed','Thurs','Fri','Sat','Sun']

class WeekDaySerializer(serializers.ModelSerializer):
    Mon = 0,
    Tues = 1,
    Wed = 2,
    Thurs = 3,
    Fri = 4,
    Sat = 5,
    Sun = 6

class Week_PlanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=WeekDay.Mon)

    def __str__(self):
        return week_list[self.id]

class IntervalSerializer(serializers.ModelSerializer):

    #week_id = serializers.ForeignKey(to='Week_Plan',related_name='ix', on_delete=serializers.CASCADE)

    start_time = serializers.CharField(max_length = 4,validators=[RegexValidator(regex='^.{4}$', message='Length has to be 4', code='Invalid length')])
    end_time = serializers.CharField(max_length = 4,validators=[RegexValidator(regex='^.{4}$', message='Length has to be 4', code='Invalid length')])
    
    time_diff = serializers.IntegerField()
    
    #task = serializers.TextField()
    score = serializers.IntegerField()
    
    status = serializers.BooleanField()

    def __str__(self):

        if self.completed:
            #Tick Mark
            symbol = u'\u2713'
        else:
            # Cross Mark
            symbol = u'\u2717'
        return self.start_time + ' - ' + self.end_time + ' ({})'.format(self.time_diff) +' => '+self.task+' {} points '.format(self.score) + symbol 


