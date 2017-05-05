# coding:utf-8

import logging
import requests
import json
import os
import sys
import traceback

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class KintoneCalendarCall(object):

    def __init__(self):
        KINTONE_URL = "https://{kintone_domain}/k/v1/records.json?app={kintone_app}"
        self.url = KINTONE_URL.format(
            kintone_domain=os.environ['KINTONE_DOMAIN'],
            kintone_app=os.environ['KINTONE_APP']
        )
        self.headers_key = os.environ['KINTONE_HEADERS_KEY']
        self.api_key = os.environ['KINTONE_API_KEY']
        self.basic_headers_key = os.environ['KINTONE_BASIC_HEADERS_KEY']
        self.basic_headers_value =os.environ['KINTONE_BASIC_HEADERS_VALUE']
        self.query = u'&query=invalid not in ("無効")'

    def get_regist(self):
        try:
            headers = {self.headers_key: self.api_key}
            headers[self.basic_headers_key] = self.basic_headers_value
            response_record = requests.get(self.url + self.query , headers=headers)
            record_data = json.loads(response_record.text)
            logger.info(record_data)
            records = record_data['records']

            return records

        except Exception as e:
            logger.error(traceback.format_exc(sys.exc_info()[2]))

