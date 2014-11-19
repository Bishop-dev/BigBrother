import gdata.spreadsheet.service
from scrapy.conf import settings
import time


class GoogleService():

    temp_activity_label = 'temp'
    datetime_template = "{0}:{1} {2}.{3}.{4}"

    def __init__(self):
        spr_client = gdata.spreadsheet.service.SpreadsheetsService()
        spr_client.email = settings['GOOGLE_EMAIL']
        spr_client.password = settings['GOOGLE_PASSWORD']
        spr_client.ProgrammaticLogin()
        self.spr_client = spr_client
        self.spreadsheet_key = settings['GOOGLE_SPREADSHEET_KEY']
        self.spreadsheet_key0 = settings['GOOGLE_SPREADSHEET_KEY0']
        self.worksheet_id = settings['GOOGLE_WORKSHEET_ID']

    def getCurrentActivity(self):
        query = gdata.spreadsheet.service.CellQuery()
        query.max_results = 3
        list_feed = self.spr_client.GetListFeed(key=self.spreadsheet_key, wksht_id=self.worksheet_id, query=query)
        if len(list_feed.entry) == 0:
            return None
        line = (list_feed.entry[0]).content.text
        timestamp = (line.split('temp:')[1])
        return time.strptime(timestamp.strip(), '%H:%M %d.%m.%Y')

    def startActivity(self, dt):
        timestamp = self.convert_datetime_to_str(dt)
        record = {self.temp_activity_label: timestamp}
        self.insert(record, self.spreadsheet_key)

    def endActivity(self, record):
        record['start'] = self.convert_datetime_to_str(record['start'])
        record['end'] = self.convert_datetime_to_str(record['end'])
        self.insert(record, self.spreadsheet_key)
        query = gdata.spreadsheet.service.CellQuery()
        query.max_results = 6
        cells = self.spr_client.GetCellsFeed(key=self.spreadsheet_key, wksht_id=self.worksheet_id, query=query)
        batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeed()
        cells.entry[3].cell.inputValue = 'x'
        self.spr_client.ExecuteBatch(batchRequest, cells.GetBatchLink().href)
        batchRequest.AddUpdate(cells.entry[3])

    def insert(self, record, sh_key):
        response = self.spr_client.InsertRow(record, sh_key, self.worksheet_id)
        if not isinstance(response, gdata.spreadsheet.SpreadsheetsList):
            raise RuntimeError("can't store to google docs")

    def convert_datetime_to_str(self, dt):
        return self.datetime_template.format(dt.hour, dt.minute, dt.day, dt.month, dt.year)