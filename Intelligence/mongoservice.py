import datetime
import pymongo
from scrapy.conf import settings
from time import mktime

class MongoService():

    def __init__(self):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.temp_track_collection = db[settings['MONGODB_COLLECTION_TEMP_TRACK']]
        self.tracking_collection = db[settings['MONGODB_COLLECTION_TRACK']]

    def track_status(self, status):
        dt = datetime.datetime.now()
        current_time = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
        print status
        if status == 'Online':
            previous = self.temp_track_collection.find_one()
            if previous is None:
                self.temp_track_collection.insert({"time": current_time})
            else:
                stored_time = previous['time']
                stored_minutes = self.calculate_minutes(stored_time)
                if self.calculate_minutes(current_time) - stored_minutes > 5:
                    self.tracking_collection.insert({"start": stored_time, "end": current_time})
                    self.temp_track_collection.drop()

    def calculate_minutes(self, timestamp):
        return mktime(timestamp.timetuple()) / 60