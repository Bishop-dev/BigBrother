import pymongo
from scrapy.conf import settings


class MongoService():
    time_label = 'time'

    def __init__(self):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.temp_track_collection = db[settings['MONGODB_COLLECTION_TEMP_TRACK']]
        self.tracking_collection = db[settings['MONGODB_COLLECTION_TRACK']]

    def getCurrentActivity(self):
        record = self.temp_track_collection.find_one()
        return None if record is None else record[self.time_label]

    def startActivity(self, current_time):
        self.temp_track_collection.insert({self.time_label: current_time})

    def endActivity(self, record):
        self.tracking_collection.insert(record)
        self.temp_track_collection.drop()