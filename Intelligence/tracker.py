import datetime
import re
from time import mktime


class Tracker():

    pattern_time_status = 'last seen \d{1,2} minutes ago'

    def __init__(self, service):
        self.service = service

    def track(self, status_time, status_device):
        dt = datetime.datetime.now()
        current_time = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
        current_activity = self.service.getCurrentActivity()
        if status_time == 'Online' and current_activity is None:
                # self.temp_track_collection.insert({"time": current_time})
                self.service.startActivity(current_time)
        else:
            if re.match(self.pattern_time_status, status_time) and current_activity is not None:
                period = ([int(s) for s in status_time.split() if s.isdigit()])[0]
                end_time = current_time - datetime.timedelta(minutes=period)
                end = datetime.datetime(end_time.year, end_time.month, end_time.day, end_time.hour, end_time.minute)
                start = datetime.datetime(current_activity.tm_year, current_activity.tm_mon, current_activity.tm_mday,
                                          current_activity.tm_hour, current_activity.tm_min)
                record = {"start": start, "end": end}
                if status_device:
                    record['device'] = 'mobile'
                self.service.endActivity(record)
                # self.tracking_collection.insert(record)
                # self.temp_track_collection.drop()

    def calculate_minutes(self, timestamp):
        return mktime(timestamp.timetuple()) / 60