# coding:utf-8

import os
import sys
import traceback
import logging
import logging.config
import pytz
from datetime import datetime, timedelta
from kintone_calendar_call import KintoneCalendarCall
from google_calendar import GoogleCalendar
from polly_mp3 import PollyMp3
from twilio_calendar import TwilioCalendar

DOMAIN = '@' + os.environ['DOMAIN']
TIME_ZONE = os.environ['TIME_ZONE']
TIME_LAG = int(os.environ['TIME_LAG'])

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_time_interval(time_lag = TIME_LAG):
    now = datetime.now(pytz.timezone(TIME_ZONE))
    now_start = now + timedelta(hours=time_lag)

    time_min = now_start.strftime('%Y-%m-%dT%H:00:00+09:00')
    time_max = now_start.strftime('%Y-%m-%dT%H:59:00+09:00')

    check_time = now_start.strftime('%Y%m%d%H')

    logger.info(time_min + '~' + time_max)

    return time_min,time_max,check_time


def generate_file_name(calendar_id,domain=DOMAIN):
    now = datetime.now(pytz.timezone(TIME_ZONE))

    file_name = calendar_id.replace(domain,'') + now.strftime('%Y%m%d%H%M%S')

    return file_name

def generate_time_to_str(time_str):
    replace_time = time_str.replace('+09:00','')
    str_to_time = datetime.strptime(replace_time,'%Y-%m-%dT%H:%M:%S')
    time_to_str = str_to_time.strftime('%m') + u'月' +\
                  str_to_time.strftime('%d') + u'日' + \
                  str_to_time.strftime('%H') + u'時' + \
                  str_to_time.strftime('%M') + u'分'

    logger.info(time_to_str)

    check_time = str_to_time.strftime('%Y%m%d%H')

    return time_to_str,check_time


def generate_polly_text(start_time,end_time,summary,location):
    polly_text = ''
    if start_time is not None:
        polly_text += start_time + u'から'
    if end_time is not None:
        polly_text += end_time + u'まで'
    if location is not None:
        polly_text += location + u'で'
    if summary is not None:
        polly_text += summary + u'の予定'
    else:
        polly_text += u'予定'

    polly_text += u'があります。'

    return polly_text


def main(event, context):
    try:
        time_min,time_max,check_time_from = get_time_interval()

        google = GoogleCalendar()
        kintone = KintoneCalendarCall()
        polly = PollyMp3()
        twilio = TwilioCalendar()

        regist_records = kintone.get_regist()
        logger.info(regist_records)

        for regist_record in regist_records:
            logger.info(regist_record)
            calendar_id = regist_record['calendar_id']['value']

            schedule_items = google.get_schedule(calendar_id,time_min,time_max)
            logger.info(schedule_items)

            polly_text = ''

            for schedule_item in schedule_items:
                if 'description' in schedule_item:
                    description = schedule_item['description']
                    if 'call' in description:
                        start_time = None
                        end_time = None
                        summary = None
                        location = None
                        check_time_to = ''
                        check_time_dummy = ''

                        if 'start' in schedule_item:
                            start_time,check_time_to = generate_time_to_str(schedule_item['start']['dateTime'])
                        if 'end' in schedule_item:
                            end_time,check_time_dummy = generate_time_to_str(schedule_item['end']['dateTime'])
                        if 'summary' in schedule_item:
                            summary = schedule_item['summary']
                        if 'location' in schedule_item:
                            location = schedule_item['location']

                        if check_time_from == check_time_to:
                            polly_text += generate_polly_text(start_time, end_time, summary, location)

            if len(polly_text) > 0:
                tel_number = regist_record['tel_number']['value'].replace('-','')

                if tel_number[0:1] == '0':
                    tel_number = '+81' + tel_number[1:len(tel_number)]

                logger.info(tel_number)

                file_name = generate_file_name(calendar_id)
                mp3_url = polly.set_mp3(file_name,polly_text)
                logger.info(mp3_url)

                twiml_str = twilio.get_twiml(mp3_url)
                logger.info(twiml_str)

                twiml_url = polly.set_twiml(file_name,twiml_str)
                logger.info(twiml_url)

                call_sid = twilio.make_call(tel_number,twiml_url)
                logger.info(call_sid)


    except Exception as e:
        logger.error(traceback.format_exc(sys.exc_info()[2]))


def lambda_handler(event, context):
    logger.setLevel(logging.INFO)
    main(event, context)
    return {
        'message': 'done'
    }

if __name__ == '__main__':
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    event = {}
    main(event, None)