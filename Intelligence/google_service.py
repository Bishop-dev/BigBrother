import gdata.spreadsheet.service
from scrapy.conf import settings
import time


class GoogleService():

    temp_activity_label = 'temp_activity'
    datetime_template = "{0}:{1} {2}.{3}.{4}"

    def __init__(self):
        spr_client = gdata.spreadsheet.service.SpreadsheetsService()
        spr_client.email = settings['GOOGLE_EMAIL']
        spr_client.password = settings['GOOGLE_PASSWORD']
        spr_client.ProgrammaticLogin()
        self.spr_client = spr_client
        self.spreadsheet_key = settings['GOOGLE_SPREADSHEET_KEY']
        self.worksheet_id = settings['GOOGLE_WORKSHEET_ID']

    def getCurrentActivity(self):
        query = gdata.spreadsheet.service.CellQuery()
        query.max_results = 1
        list_feed = self.spr_client.GetListFeed(key=self.spreadsheet_key, wksht_id=self.worksheet_id, query=query)
        if list_feed.entry[0] is None:
            return None
        line = (list_feed.entry[0]).content.text
        timestamp = (line.split(',')[1]).replace('track: ', '')
        return time.strptime(timestamp, '%H:%M %d.%b.%Y')
        # for entry in list_feed.entry:
        #     print "%s: %s\n" % (entry.title.text, entry.content.text)
        # return self.temp_track_collection.find_one()

    def startActivity(self, dt):
        timestamp = self.datetime_template.format(dt.hour, dt.minute, dt.day, dt.month, dt.year)
        record = {self.temp_activity_label: timestamp}
        self.insert(record)

    def endActivity(self, record):
        self.insert(record)

        # self.tracking_collection.insert(record)
        # self.temp_track_collection.drop()

    def insert(self, record):
        response = self.spr_client.InsertRow(record, self.spreadsheet_key, self.worksheet_id)
        if not isinstance(response, gdata.spreadsheet.SpreadsheetsList):
            raise RuntimeError("can't store to google docs")


        # dict1 = {"test1": "test2", "test3": "12"}
        # print dict1
        # entry = self.spr_client.InsertRow(dict1, self.spreadsheet_key, self.worksheet_id)
        # if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
        #   print "Insert row succeeded."
        # else:
        #   print "Insert row failed."
        # query = gdata.spreadsheet.service.CellQuery()
        # query.max_results = 1
        # list_feed = self.spr_client.GetListFeed(key=self.spreadsheet_key, wksht_id=self.worksheet_id, query=query)
        # for entry in list_feed.entry:
        #     print "%s: %s\n" % (entry.title.text, entry.content.text)
        #
        #
        # query.max_results = 6
        # cells = self.spr_client.GetCellsFeed(key=self.spreadsheet_key, wksht_id=self.worksheet_id, query=query)
        # batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeed()
        # cells.entry[5].cell.inputValue = ''
        # print len(cells.entry)
        # batchRequest.AddUpdate(cells.entry[5])
        # self.spr_client.ExecuteBatch(batchRequest, cells.GetBatchLink().href)