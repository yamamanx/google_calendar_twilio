from kintone_calendar_call import KintoneCalendarCall

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class UnitTests(unittest.TestCase):

    def test_get_regist_record(self):
        kintone = KintoneCalendarCall()
        regist_records = kintone.get_regist()

        return regist_records




