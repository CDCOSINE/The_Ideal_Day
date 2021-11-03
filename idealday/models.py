
from django.core.validators import RegexValidator

from django.db import models
from datetime import datetime

week_list = ['Mon','Tue','Wed','Thurs','Fri','Sat','Sun']

class WeekDay(models.IntegerChoices):
    Mon = 0,
    Tues = 1,
    Wed = 2,
    Thurs = 3,
    Fri = 4,
    Sat = 5,
    Sun = 6

class Week_Plan(models.Model):
    id = models.IntegerField(default=WeekDay.Mon, choices=WeekDay.choices,primary_key=True)

    def __str__(self):
        return week_list[self.id]

class Interval(models.Model):

    week_id = models.ForeignKey(to='Week_Plan',related_name='ix', on_delete=models.CASCADE)

    start_time = models.CharField(max_length = 4,validators=[RegexValidator(regex='^.{4}$', message='Length has to be 4', code='Invalid length')])
    end_time = models.CharField(max_length = 4,validators=[RegexValidator(regex='^.{4}$', message='Length has to be 4', code='Invalid length')])
    
    time_diff = models.IntegerField()
    
    task = models.TextField()
    score = models.IntegerField()
    
    status = models.BooleanField()

    def __str__(self):

        if self.status:
            #Tick Mark
            symbol = u'\u2713'
        else:
            # Cross Mark
            symbol = u'\u2717'
        return self.start_time + ' - ' + self.end_time + ' ({})'.format(self.time_diff) +' => '+self.task+' {} points '.format(self.score) + symbol 


