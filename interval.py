
class interval:

    def __init__(self,starttime,endtime,timediff):

        # starttime , endtime are time objects from mytime
        # print accordingly
        #print('gval ',starttime,':',endtime)
        self.start_time = starttime
        self.end_time = endtime

        # timediff is in minutes
        self.time_diff = timediff
    
    def __str__(self):
        return str(self.start_time) + ' - ' + str(self.end_time)+ ' ({}) '.format(self.time_diff) 


    def is_intersection(self,interval2):
        # interval is object of interval class only
        if str(self.end_time) == str(interval2.start_time):
            return True,self,interval2
        elif str(self.start_time) == str(interval2.end_time):
            return True,interval2,self
        return False,self
