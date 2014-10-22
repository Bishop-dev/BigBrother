import datetime
import re
import pymongo
from scrapy.conf import settings
from time import mktime

class MongoService():

    pattern_time_status = 'last seen \d{1,2} minutes ago'

    def __init__(self):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.temp_track_collection = db[settings['MONGODB_COLLECTION_TEMP_TRACK']]
        self.tracking_collection = db[settings['MONGODB_COLLECTION_TRACK']]

    def track_status(self, status_time, status_mobile):
        dt = datetime.datetime.now()
        current_time = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
        # print status_time
        # print current_time
        previous = self.temp_track_collection.find_one()
        if status_time == 'Online':
            if previous is None:
                self.temp_track_collection.insert({"time": current_time})
                # print 'tracked'
        else:
            if re.match(self.pattern_time_status, status_time) and previous is not None:
                period = ([int(s) for s in status_time.split() if s.isdigit()])[0]
                end = current_time - datetime.timedelta(minutes=period)
                record = {"start": previous['time'], "end": end}
                if status_mobile:
                    record['mobile'] = True
                self.tracking_collection.insert(record)
                self.temp_track_collection.drop()
                # print record

    def calculate_minutes(self, timestamp):
        return mktime(timestamp.timetuple()) / 60