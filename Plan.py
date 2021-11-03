import schedule

fail = -1
success = 0

class Plan:
    def __init__(self):
        self.week_plan = {}
        self.week_plan['Mon'] = schedule.schedule()
        self.week_plan['Tue'] = schedule.schedule()
        self.week_plan['Wed'] = schedule.schedule()
        self.week_plan['Thur'] = schedule.schedule()
        self.week_plan['Fri'] = schedule.schedule()
        self.week_plan['Sat'] = schedule.schedule()
        self.week_plan['Sun'] = schedule.schedule()

    
    def check_interval(self,day,interval1):
        return self.week_plan[day].check_interval(interval1)

    def merge_interval(self,day,interval1,interval2):
        return self.week_plan[day].merge_interval(interval1,interval2)
    
    def modify_interval(self,day,interval1,task):
        if self.check_interval(self,day,interval1) !=  success:
            return fail
        self.week_plan[day].intervals[interval1] = task
        return success

    def __str__(self):
        plan_str = ""
        for day in self.week_plan.keys():
            plan_str += '-'*10 + ' ' + day + ' '+ '-'*10 + '\n' + str(self.week_plan[day])
        return plan_str