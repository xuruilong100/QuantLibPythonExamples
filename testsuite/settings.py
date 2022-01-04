import unittest
from utilities import *
from QuantLib import *


class SettingsTest(unittest.TestCase):

    def testNotificationsOnDateChange(self):
        TEST_MESSAGE("Testing notifications on evaluation-date change...")

        rollback = SavedSettings()

        # ifdef QL_HIGH_RESOLUTION_DATE

        d1 = Date(11, February, 2021, 9, 17, 0)
        d2 = Date(11, February, 2021, 10, 21, 0)

        # else

        # d1 = Date(11, February, 2021)
        # d2 = Date(12, February, 2021)

        # endif

        Settings.instance().evaluationDate = d1

        flag = Flag()
        flag.registerWith(Settings.instance().evaluationDateAsObservable())

        # Set to same date, no notification
        Settings.instance().evaluationDate = d1

        self.assertFalse(flag.isUp())

        # Set to different date, notification expected
        Settings.instance().evaluationDate = d2

        self.assertFalse(not flag.isUp())
