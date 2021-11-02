class time:
    def __init__(self):

        self.hour = '00'
        self.minutes = '00'
    
    def __init__(self,hr,mn):
        self.hour = hr
        self.minutes = mn

    def __str__(self):
        return self.hour+':'+self.minutes
    def add_x_hour(self,x):

        if x==0:
            return

        x = x%24
        hour_val = int(x+int(self.hour))
        
        if(hour_val >= 24):
            self.hour = '00'
            self.add_x_hour(hour_val-24)
            return

        hour_str = str(hour_val)
        self.hour = ('0'* (2-len(hour_str)) ) + hour_str

    
    def add_x_min(self,x):
        
        if x==0:
            return

        if(x>=60):
            self.add_x_hour(x//60)
            x = x%60

        mins_val = x + int(self.minutes)

        if mins_val >= 60:
            
            self.minutes = '00'
            self.add_x_hour(1)
            self.add_x_min(mins_val-60)
            return
        #print('O ',mins_val)
        minutes_string = str(mins_val)
        self.minutes = '0'*(2 - len(minutes_string)) + minutes_string 
        
"""
start_time = time('00','00')

end_time = time('00','15')

count  = 0
while count<96:
    count = count+1
    print(start_time,' - ', end_time)
    start_time = time(end_time.hour,end_time.minutes)
    end_time.add_x_min(15)
 """