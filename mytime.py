class time:    
    def __init__(self,hr,mn):
        self.hour = hr
        self.minutes = mn

    def __str__(self):
        return self.hour+':'+self.minutes
    def add_x_hour(self,x):

        if x==0:
            return self

        x = x%24
        hour_val = int(x+int(self.hour))
        
        if(hour_val >= 24):
            self.hour = '00'
            self = self.add_x_hour(hour_val-24)
            return self

        hour_str = str(hour_val)
        self.hour = ('0'* (2-len(hour_str)) ) + hour_str
        return self
    
    def add_x_min(self,x):
        
        if x==0:
            return self

        if(x>=60):
            self.add_x_hour(x//60)
            x = x%60

        mins_val = x + int(self.minutes)

        if mins_val >= 60:
            
            self.minutes = '00'
            self = self.add_x_hour(1)
            self = self.add_x_min(mins_val-60)
            return self
        #print('O ',mins_val)
        minutes_string = str(mins_val)
        self.minutes = '0'*(2 - len(minutes_string)) + minutes_string 
        return self
        
