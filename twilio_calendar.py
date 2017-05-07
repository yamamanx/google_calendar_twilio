# coding:utf-8

from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import logging
import os
import sys
import traceback

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class TwilioCalendar(object):

    def __init__(self):
        self.account_sid = os.environ['TWILIO_ACCOUNT_SID']
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.from_number = os.environ['TWILIO_FROM_NUMBER']

    def get_twiml(self,entry_url):
        resp = VoiceResponse()
        resp.play(entry_url)

        return str(resp)

    def make_call(self,to_number,twiml_url):
        try:
            client = Client(self.account_sid, self.auth_token)
            call = client.api.account.calls.create(
                to = to_number,
                from_= self.from_number,
                url = twiml_url,
                method= 'GET'
            )

            return call.sid

        except Exception as e:
            logger.error(traceback.format_exc(sys.exc_info()[2]))


