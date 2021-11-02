class task:
    def __init__(self,name,r_time = 1000,avg_time = 200, inf_cap_time = 75):
        self.score = 0
        self.title = name

        #ll times in minutes
        self.relaxed_time = r_time
        self.average_time = avg_time
        self.inf_capability = inf_cap_time

    def __add__(self,task2):
        
        self.score += task2.score
        self.title += '+ '+task2.title

        self.relaxed_time += task2.relaxed_time
        
        self.average_time = (self.average_time+task2.average_time)/2

        self.inf_capability = (self.inf_capability + task2.inf_capability)*(1)

        return self

"""     self.relaxed_time = 480
        self.average_time = 120
        self.inf_capability = 45

        # a person can do this task in
        ## 480 minutes at slowest speed and relaxed manner
        ## 120 minutes, her/his average speed
        ## 45 minutes full focused and approx. 100% efficiency"""