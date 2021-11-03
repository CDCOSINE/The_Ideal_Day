import mytime
import interval
import task
from random import randrange

success = 0
fail = -1

class schedule:

    def __init__(self):    
        self.intervals = {}


        # 00:00 am
        start_time = mytime.time('00','00')
        
        # 00:15 am
        end_time = mytime.time('00','15')
        
        # 96 intervals of 15 minutes each
        
        total_intervals = 96
        intervals_formed = 0
        size_of_interval = 15

        

        while intervals_formed < total_intervals:
            
            current_interval = interval.interval(start_time,end_time,size_of_interval)

            self.intervals[current_interval] = task.task("task "+str(randrange(10)),randrange(10))

            intervals_formed += 1

            start_time = mytime.time(end_time.hour,end_time.minutes)
            end_time = mytime.time(end_time.hour,end_time.minutes)
            end_time = end_time.add_x_min(15)
        
    def check_interval(self,interval1):
        if interval1 not in self.intervals.keys():
            return fail
        return success

    def merge_intervals(self,interval1,interval2):

        if self.check_interval(interval1)!=success or self.check_interval(interval2)!=success :
            return fail
        
        ##check intersection of intervals
        [is_intersect,prior,later] = interval1.is_intersection(interval2)
        
        if is_intersect:

            ## + Operator overloaded to add objects of custom task class
            self.intervals[prior] = self.intervals[prior] + self.intervals[later]
            prior.end_time = later.end_time
            prior.time_diff = prior.time_diff + later.time_diff
            del self.intervals[later]
            return success
        
        return fail

    def __str__(self):
        schedule_str = ""
        for intervl in  self.intervals.keys():
            schedule_str += (str(intervl) + ' -> ' + str(self.intervals[intervl])) + '\n'
        return schedule_str