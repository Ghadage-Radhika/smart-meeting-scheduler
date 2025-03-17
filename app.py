# Application
from datetime import datetime, timedelta
import calendar

class MeetingScheduler:
    def __init__(self, working_hours=(9, 17), public_holidays=None):
        self.working_hours = working_hours
        self.public_holidays = public_holidays if public_holidays else []
        self.schedules = {}  # Store user meetings
    
    def is_working_day(self, date):
        return date.weekday() < 5 and date.strftime('%Y-%m-%d') not in self.public_holidays
    
    def schedule_meeting(self, user, date_str, start_time, end_time):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if not self.is_working_day(date):
            return "Cannot schedule on weekends or public holidays."
        
        start_time = datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.strptime(end_time, "%H:%M").time()
        
        if start_time.hour < self.working_hours[0] or end_time.hour > self.working_hours[1]:
            return "Meeting time is outside working hours."
        
        if user not in self.schedules:
            self.schedules[user] = {}
        
        if date_str not in self.schedules[user]:
            self.schedules[user][date_str] = []
        
        for meeting in self.schedules[user][date_str]:
            if not (end_time <= meeting[0] or start_time >= meeting[1]):
                return "Meeting overlaps with an existing one."
        
        self.schedules[user][date_str].append((start_time, end_time))
        self.schedules[user][date_str].sort()
        return "Meeting scheduled successfully."
    
    def available_slots(self, user, date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if not self.is_working_day(date):
            return "No available slots on weekends or public holidays."
        
        start_hour, end_hour = self.working_hours
        slots = [(datetime.strptime(f"{h}:00", "%H:%M").time(), datetime.strptime(f"{h+1}:00", "%H:%M").time()) for h in range(start_hour, end_hour)]
        
        if user in self.schedules and date_str in self.schedules[user]:
            meetings = self.schedules[user][date_str]
            slots = [slot for slot in slots if all(slot[1] <= m[0] or slot[0] >= m[1] for m in meetings)]
        
        return slots if slots else "No available slots."
    
    def view_meetings(self, user, date_str):
        return self.schedules.get(user, {}).get(date_str, "No meetings scheduled.")


scheduler = MeetingScheduler(public_holidays=["2025-03-17", "2025-12-25"])  
print(scheduler.schedule_meeting("Alice", "2025-03-18", "10:00", "11:00"))
print(scheduler.available_slots("Alice", "2025-03-18"))
print(scheduler.view_meetings("Alice", "2025-03-18"))
