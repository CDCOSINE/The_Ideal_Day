import mytime
import interval
import task

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

            self.intervals[current_interval] = task.task("task 1")

            intervals_formed += 1

            start_time = mytime.time(end_time.hour,end_time.minutes)
            end_time.add_x_hour(15)
        
    def check_interval(self,interval1):
        if interval1 not in self.intervals.keys():
            return -1
        return 0

    def merge_intervals(self,interval1,interval2):

        if self.check_interval(interval1)!=0 or self.check_interval(interval2)!=0 :
            return -1
        
        ##check intersection of intervals
        [is_intersect,prior,later] = interval1.is_intersection(interval2)
        
        if is_intersect:

            ## + Operator overriden to add objects of custom task class
            self.intervals[prior] = self.intervals[prior] + self.intervals[later]
            prior.end_time = later.end_time
            del self.intervals[later]
            return 0
        
        return -1