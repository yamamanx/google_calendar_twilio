# coding:utf-8

import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import logging
import os
import sys
import traceback

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class GoogleCalendar(object):

    def __init__(self):
        self.service_account_id = os.environ['GOOGLE_SERVICE_ACCOUNT_ID']

    def get_credentials(self):
        scopes = 'https://www.googleapis.com/auth/calendar'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'google_key.json',
            scopes=scopes
        )

        return credentials


    def get_schedule(self,calendar_id, time_min, time_max):
        try:
            credentials = self.get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build(
                'calendar',
                'v3',
                http=http
            )

            events = service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True
            ).execute()

            items = events['items']

            return items

        except Exception as e:
            logger.error(traceback.format_exc(sys.exc_info()[2]))










