import unittest

from QuantLib import *

from utilities import *


class SettingsTest(unittest.TestCase):

    def testNotificationsOnDateChange(self):
        TEST_MESSAGE(
            "Testing notifications on evaluation-date change...")

        rollback = SavedSettings()

        d1 = Date(11, February, 2021, 9, 17, 0)
        d2 = Date(11, February, 2021, 10, 21, 0)

        Settings.instance().evaluationDate = d1

        flag = Flag()
        flag.registerWith(Settings.instance().evaluationDateAsObservable())

        Settings.instance().evaluationDate = d1

        self.assertFalse(flag.isUp())

        Settings.instance().evaluationDate = d2

        self.assertFalse(not flag.isUp())
