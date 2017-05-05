# coding:utf-8

import os
import logging
import sys
import traceback
from boto3 import Session
from boto3 import resource
from contextlib import closing

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class PollyMp3(object):

    def __init__(self):
        self.polly_region = os.environ['POLLY_REGION']
        self.bucket_name = os.environ['BUCKET_NAME']
        self.bucket_region = os.environ['BUCKET_REGION']
        self.voice_id = os.environ['VOICE_ID']

    def set_twiml(self,file_name,twiml_str):
        try:
            s3 = resource('s3')
            bucket = s3.Bucket(self.bucket_name)

            twiml_file_name = '%s.xml' % file_name

            bucket.put_object(
                Key=twiml_file_name,
                Body=twiml_str,
                ContentType='application/xml'
            )

            ENTRY_URL = "https://s3-{region}.amazonaws.com/{bucket}/{filename}"
            entry_url = ENTRY_URL.format(
                bucket=self.bucket_name,
                region=self.bucket_region,
                filename=twiml_file_name
            )

            return entry_url

        except Exception as e:
            logger.error(traceback.format_exc(sys.exc_info()[2]))

    def set_mp3(self,file_name,polly_text):
        try:
            session = Session(region_name=self.polly_region)
            polly = session.client("polly")
            s3 = resource('s3')
            bucket = s3.Bucket(self.bucket_name)

            response = polly.synthesize_speech(
                Text=polly_text,
                OutputFormat="mp3",
                VoiceId=self.voice_id)

            mp3_file_name = '%s.mp3' % file_name

            with closing(response["AudioStream"]) as stream:
                bucket.put_object(
                    Key=mp3_file_name,
                    Body=stream.read(),
                    ContentType = 'audio/mpeg'
                )

            ENTRY_URL = "https://s3-{region}.amazonaws.com/{bucket}/{filename}"
            entry_url = ENTRY_URL.format(
                bucket=self.bucket_name,
                region=self.bucket_region,
                filename=mp3_file_name
            )

            return entry_url

        except Exception as e:
            logger.error(traceback.format_exc(sys.exc_info()[2]))