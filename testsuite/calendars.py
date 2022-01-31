import unittest
from utilities import *
from QuantLib import *


class CalendarTest(unittest.TestCase):

    def testRussia(self):
        TEST_MESSAGE("Testing Russia holiday list...")

        expectedHol = DateVector()

        # exhaustive holiday list for the year 2012
        expectedHol.push_back(Date(1, January, 2012))
        expectedHol.push_back(Date(2, January, 2012))
        expectedHol.push_back(Date(7, January, 2012))
        expectedHol.push_back(Date(8, January, 2012))
        expectedHol.push_back(Date(14, January, 2012))
        expectedHol.push_back(Date(15, January, 2012))
        expectedHol.push_back(Date(21, January, 2012))
        expectedHol.push_back(Date(22, January, 2012))
        expectedHol.push_back(Date(28, January, 2012))
        expectedHol.push_back(Date(29, January, 2012))
        expectedHol.push_back(Date(4, February, 2012))
        expectedHol.push_back(Date(5, February, 2012))
        expectedHol.push_back(Date(11, February, 2012))
        expectedHol.push_back(Date(12, February, 2012))
        expectedHol.push_back(Date(18, February, 2012))
        expectedHol.push_back(Date(19, February, 2012))
        expectedHol.push_back(Date(23, February, 2012))
        expectedHol.push_back(Date(25, February, 2012))
        expectedHol.push_back(Date(26, February, 2012))
        expectedHol.push_back(Date(3, March, 2012))
        expectedHol.push_back(Date(4, March, 2012))
        expectedHol.push_back(Date(8, March, 2012))
        expectedHol.push_back(Date(9, March, 2012))
        expectedHol.push_back(Date(10, March, 2012))
        expectedHol.push_back(Date(17, March, 2012))
        expectedHol.push_back(Date(18, March, 2012))
        expectedHol.push_back(Date(24, March, 2012))
        expectedHol.push_back(Date(25, March, 2012))
        expectedHol.push_back(Date(31, March, 2012))
        expectedHol.push_back(Date(1, April, 2012))
        expectedHol.push_back(Date(7, April, 2012))
        expectedHol.push_back(Date(8, April, 2012))
        expectedHol.push_back(Date(14, April, 2012))
        expectedHol.push_back(Date(15, April, 2012))
        expectedHol.push_back(Date(21, April, 2012))
        expectedHol.push_back(Date(22, April, 2012))
        expectedHol.push_back(Date(29, April, 2012))
        expectedHol.push_back(Date(30, April, 2012))
        expectedHol.push_back(Date(1, May, 2012))
        expectedHol.push_back(Date(6, May, 2012))
        expectedHol.push_back(Date(9, May, 2012))
        expectedHol.push_back(Date(13, May, 2012))
        expectedHol.push_back(Date(19, May, 2012))
        expectedHol.push_back(Date(20, May, 2012))
        expectedHol.push_back(Date(26, May, 2012))
        expectedHol.push_back(Date(27, May, 2012))
        expectedHol.push_back(Date(2, June, 2012))
        expectedHol.push_back(Date(3, June, 2012))
        expectedHol.push_back(Date(10, June, 2012))
        expectedHol.push_back(Date(11, June, 2012))
        expectedHol.push_back(Date(12, June, 2012))
        expectedHol.push_back(Date(16, June, 2012))
        expectedHol.push_back(Date(17, June, 2012))
        expectedHol.push_back(Date(23, June, 2012))
        expectedHol.push_back(Date(24, June, 2012))
        expectedHol.push_back(Date(30, June, 2012))
        expectedHol.push_back(Date(1, July, 2012))
        expectedHol.push_back(Date(7, July, 2012))
        expectedHol.push_back(Date(8, July, 2012))
        expectedHol.push_back(Date(14, July, 2012))
        expectedHol.push_back(Date(15, July, 2012))
        expectedHol.push_back(Date(21, July, 2012))
        expectedHol.push_back(Date(22, July, 2012))
        expectedHol.push_back(Date(28, July, 2012))
        expectedHol.push_back(Date(29, July, 2012))
        expectedHol.push_back(Date(4, August, 2012))
        expectedHol.push_back(Date(5, August, 2012))
        expectedHol.push_back(Date(11, August, 2012))
        expectedHol.push_back(Date(12, August, 2012))
        expectedHol.push_back(Date(18, August, 2012))
        expectedHol.push_back(Date(19, August, 2012))
        expectedHol.push_back(Date(25, August, 2012))
        expectedHol.push_back(Date(26, August, 2012))
        expectedHol.push_back(Date(1, September, 2012))
        expectedHol.push_back(Date(2, September, 2012))
        expectedHol.push_back(Date(8, September, 2012))
        expectedHol.push_back(Date(9, September, 2012))
        expectedHol.push_back(Date(15, September, 2012))
        expectedHol.push_back(Date(16, September, 2012))
        expectedHol.push_back(Date(22, September, 2012))
        expectedHol.push_back(Date(23, September, 2012))
        expectedHol.push_back(Date(29, September, 2012))
        expectedHol.push_back(Date(30, September, 2012))
        expectedHol.push_back(Date(6, October, 2012))
        expectedHol.push_back(Date(7, October, 2012))
        expectedHol.push_back(Date(13, October, 2012))
        expectedHol.push_back(Date(14, October, 2012))
        expectedHol.push_back(Date(20, October, 2012))
        expectedHol.push_back(Date(21, October, 2012))
        expectedHol.push_back(Date(27, October, 2012))
        expectedHol.push_back(Date(28, October, 2012))
        expectedHol.push_back(Date(3, November, 2012))
        expectedHol.push_back(Date(4, November, 2012))
        expectedHol.push_back(Date(5, November, 2012))
        expectedHol.push_back(Date(10, November, 2012))
        expectedHol.push_back(Date(11, November, 2012))
        expectedHol.push_back(Date(17, November, 2012))
        expectedHol.push_back(Date(18, November, 2012))
        expectedHol.push_back(Date(24, November, 2012))
        expectedHol.push_back(Date(25, November, 2012))
        expectedHol.push_back(Date(1, December, 2012))
        expectedHol.push_back(Date(2, December, 2012))
        expectedHol.push_back(Date(8, December, 2012))
        expectedHol.push_back(Date(9, December, 2012))
        expectedHol.push_back(Date(15, December, 2012))
        expectedHol.push_back(Date(16, December, 2012))
        expectedHol.push_back(Date(22, December, 2012))
        expectedHol.push_back(Date(23, December, 2012))
        expectedHol.push_back(Date(29, December, 2012))
        expectedHol.push_back(Date(30, December, 2012))
        expectedHol.push_back(Date(31, December, 2012))

        # exhaustive holiday list for the year 2013
        expectedHol.push_back(Date(1, January, 2013))
        expectedHol.push_back(Date(2, January, 2013))
        expectedHol.push_back(Date(3, January, 2013))
        expectedHol.push_back(Date(4, January, 2013))
        expectedHol.push_back(Date(5, January, 2013))
        expectedHol.push_back(Date(6, January, 2013))
        expectedHol.push_back(Date(7, January, 2013))
        expectedHol.push_back(Date(12, January, 2013))
        expectedHol.push_back(Date(13, January, 2013))
        expectedHol.push_back(Date(19, January, 2013))
        expectedHol.push_back(Date(20, January, 2013))
        expectedHol.push_back(Date(26, January, 2013))
        expectedHol.push_back(Date(27, January, 2013))
        expectedHol.push_back(Date(2, February, 2013))
        expectedHol.push_back(Date(3, February, 2013))
        expectedHol.push_back(Date(9, February, 2013))
        expectedHol.push_back(Date(10, February, 2013))
        expectedHol.push_back(Date(16, February, 2013))
        expectedHol.push_back(Date(17, February, 2013))
        expectedHol.push_back(Date(23, February, 2013))
        expectedHol.push_back(Date(24, February, 2013))
        expectedHol.push_back(Date(2, March, 2013))
        expectedHol.push_back(Date(3, March, 2013))
        expectedHol.push_back(Date(8, March, 2013))
        expectedHol.push_back(Date(9, March, 2013))
        expectedHol.push_back(Date(10, March, 2013))
        expectedHol.push_back(Date(16, March, 2013))
        expectedHol.push_back(Date(17, March, 2013))
        expectedHol.push_back(Date(23, March, 2013))
        expectedHol.push_back(Date(24, March, 2013))
        expectedHol.push_back(Date(30, March, 2013))
        expectedHol.push_back(Date(31, March, 2013))
        expectedHol.push_back(Date(6, April, 2013))
        expectedHol.push_back(Date(7, April, 2013))
        expectedHol.push_back(Date(13, April, 2013))
        expectedHol.push_back(Date(14, April, 2013))
        expectedHol.push_back(Date(20, April, 2013))
        expectedHol.push_back(Date(21, April, 2013))
        expectedHol.push_back(Date(27, April, 2013))
        expectedHol.push_back(Date(28, April, 2013))
        expectedHol.push_back(Date(1, May, 2013))
        expectedHol.push_back(Date(4, May, 2013))
        expectedHol.push_back(Date(5, May, 2013))
        expectedHol.push_back(Date(9, May, 2013))
        expectedHol.push_back(Date(11, May, 2013))
        expectedHol.push_back(Date(12, May, 2013))
        expectedHol.push_back(Date(18, May, 2013))
        expectedHol.push_back(Date(19, May, 2013))
        expectedHol.push_back(Date(25, May, 2013))
        expectedHol.push_back(Date(26, May, 2013))
        expectedHol.push_back(Date(1, June, 2013))
        expectedHol.push_back(Date(2, June, 2013))
        expectedHol.push_back(Date(8, June, 2013))
        expectedHol.push_back(Date(9, June, 2013))
        expectedHol.push_back(Date(12, June, 2013))
        expectedHol.push_back(Date(15, June, 2013))
        expectedHol.push_back(Date(16, June, 2013))
        expectedHol.push_back(Date(22, June, 2013))
        expectedHol.push_back(Date(23, June, 2013))
        expectedHol.push_back(Date(29, June, 2013))
        expectedHol.push_back(Date(30, June, 2013))
        expectedHol.push_back(Date(6, July, 2013))
        expectedHol.push_back(Date(7, July, 2013))
        expectedHol.push_back(Date(13, July, 2013))
        expectedHol.push_back(Date(14, July, 2013))
        expectedHol.push_back(Date(20, July, 2013))
        expectedHol.push_back(Date(21, July, 2013))
        expectedHol.push_back(Date(27, July, 2013))
        expectedHol.push_back(Date(28, July, 2013))
        expectedHol.push_back(Date(3, August, 2013))
        expectedHol.push_back(Date(4, August, 2013))
        expectedHol.push_back(Date(10, August, 2013))
        expectedHol.push_back(Date(11, August, 2013))
        expectedHol.push_back(Date(17, August, 2013))
        expectedHol.push_back(Date(18, August, 2013))
        expectedHol.push_back(Date(24, August, 2013))
        expectedHol.push_back(Date(25, August, 2013))
        expectedHol.push_back(Date(31, August, 2013))
        expectedHol.push_back(Date(1, September, 2013))
        expectedHol.push_back(Date(7, September, 2013))
        expectedHol.push_back(Date(8, September, 2013))
        expectedHol.push_back(Date(14, September, 2013))
        expectedHol.push_back(Date(15, September, 2013))
        expectedHol.push_back(Date(21, September, 2013))
        expectedHol.push_back(Date(22, September, 2013))
        expectedHol.push_back(Date(28, September, 2013))
        expectedHol.push_back(Date(29, September, 2013))
        expectedHol.push_back(Date(5, October, 2013))
        expectedHol.push_back(Date(6, October, 2013))
        expectedHol.push_back(Date(12, October, 2013))
        expectedHol.push_back(Date(13, October, 2013))
        expectedHol.push_back(Date(19, October, 2013))
        expectedHol.push_back(Date(20, October, 2013))
        expectedHol.push_back(Date(26, October, 2013))
        expectedHol.push_back(Date(27, October, 2013))
        expectedHol.push_back(Date(2, November, 2013))
        expectedHol.push_back(Date(3, November, 2013))
        expectedHol.push_back(Date(4, November, 2013))
        expectedHol.push_back(Date(9, November, 2013))
        expectedHol.push_back(Date(10, November, 2013))
        expectedHol.push_back(Date(16, November, 2013))
        expectedHol.push_back(Date(17, November, 2013))
        expectedHol.push_back(Date(23, November, 2013))
        expectedHol.push_back(Date(24, November, 2013))
        expectedHol.push_back(Date(30, November, 2013))
        expectedHol.push_back(Date(1, December, 2013))
        expectedHol.push_back(Date(7, December, 2013))
        expectedHol.push_back(Date(8, December, 2013))
        expectedHol.push_back(Date(14, December, 2013))
        expectedHol.push_back(Date(15, December, 2013))
        expectedHol.push_back(Date(21, December, 2013))
        expectedHol.push_back(Date(22, December, 2013))
        expectedHol.push_back(Date(28, December, 2013))
        expectedHol.push_back(Date(29, December, 2013))
        expectedHol.push_back(Date(31, December, 2013))

        # exhaustive holiday list for the year 2014
        expectedHol.push_back(Date(1, January, 2014))
        expectedHol.push_back(Date(2, January, 2014))
        expectedHol.push_back(Date(3, January, 2014))
        expectedHol.push_back(Date(4, January, 2014))
        expectedHol.push_back(Date(5, January, 2014))
        expectedHol.push_back(Date(7, January, 2014))
        expectedHol.push_back(Date(11, January, 2014))
        expectedHol.push_back(Date(12, January, 2014))
        expectedHol.push_back(Date(18, January, 2014))
        expectedHol.push_back(Date(19, January, 2014))
        expectedHol.push_back(Date(25, January, 2014))
        expectedHol.push_back(Date(26, January, 2014))
        expectedHol.push_back(Date(1, February, 2014))
        expectedHol.push_back(Date(2, February, 2014))
        expectedHol.push_back(Date(8, February, 2014))
        expectedHol.push_back(Date(9, February, 2014))
        expectedHol.push_back(Date(15, February, 2014))
        expectedHol.push_back(Date(16, February, 2014))
        expectedHol.push_back(Date(22, February, 2014))
        expectedHol.push_back(Date(23, February, 2014))
        expectedHol.push_back(Date(1, March, 2014))
        expectedHol.push_back(Date(2, March, 2014))
        expectedHol.push_back(Date(8, March, 2014))
        expectedHol.push_back(Date(9, March, 2014))
        expectedHol.push_back(Date(10, March, 2014))
        expectedHol.push_back(Date(15, March, 2014))
        expectedHol.push_back(Date(16, March, 2014))
        expectedHol.push_back(Date(22, March, 2014))
        expectedHol.push_back(Date(23, March, 2014))
        expectedHol.push_back(Date(29, March, 2014))
        expectedHol.push_back(Date(30, March, 2014))
        expectedHol.push_back(Date(5, April, 2014))
        expectedHol.push_back(Date(6, April, 2014))
        expectedHol.push_back(Date(12, April, 2014))
        expectedHol.push_back(Date(13, April, 2014))
        expectedHol.push_back(Date(19, April, 2014))
        expectedHol.push_back(Date(20, April, 2014))
        expectedHol.push_back(Date(26, April, 2014))
        expectedHol.push_back(Date(27, April, 2014))
        expectedHol.push_back(Date(1, May, 2014))
        expectedHol.push_back(Date(3, May, 2014))
        expectedHol.push_back(Date(4, May, 2014))
        expectedHol.push_back(Date(9, May, 2014))
        expectedHol.push_back(Date(10, May, 2014))
        expectedHol.push_back(Date(11, May, 2014))
        expectedHol.push_back(Date(17, May, 2014))
        expectedHol.push_back(Date(18, May, 2014))
        expectedHol.push_back(Date(24, May, 2014))
        expectedHol.push_back(Date(25, May, 2014))
        expectedHol.push_back(Date(31, May, 2014))
        expectedHol.push_back(Date(1, June, 2014))
        expectedHol.push_back(Date(7, June, 2014))
        expectedHol.push_back(Date(8, June, 2014))
        expectedHol.push_back(Date(12, June, 2014))
        expectedHol.push_back(Date(14, June, 2014))
        expectedHol.push_back(Date(15, June, 2014))
        expectedHol.push_back(Date(21, June, 2014))
        expectedHol.push_back(Date(22, June, 2014))
        expectedHol.push_back(Date(28, June, 2014))
        expectedHol.push_back(Date(29, June, 2014))
        expectedHol.push_back(Date(5, July, 2014))
        expectedHol.push_back(Date(6, July, 2014))
        expectedHol.push_back(Date(12, July, 2014))
        expectedHol.push_back(Date(13, July, 2014))
        expectedHol.push_back(Date(19, July, 2014))
        expectedHol.push_back(Date(20, July, 2014))
        expectedHol.push_back(Date(26, July, 2014))
        expectedHol.push_back(Date(27, July, 2014))
        expectedHol.push_back(Date(2, August, 2014))
        expectedHol.push_back(Date(3, August, 2014))
        expectedHol.push_back(Date(9, August, 2014))
        expectedHol.push_back(Date(10, August, 2014))
        expectedHol.push_back(Date(16, August, 2014))
        expectedHol.push_back(Date(17, August, 2014))
        expectedHol.push_back(Date(23, August, 2014))
        expectedHol.push_back(Date(24, August, 2014))
        expectedHol.push_back(Date(30, August, 2014))
        expectedHol.push_back(Date(31, August, 2014))
        expectedHol.push_back(Date(6, September, 2014))
        expectedHol.push_back(Date(7, September, 2014))
        expectedHol.push_back(Date(13, September, 2014))
        expectedHol.push_back(Date(14, September, 2014))
        expectedHol.push_back(Date(20, September, 2014))
        expectedHol.push_back(Date(21, September, 2014))
        expectedHol.push_back(Date(27, September, 2014))
        expectedHol.push_back(Date(28, September, 2014))
        expectedHol.push_back(Date(4, October, 2014))
        expectedHol.push_back(Date(5, October, 2014))
        expectedHol.push_back(Date(11, October, 2014))
        expectedHol.push_back(Date(12, October, 2014))
        expectedHol.push_back(Date(18, October, 2014))
        expectedHol.push_back(Date(19, October, 2014))
        expectedHol.push_back(Date(25, October, 2014))
        expectedHol.push_back(Date(26, October, 2014))
        expectedHol.push_back(Date(1, November, 2014))
        expectedHol.push_back(Date(2, November, 2014))
        expectedHol.push_back(Date(4, November, 2014))
        expectedHol.push_back(Date(8, November, 2014))
        expectedHol.push_back(Date(9, November, 2014))
        expectedHol.push_back(Date(15, November, 2014))
        expectedHol.push_back(Date(16, November, 2014))
        expectedHol.push_back(Date(22, November, 2014))
        expectedHol.push_back(Date(23, November, 2014))
        expectedHol.push_back(Date(29, November, 2014))
        expectedHol.push_back(Date(30, November, 2014))
        expectedHol.push_back(Date(6, December, 2014))
        expectedHol.push_back(Date(7, December, 2014))
        expectedHol.push_back(Date(13, December, 2014))
        expectedHol.push_back(Date(14, December, 2014))
        expectedHol.push_back(Date(20, December, 2014))
        expectedHol.push_back(Date(21, December, 2014))
        expectedHol.push_back(Date(27, December, 2014))
        expectedHol.push_back(Date(28, December, 2014))
        expectedHol.push_back(Date(31, December, 2014))

        # exhaustive holiday list for the year 2015
        expectedHol.push_back(Date(1, January, 2015))
        expectedHol.push_back(Date(2, January, 2015))
        expectedHol.push_back(Date(3, January, 2015))
        expectedHol.push_back(Date(4, January, 2015))
        expectedHol.push_back(Date(7, January, 2015))
        expectedHol.push_back(Date(10, January, 2015))
        expectedHol.push_back(Date(11, January, 2015))
        expectedHol.push_back(Date(17, January, 2015))
        expectedHol.push_back(Date(18, January, 2015))
        expectedHol.push_back(Date(24, January, 2015))
        expectedHol.push_back(Date(25, January, 2015))
        expectedHol.push_back(Date(31, January, 2015))
        expectedHol.push_back(Date(1, February, 2015))
        expectedHol.push_back(Date(7, February, 2015))
        expectedHol.push_back(Date(8, February, 2015))
        expectedHol.push_back(Date(14, February, 2015))
        expectedHol.push_back(Date(15, February, 2015))
        expectedHol.push_back(Date(21, February, 2015))
        expectedHol.push_back(Date(22, February, 2015))
        expectedHol.push_back(Date(23, February, 2015))
        expectedHol.push_back(Date(28, February, 2015))
        expectedHol.push_back(Date(1, March, 2015))
        expectedHol.push_back(Date(7, March, 2015))
        expectedHol.push_back(Date(8, March, 2015))
        expectedHol.push_back(Date(9, March, 2015))
        expectedHol.push_back(Date(14, March, 2015))
        expectedHol.push_back(Date(15, March, 2015))
        expectedHol.push_back(Date(21, March, 2015))
        expectedHol.push_back(Date(22, March, 2015))
        expectedHol.push_back(Date(28, March, 2015))
        expectedHol.push_back(Date(29, March, 2015))
        expectedHol.push_back(Date(4, April, 2015))
        expectedHol.push_back(Date(5, April, 2015))
        expectedHol.push_back(Date(11, April, 2015))
        expectedHol.push_back(Date(12, April, 2015))
        expectedHol.push_back(Date(18, April, 2015))
        expectedHol.push_back(Date(19, April, 2015))
        expectedHol.push_back(Date(25, April, 2015))
        expectedHol.push_back(Date(26, April, 2015))
        expectedHol.push_back(Date(1, May, 2015))
        expectedHol.push_back(Date(2, May, 2015))
        expectedHol.push_back(Date(3, May, 2015))
        expectedHol.push_back(Date(9, May, 2015))
        expectedHol.push_back(Date(10, May, 2015))
        expectedHol.push_back(Date(11, May, 2015))
        expectedHol.push_back(Date(16, May, 2015))
        expectedHol.push_back(Date(17, May, 2015))
        expectedHol.push_back(Date(23, May, 2015))
        expectedHol.push_back(Date(24, May, 2015))
        expectedHol.push_back(Date(30, May, 2015))
        expectedHol.push_back(Date(31, May, 2015))
        expectedHol.push_back(Date(6, June, 2015))
        expectedHol.push_back(Date(7, June, 2015))
        expectedHol.push_back(Date(12, June, 2015))
        expectedHol.push_back(Date(13, June, 2015))
        expectedHol.push_back(Date(14, June, 2015))
        expectedHol.push_back(Date(20, June, 2015))
        expectedHol.push_back(Date(21, June, 2015))
        expectedHol.push_back(Date(27, June, 2015))
        expectedHol.push_back(Date(28, June, 2015))
        expectedHol.push_back(Date(4, July, 2015))
        expectedHol.push_back(Date(5, July, 2015))
        expectedHol.push_back(Date(11, July, 2015))
        expectedHol.push_back(Date(12, July, 2015))
        expectedHol.push_back(Date(18, July, 2015))
        expectedHol.push_back(Date(19, July, 2015))
        expectedHol.push_back(Date(25, July, 2015))
        expectedHol.push_back(Date(26, July, 2015))
        expectedHol.push_back(Date(1, August, 2015))
        expectedHol.push_back(Date(2, August, 2015))
        expectedHol.push_back(Date(8, August, 2015))
        expectedHol.push_back(Date(9, August, 2015))
        expectedHol.push_back(Date(15, August, 2015))
        expectedHol.push_back(Date(16, August, 2015))
        expectedHol.push_back(Date(22, August, 2015))
        expectedHol.push_back(Date(23, August, 2015))
        expectedHol.push_back(Date(29, August, 2015))
        expectedHol.push_back(Date(30, August, 2015))
        expectedHol.push_back(Date(5, September, 2015))
        expectedHol.push_back(Date(6, September, 2015))
        expectedHol.push_back(Date(12, September, 2015))
        expectedHol.push_back(Date(13, September, 2015))
        expectedHol.push_back(Date(19, September, 2015))
        expectedHol.push_back(Date(20, September, 2015))
        expectedHol.push_back(Date(26, September, 2015))
        expectedHol.push_back(Date(27, September, 2015))
        expectedHol.push_back(Date(3, October, 2015))
        expectedHol.push_back(Date(4, October, 2015))
        expectedHol.push_back(Date(10, October, 2015))
        expectedHol.push_back(Date(11, October, 2015))
        expectedHol.push_back(Date(17, October, 2015))
        expectedHol.push_back(Date(18, October, 2015))
        expectedHol.push_back(Date(24, October, 2015))
        expectedHol.push_back(Date(25, October, 2015))
        expectedHol.push_back(Date(31, October, 2015))
        expectedHol.push_back(Date(1, November, 2015))
        expectedHol.push_back(Date(4, November, 2015))
        expectedHol.push_back(Date(7, November, 2015))
        expectedHol.push_back(Date(8, November, 2015))
        expectedHol.push_back(Date(14, November, 2015))
        expectedHol.push_back(Date(15, November, 2015))
        expectedHol.push_back(Date(21, November, 2015))
        expectedHol.push_back(Date(22, November, 2015))
        expectedHol.push_back(Date(28, November, 2015))
        expectedHol.push_back(Date(29, November, 2015))
        expectedHol.push_back(Date(5, December, 2015))
        expectedHol.push_back(Date(6, December, 2015))
        expectedHol.push_back(Date(12, December, 2015))
        expectedHol.push_back(Date(13, December, 2015))
        expectedHol.push_back(Date(19, December, 2015))
        expectedHol.push_back(Date(20, December, 2015))
        expectedHol.push_back(Date(26, December, 2015))
        expectedHol.push_back(Date(27, December, 2015))
        expectedHol.push_back(Date(31, December, 2015))

        # exhaustive holiday list for the year 2016
        expectedHol.push_back(Date(1, January, 2016))
        expectedHol.push_back(Date(2, January, 2016))
        expectedHol.push_back(Date(3, January, 2016))
        expectedHol.push_back(Date(7, January, 2016))
        expectedHol.push_back(Date(8, January, 2016))
        expectedHol.push_back(Date(9, January, 2016))
        expectedHol.push_back(Date(10, January, 2016))
        expectedHol.push_back(Date(16, January, 2016))
        expectedHol.push_back(Date(17, January, 2016))
        expectedHol.push_back(Date(23, January, 2016))
        expectedHol.push_back(Date(24, January, 2016))
        expectedHol.push_back(Date(30, January, 2016))
        expectedHol.push_back(Date(31, January, 2016))
        expectedHol.push_back(Date(6, February, 2016))
        expectedHol.push_back(Date(7, February, 2016))
        expectedHol.push_back(Date(13, February, 2016))
        expectedHol.push_back(Date(14, February, 2016))
        expectedHol.push_back(Date(21, February, 2016))
        expectedHol.push_back(Date(23, February, 2016))
        expectedHol.push_back(Date(27, February, 2016))
        expectedHol.push_back(Date(28, February, 2016))
        expectedHol.push_back(Date(5, March, 2016))
        expectedHol.push_back(Date(6, March, 2016))
        expectedHol.push_back(Date(8, March, 2016))
        expectedHol.push_back(Date(12, March, 2016))
        expectedHol.push_back(Date(13, March, 2016))
        expectedHol.push_back(Date(19, March, 2016))
        expectedHol.push_back(Date(20, March, 2016))
        expectedHol.push_back(Date(26, March, 2016))
        expectedHol.push_back(Date(27, March, 2016))
        expectedHol.push_back(Date(2, April, 2016))
        expectedHol.push_back(Date(3, April, 2016))
        expectedHol.push_back(Date(9, April, 2016))
        expectedHol.push_back(Date(10, April, 2016))
        expectedHol.push_back(Date(16, April, 2016))
        expectedHol.push_back(Date(17, April, 2016))
        expectedHol.push_back(Date(23, April, 2016))
        expectedHol.push_back(Date(24, April, 2016))
        expectedHol.push_back(Date(30, April, 2016))
        expectedHol.push_back(Date(1, May, 2016))
        expectedHol.push_back(Date(2, May, 2016))
        expectedHol.push_back(Date(3, May, 2016))
        expectedHol.push_back(Date(7, May, 2016))
        expectedHol.push_back(Date(8, May, 2016))
        expectedHol.push_back(Date(9, May, 2016))
        expectedHol.push_back(Date(14, May, 2016))
        expectedHol.push_back(Date(15, May, 2016))
        expectedHol.push_back(Date(21, May, 2016))
        expectedHol.push_back(Date(22, May, 2016))
        expectedHol.push_back(Date(28, May, 2016))
        expectedHol.push_back(Date(29, May, 2016))
        expectedHol.push_back(Date(4, June, 2016))
        expectedHol.push_back(Date(5, June, 2016))
        expectedHol.push_back(Date(11, June, 2016))
        expectedHol.push_back(Date(12, June, 2016))
        expectedHol.push_back(Date(13, June, 2016))
        expectedHol.push_back(Date(18, June, 2016))
        expectedHol.push_back(Date(19, June, 2016))
        expectedHol.push_back(Date(25, June, 2016))
        expectedHol.push_back(Date(26, June, 2016))
        expectedHol.push_back(Date(2, July, 2016))
        expectedHol.push_back(Date(3, July, 2016))
        expectedHol.push_back(Date(9, July, 2016))
        expectedHol.push_back(Date(10, July, 2016))
        expectedHol.push_back(Date(16, July, 2016))
        expectedHol.push_back(Date(17, July, 2016))
        expectedHol.push_back(Date(23, July, 2016))
        expectedHol.push_back(Date(24, July, 2016))
        expectedHol.push_back(Date(30, July, 2016))
        expectedHol.push_back(Date(31, July, 2016))
        expectedHol.push_back(Date(6, August, 2016))
        expectedHol.push_back(Date(7, August, 2016))
        expectedHol.push_back(Date(13, August, 2016))
        expectedHol.push_back(Date(14, August, 2016))
        expectedHol.push_back(Date(20, August, 2016))
        expectedHol.push_back(Date(21, August, 2016))
        expectedHol.push_back(Date(27, August, 2016))
        expectedHol.push_back(Date(28, August, 2016))
        expectedHol.push_back(Date(3, September, 2016))
        expectedHol.push_back(Date(4, September, 2016))
        expectedHol.push_back(Date(10, September, 2016))
        expectedHol.push_back(Date(11, September, 2016))
        expectedHol.push_back(Date(17, September, 2016))
        expectedHol.push_back(Date(18, September, 2016))
        expectedHol.push_back(Date(24, September, 2016))
        expectedHol.push_back(Date(25, September, 2016))
        expectedHol.push_back(Date(1, October, 2016))
        expectedHol.push_back(Date(2, October, 2016))
        expectedHol.push_back(Date(8, October, 2016))
        expectedHol.push_back(Date(9, October, 2016))
        expectedHol.push_back(Date(15, October, 2016))
        expectedHol.push_back(Date(16, October, 2016))
        expectedHol.push_back(Date(22, October, 2016))
        expectedHol.push_back(Date(23, October, 2016))
        expectedHol.push_back(Date(29, October, 2016))
        expectedHol.push_back(Date(30, October, 2016))
        expectedHol.push_back(Date(4, November, 2016))
        expectedHol.push_back(Date(5, November, 2016))
        expectedHol.push_back(Date(6, November, 2016))
        expectedHol.push_back(Date(12, November, 2016))
        expectedHol.push_back(Date(13, November, 2016))
        expectedHol.push_back(Date(19, November, 2016))
        expectedHol.push_back(Date(20, November, 2016))
        expectedHol.push_back(Date(26, November, 2016))
        expectedHol.push_back(Date(27, November, 2016))
        expectedHol.push_back(Date(3, December, 2016))
        expectedHol.push_back(Date(4, December, 2016))
        expectedHol.push_back(Date(10, December, 2016))
        expectedHol.push_back(Date(11, December, 2016))
        expectedHol.push_back(Date(17, December, 2016))
        expectedHol.push_back(Date(18, December, 2016))
        expectedHol.push_back(Date(24, December, 2016))
        expectedHol.push_back(Date(25, December, 2016))
        expectedHol.push_back(Date(30, December, 2016))
        expectedHol.push_back(Date(31, December, 2016))

        c = Russia(Russia.MOEX)

        hol = c.holidayList(
            Date(1, January, 2012),
            Date(31, December, 2016),  # only dates for which calendars are available
            true)  # include week-ends since lists are exhaustive
        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testBrazil(self):
        TEST_MESSAGE("Testing Brazil holiday list...")

        expectedHol = DateVector()

        # expectedHol.push_back(Date(1,January,2005)) # Saturday
        expectedHol.push_back(Date(7, February, 2005))
        expectedHol.push_back(Date(8, February, 2005))
        expectedHol.push_back(Date(25, March, 2005))
        expectedHol.push_back(Date(21, April, 2005))
        # expectedHol.push_back(Date(1,May,2005)) # Sunday
        expectedHol.push_back(Date(26, May, 2005))
        expectedHol.push_back(Date(7, September, 2005))
        expectedHol.push_back(Date(12, October, 2005))
        expectedHol.push_back(Date(2, November, 2005))
        expectedHol.push_back(Date(15, November, 2005))
        # expectedHol.push_back(Date(25,December,2005)) # Sunday

        # expectedHol.push_back(Date(1,January,2006)) # Sunday
        expectedHol.push_back(Date(27, February, 2006))
        expectedHol.push_back(Date(28, February, 2006))
        expectedHol.push_back(Date(14, April, 2006))
        expectedHol.push_back(Date(21, April, 2006))
        expectedHol.push_back(Date(1, May, 2006))
        expectedHol.push_back(Date(15, June, 2006))
        expectedHol.push_back(Date(7, September, 2006))
        expectedHol.push_back(Date(12, October, 2006))
        expectedHol.push_back(Date(2, November, 2006))
        expectedHol.push_back(Date(15, November, 2006))
        expectedHol.push_back(Date(25, December, 2006))

        c = Brazil()
        hol = c.holidayList(Date(1, January, 2005), Date(31, December, 2006))
        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testItalyExchange(self):
        TEST_MESSAGE("Testing Milan Stock Exchange holiday list...")

        expectedHol = DateVector()

        expectedHol.push_back(Date(1, January, 2002))
        expectedHol.push_back(Date(29, March, 2002))
        expectedHol.push_back(Date(1, April, 2002))
        expectedHol.push_back(Date(1, May, 2002))
        expectedHol.push_back(Date(15, August, 2002))
        expectedHol.push_back(Date(24, December, 2002))
        expectedHol.push_back(Date(25, December, 2002))
        expectedHol.push_back(Date(26, December, 2002))
        expectedHol.push_back(Date(31, December, 2002))
        expectedHol.push_back(Date(1, January, 2003))
        expectedHol.push_back(Date(18, April, 2003))
        expectedHol.push_back(Date(21, April, 2003))
        expectedHol.push_back(Date(1, May, 2003))
        expectedHol.push_back(Date(15, August, 2003))
        expectedHol.push_back(Date(24, December, 2003))
        expectedHol.push_back(Date(25, December, 2003))
        expectedHol.push_back(Date(26, December, 2003))
        expectedHol.push_back(Date(31, December, 2003))
        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(9, April, 2004))
        expectedHol.push_back(Date(12, April, 2004))
        expectedHol.push_back(Date(24, December, 2004))
        expectedHol.push_back(Date(31, December, 2004))

        c = Italy(Italy.Exchange)
        hol = c.holidayList(Date(1, January, 2002), Date(31, December, 2004))
        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testUKSettlement(self):
        TEST_MESSAGE("Testing UK settlement holiday list...")

        expectedHol = DateVector()

        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(9, April, 2004))
        expectedHol.push_back(Date(12, April, 2004))
        expectedHol.push_back(Date(3, May, 2004))
        expectedHol.push_back(Date(31, May, 2004))
        expectedHol.push_back(Date(30, August, 2004))
        expectedHol.push_back(Date(27, December, 2004))
        expectedHol.push_back(Date(28, December, 2004))
        expectedHol.push_back(Date(3, January, 2005))
        expectedHol.push_back(Date(25, March, 2005))
        expectedHol.push_back(Date(28, March, 2005))
        expectedHol.push_back(Date(2, May, 2005))
        expectedHol.push_back(Date(30, May, 2005))
        expectedHol.push_back(Date(29, August, 2005))
        expectedHol.push_back(Date(26, December, 2005))
        expectedHol.push_back(Date(27, December, 2005))
        expectedHol.push_back(Date(2, January, 2006))
        expectedHol.push_back(Date(14, April, 2006))
        expectedHol.push_back(Date(17, April, 2006))
        expectedHol.push_back(Date(1, May, 2006))
        expectedHol.push_back(Date(29, May, 2006))
        expectedHol.push_back(Date(28, August, 2006))
        expectedHol.push_back(Date(25, December, 2006))
        expectedHol.push_back(Date(26, December, 2006))
        expectedHol.push_back(Date(1, January, 2007))
        expectedHol.push_back(Date(6, April, 2007))
        expectedHol.push_back(Date(9, April, 2007))
        expectedHol.push_back(Date(7, May, 2007))
        expectedHol.push_back(Date(28, May, 2007))
        expectedHol.push_back(Date(27, August, 2007))
        expectedHol.push_back(Date(25, December, 2007))
        expectedHol.push_back(Date(26, December, 2007))

        c = UnitedKingdom(UnitedKingdom.Settlement)
        hol = c.holidayList(Date(1, January, 2004), Date(31, December, 2007))
        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testUKExchange(self):
        TEST_MESSAGE("Testing London Stock Exchange holiday list...")

        expectedHol = DateVector()

        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(9, April, 2004))
        expectedHol.push_back(Date(12, April, 2004))
        expectedHol.push_back(Date(3, May, 2004))
        expectedHol.push_back(Date(31, May, 2004))
        expectedHol.push_back(Date(30, August, 2004))
        expectedHol.push_back(Date(27, December, 2004))
        expectedHol.push_back(Date(28, December, 2004))
        expectedHol.push_back(Date(3, January, 2005))
        expectedHol.push_back(Date(25, March, 2005))
        expectedHol.push_back(Date(28, March, 2005))
        expectedHol.push_back(Date(2, May, 2005))
        expectedHol.push_back(Date(30, May, 2005))
        expectedHol.push_back(Date(29, August, 2005))
        expectedHol.push_back(Date(26, December, 2005))
        expectedHol.push_back(Date(27, December, 2005))
        expectedHol.push_back(Date(2, January, 2006))
        expectedHol.push_back(Date(14, April, 2006))
        expectedHol.push_back(Date(17, April, 2006))
        expectedHol.push_back(Date(1, May, 2006))
        expectedHol.push_back(Date(29, May, 2006))
        expectedHol.push_back(Date(28, August, 2006))
        expectedHol.push_back(Date(25, December, 2006))
        expectedHol.push_back(Date(26, December, 2006))
        expectedHol.push_back(Date(1, January, 2007))
        expectedHol.push_back(Date(6, April, 2007))
        expectedHol.push_back(Date(9, April, 2007))
        expectedHol.push_back(Date(7, May, 2007))
        expectedHol.push_back(Date(28, May, 2007))
        expectedHol.push_back(Date(27, August, 2007))
        expectedHol.push_back(Date(25, December, 2007))
        expectedHol.push_back(Date(26, December, 2007))

        c = UnitedKingdom(UnitedKingdom.Exchange)
        hol = c.holidayList(Date(1, January, 2004), Date(31, December, 2007))
        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testUKMetals(self):
        TEST_MESSAGE("Testing London Metals Exchange holiday list...")

        expectedHol = DateVector()

        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(9, April, 2004))
        expectedHol.push_back(Date(12, April, 2004))
        expectedHol.push_back(Date(3, May, 2004))
        expectedHol.push_back(Date(31, May, 2004))
        expectedHol.push_back(Date(30, August, 2004))
        expectedHol.push_back(Date(27, December, 2004))
        expectedHol.push_back(Date(28, December, 2004))
        expectedHol.push_back(Date(3, January, 2005))
        expectedHol.push_back(Date(25, March, 2005))
        expectedHol.push_back(Date(28, March, 2005))
        expectedHol.push_back(Date(2, May, 2005))
        expectedHol.push_back(Date(30, May, 2005))
        expectedHol.push_back(Date(29, August, 2005))
        expectedHol.push_back(Date(26, December, 2005))
        expectedHol.push_back(Date(27, December, 2005))
        expectedHol.push_back(Date(2, January, 2006))
        expectedHol.push_back(Date(14, April, 2006))
        expectedHol.push_back(Date(17, April, 2006))
        expectedHol.push_back(Date(1, May, 2006))
        expectedHol.push_back(Date(29, May, 2006))
        expectedHol.push_back(Date(28, August, 2006))
        expectedHol.push_back(Date(25, December, 2006))
        expectedHol.push_back(Date(26, December, 2006))
        expectedHol.push_back(Date(1, January, 2007))
        expectedHol.push_back(Date(6, April, 2007))
        expectedHol.push_back(Date(9, April, 2007))
        expectedHol.push_back(Date(7, May, 2007))
        expectedHol.push_back(Date(28, May, 2007))
        expectedHol.push_back(Date(27, August, 2007))
        expectedHol.push_back(Date(25, December, 2007))
        expectedHol.push_back(Date(26, December, 2007))

        c = UnitedKingdom(UnitedKingdom.Metals)
        hol = c.holidayList(Date(1, January, 2004), Date(31, December, 2007))
        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testGermanyFrankfurt(self):
        TEST_MESSAGE("Testing Frankfurt Stock Exchange holiday list...")

        expectedHol = DateVector()

        expectedHol.push_back(Date(1, January, 2003))
        expectedHol.push_back(Date(18, April, 2003))
        expectedHol.push_back(Date(21, April, 2003))
        expectedHol.push_back(Date(1, May, 2003))
        expectedHol.push_back(Date(24, December, 2003))
        expectedHol.push_back(Date(25, December, 2003))
        expectedHol.push_back(Date(26, December, 2003))
        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(9, April, 2004))
        expectedHol.push_back(Date(12, April, 2004))
        expectedHol.push_back(Date(24, December, 2004))

        c = Germany(Germany.FrankfurtStockExchange)
        hol = c.holidayList(Date(1, January, 2003), Date(31, December, 2004))
        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testGermanyXetra(self):
        TEST_MESSAGE("Testing Xetra holiday list...")

        expectedHol = DateVector()

        expectedHol.push_back(Date(1, January, 2003))
        expectedHol.push_back(Date(18, April, 2003))
        expectedHol.push_back(Date(21, April, 2003))
        expectedHol.push_back(Date(1, May, 2003))
        expectedHol.push_back(Date(24, December, 2003))
        expectedHol.push_back(Date(25, December, 2003))
        expectedHol.push_back(Date(26, December, 2003))
        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(9, April, 2004))
        expectedHol.push_back(Date(12, April, 2004))
        expectedHol.push_back(Date(24, December, 2004))

        c = Germany(Germany.Xetra)
        hol = c.holidayList(Date(1, January, 2003), Date(31, December, 2004))
        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testGermanyEurex(self):
        TEST_MESSAGE("Testing Eurex holiday list...")

        expectedHol = DateVector()

        expectedHol.push_back(Date(1, January, 2003))
        expectedHol.push_back(Date(18, April, 2003))
        expectedHol.push_back(Date(21, April, 2003))
        expectedHol.push_back(Date(1, May, 2003))
        expectedHol.push_back(Date(24, December, 2003))
        expectedHol.push_back(Date(25, December, 2003))
        expectedHol.push_back(Date(26, December, 2003))
        expectedHol.push_back(Date(31, December, 2003))
        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(9, April, 2004))
        expectedHol.push_back(Date(12, April, 2004))
        expectedHol.push_back(Date(24, December, 2004))
        expectedHol.push_back(Date(31, December, 2004))

        c = Germany(Germany.Eurex)
        hol = c.holidayList(Date(1, January, 2003), Date(31, December, 2004))
        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testTARGET(self):
        TEST_MESSAGE("Testing TARGET holiday list...")

        expectedHol = DateVector()
        expectedHol.push_back(Date(1, January, 1999))
        expectedHol.push_back(Date(31, December, 1999))
        expectedHol.push_back(Date(21, April, 2000))
        expectedHol.push_back(Date(24, April, 2000))
        expectedHol.push_back(Date(1, May, 2000))
        expectedHol.push_back(Date(25, December, 2000))
        expectedHol.push_back(Date(26, December, 2000))
        expectedHol.push_back(Date(1, January, 2001))
        expectedHol.push_back(Date(13, April, 2001))
        expectedHol.push_back(Date(16, April, 2001))
        expectedHol.push_back(Date(1, May, 2001))
        expectedHol.push_back(Date(25, December, 2001))
        expectedHol.push_back(Date(26, December, 2001))
        expectedHol.push_back(Date(31, December, 2001))
        expectedHol.push_back(Date(1, January, 2002))
        expectedHol.push_back(Date(29, March, 2002))
        expectedHol.push_back(Date(1, April, 2002))
        expectedHol.push_back(Date(1, May, 2002))
        expectedHol.push_back(Date(25, December, 2002))
        expectedHol.push_back(Date(26, December, 2002))
        expectedHol.push_back(Date(1, January, 2003))
        expectedHol.push_back(Date(18, April, 2003))
        expectedHol.push_back(Date(21, April, 2003))
        expectedHol.push_back(Date(1, May, 2003))
        expectedHol.push_back(Date(25, December, 2003))
        expectedHol.push_back(Date(26, December, 2003))
        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(9, April, 2004))
        expectedHol.push_back(Date(12, April, 2004))
        expectedHol.push_back(Date(25, March, 2005))
        expectedHol.push_back(Date(28, March, 2005))
        expectedHol.push_back(Date(26, December, 2005))
        expectedHol.push_back(Date(14, April, 2006))
        expectedHol.push_back(Date(17, April, 2006))
        expectedHol.push_back(Date(1, May, 2006))
        expectedHol.push_back(Date(25, December, 2006))
        expectedHol.push_back(Date(26, December, 2006))

        c = TARGET()
        hol = c.holidayList(
            Date(1, January, 1999), Date(31, December, 2006))

        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testUSSettlement(self):
        TEST_MESSAGE("Testing US settlement holiday list...")

        expectedHol = DateVector()
        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(19, January, 2004))
        expectedHol.push_back(Date(16, February, 2004))
        expectedHol.push_back(Date(31, May, 2004))
        expectedHol.push_back(Date(5, July, 2004))
        expectedHol.push_back(Date(6, September, 2004))
        expectedHol.push_back(Date(11, October, 2004))
        expectedHol.push_back(Date(11, November, 2004))
        expectedHol.push_back(Date(25, November, 2004))
        expectedHol.push_back(Date(24, December, 2004))
        expectedHol.push_back(Date(31, December, 2004))
        expectedHol.push_back(Date(17, January, 2005))
        expectedHol.push_back(Date(21, February, 2005))
        expectedHol.push_back(Date(30, May, 2005))
        expectedHol.push_back(Date(4, July, 2005))
        expectedHol.push_back(Date(5, September, 2005))
        expectedHol.push_back(Date(10, October, 2005))
        expectedHol.push_back(Date(11, November, 2005))
        expectedHol.push_back(Date(24, November, 2005))
        expectedHol.push_back(Date(26, December, 2005))

        c = UnitedStates(UnitedStates.Settlement)
        hol = c.holidayList(
            Date(1, January, 2004), Date(31, December, 2005))
        self.assertFalse(len(hol) != len(expectedHol))

        for i in range(len(hol)):
            self.assertFalse(hol[i] != expectedHol[i])

        # before Uniform Monday Holiday Act
        expectedHol = DateVector()
        expectedHol.push_back(Date(2, January, 1961))
        expectedHol.push_back(Date(22, February, 1961))
        expectedHol.push_back(Date(30, May, 1961))
        expectedHol.push_back(Date(4, July, 1961))
        expectedHol.push_back(Date(4, September, 1961))
        expectedHol.push_back(Date(10, November, 1961))
        expectedHol.push_back(Date(23, November, 1961))
        expectedHol.push_back(Date(25, December, 1961))

        hol = c.holidayList(
            Date(1, January, 1961), Date(31, December, 1961))
        self.assertFalse(len(hol) != len(expectedHol))

        for i in range(len(hol)):
            self.assertFalse(hol[i] != expectedHol[i])

    def testUSGovernmentBondMarket(self):
        TEST_MESSAGE("Testing US government bond market holiday list...")

        expectedHol = DateVector()
        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(19, January, 2004))
        expectedHol.push_back(Date(16, February, 2004))
        expectedHol.push_back(Date(9, April, 2004))
        expectedHol.push_back(Date(31, May, 2004))
        expectedHol.push_back(Date(11, June, 2004))  # Reagan's funeral
        expectedHol.push_back(Date(5, July, 2004))
        expectedHol.push_back(Date(6, September, 2004))
        expectedHol.push_back(Date(11, October, 2004))
        expectedHol.push_back(Date(11, November, 2004))
        expectedHol.push_back(Date(25, November, 2004))
        expectedHol.push_back(Date(24, December, 2004))

        c = UnitedStates(UnitedStates.GovernmentBond)
        hol = c.holidayList(Date(1, January, 2004), Date(31, December, 2004))

        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testUSNewYorkStockExchange(self):
        TEST_MESSAGE("Testing New York Stock Exchange holiday list...")

        expectedHol = DateVector()
        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(19, January, 2004))
        expectedHol.push_back(Date(16, February, 2004))
        expectedHol.push_back(Date(9, April, 2004))
        expectedHol.push_back(Date(31, May, 2004))
        expectedHol.push_back(Date(11, June, 2004))
        expectedHol.push_back(Date(5, July, 2004))
        expectedHol.push_back(Date(6, September, 2004))
        expectedHol.push_back(Date(25, November, 2004))
        expectedHol.push_back(Date(24, December, 2004))
        expectedHol.push_back(Date(17, January, 2005))
        expectedHol.push_back(Date(21, February, 2005))
        expectedHol.push_back(Date(25, March, 2005))
        expectedHol.push_back(Date(30, May, 2005))
        expectedHol.push_back(Date(4, July, 2005))
        expectedHol.push_back(Date(5, September, 2005))
        expectedHol.push_back(Date(24, November, 2005))
        expectedHol.push_back(Date(26, December, 2005))
        expectedHol.push_back(Date(2, January, 2006))
        expectedHol.push_back(Date(16, January, 2006))
        expectedHol.push_back(Date(20, February, 2006))
        expectedHol.push_back(Date(14, April, 2006))
        expectedHol.push_back(Date(29, May, 2006))
        expectedHol.push_back(Date(4, July, 2006))
        expectedHol.push_back(Date(4, September, 2006))
        expectedHol.push_back(Date(23, November, 2006))
        expectedHol.push_back(Date(25, December, 2006))

        c = UnitedStates(UnitedStates.NYSE)
        hol = c.holidayList(Date(1, January, 2004), Date(31, December, 2006))

        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

        histClose = DateVector()
        histClose.push_back(Date(30, October, 2012))  # Hurricane Sandy
        histClose.push_back(Date(29, October, 2012))  # Hurricane Sandy
        histClose.push_back(Date(11, June, 2004))  # Reagan's funeral
        histClose.push_back(Date(14, September, 2001))  # September 11, 2001
        histClose.push_back(Date(13, September, 2001))  # September 11, 2001
        histClose.push_back(Date(12, September, 2001))  # September 11, 2001
        histClose.push_back(Date(11, September, 2001))  # September 11, 2001
        histClose.push_back(Date(27, April, 1994))  # Nixon's funeral.
        histClose.push_back(Date(27, September, 1985))  # Hurricane Gloria
        histClose.push_back(Date(14, July, 1977))  # 1977 Blackout
        histClose.push_back(Date(25, January, 1973))  # Johnson's funeral.
        histClose.push_back(Date(28, December, 1972))  # Truman's funeral
        histClose.push_back(Date(21, July, 1969))  # Lunar exploration nat. day
        histClose.push_back(Date(31, March, 1969))  # Eisenhower's funeral
        histClose.push_back(Date(10, February, 1969))  # heavy snow
        histClose.push_back(Date(5, July, 1968))  # Day after Independence Day
        histClose.push_back(Date(9, April, 1968))  # Mourning for MLK
        histClose.push_back(Date(24, December, 1965))  # Christmas Eve
        histClose.push_back(Date(25, November, 1963))  # Kennedy's funeral
        histClose.push_back(Date(29, May, 1961))  # Day before Decoration Day
        histClose.push_back(Date(26, December, 1958))  # Day after Christmas
        histClose.push_back(Date(24, December, 1956))  # Christmas Eve
        histClose.push_back(Date(24, December, 1954))  # Christmas Eve
        # June 12-Dec. 31, 1968
        # Four day week (closed on Wednesdays) - Paperwork Crisis
        histClose.push_back(Date(12, Jun, 1968))
        histClose.push_back(Date(19, Jun, 1968))
        histClose.push_back(Date(26, Jun, 1968))
        histClose.push_back(Date(3, Jul, 1968))
        histClose.push_back(Date(10, Jul, 1968))
        histClose.push_back(Date(17, Jul, 1968))
        histClose.push_back(Date(20, Nov, 1968))
        histClose.push_back(Date(27, Nov, 1968))
        histClose.push_back(Date(4, Dec, 1968))
        histClose.push_back(Date(11, Dec, 1968))
        histClose.push_back(Date(18, Dec, 1968))
        # Presidential election days
        histClose.push_back(Date(4, Nov, 1980))
        histClose.push_back(Date(2, Nov, 1976))
        histClose.push_back(Date(7, Nov, 1972))
        histClose.push_back(Date(5, Nov, 1968))
        histClose.push_back(Date(3, Nov, 1964))
        for i in range(len(histClose)):
            self.assertFalse(not c.isHoliday(histClose[i]))

    def testSouthKoreanSettlement(self):
        TEST_MESSAGE("Testing South-Korean settlement holiday list...")

        expectedHol = DateVector()
        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(21, January, 2004))
        expectedHol.push_back(Date(22, January, 2004))
        expectedHol.push_back(Date(23, January, 2004))
        expectedHol.push_back(Date(1, March, 2004))
        expectedHol.push_back(Date(5, April, 2004))
        expectedHol.push_back(Date(15, April, 2004))  # election day
        #    expectedHol.push_back(Date(1,May,2004)) # Saturday
        expectedHol.push_back(Date(5, May, 2004))
        expectedHol.push_back(Date(26, May, 2004))
        #    expectedHol.push_back(Date(6,June,2004)) # Sunday
        #    expectedHol.push_back(Date(17,July,2004)) # Saturday
        #    expectedHol.push_back(Date(15,August,2004)) # Sunday
        expectedHol.push_back(Date(27, September, 2004))
        expectedHol.push_back(Date(28, September, 2004))
        expectedHol.push_back(Date(29, September, 2004))
        #    expectedHol.push_back(Date(3,October,2004)) # Sunday
        #    expectedHol.push_back(Date(25,December,2004)) # Saturday

        #    expectedHol.push_back(Date(1,January,2005)) # Saturday
        expectedHol.push_back(Date(8, February, 2005))
        expectedHol.push_back(Date(9, February, 2005))
        expectedHol.push_back(Date(10, February, 2005))
        expectedHol.push_back(Date(1, March, 2005))
        expectedHol.push_back(Date(5, April, 2005))
        expectedHol.push_back(Date(5, May, 2005))
        #    expectedHol.push_back(Date(15,May,2005)) # Sunday
        expectedHol.push_back(Date(6, June, 2005))
        #    expectedHol.push_back(Date(17,July,2005)) # Sunday
        expectedHol.push_back(Date(15, August, 2005))
        #    expectedHol.push_back(Date(17,September,2005)) # Saturday
        #    expectedHol.push_back(Date(18,September,2005)) # Sunday
        expectedHol.push_back(Date(19, September, 2005))
        expectedHol.push_back(Date(3, October, 2005))
        #    expectedHol.push_back(Date(25,December,2005)) # Sunday

        #    expectedHol.push_back(Date(1,January,2006)) # Sunday
        #    expectedHol.push_back(Date(28,January,2006)) # Saturday
        #    expectedHol.push_back(Date(29,January,2006)) # Sunday
        expectedHol.push_back(Date(30, January, 2006))
        expectedHol.push_back(Date(1, March, 2006))
        expectedHol.push_back(Date(1, May, 2006))
        expectedHol.push_back(Date(5, May, 2006))
        expectedHol.push_back(Date(31, May, 2006))  # election
        expectedHol.push_back(Date(6, June, 2006))
        expectedHol.push_back(Date(17, July, 2006))
        expectedHol.push_back(Date(15, August, 2006))
        expectedHol.push_back(Date(3, October, 2006))
        expectedHol.push_back(Date(5, October, 2006))
        expectedHol.push_back(Date(6, October, 2006))
        #    expectedHol.push_back(Date(7,October,2006)) # Saturday
        expectedHol.push_back(Date(25, December, 2006))

        expectedHol.push_back(Date(1, January, 2007))
        #    expectedHol.push_back(Date(17,February,2007)) # Saturday
        #    expectedHol.push_back(Date(18,February,2007)) # Sunday
        expectedHol.push_back(Date(19, February, 2007))
        expectedHol.push_back(Date(1, March, 2007))
        expectedHol.push_back(Date(1, May, 2007))
        #    expectedHol.push_back(Date(5,May,2007)) # Saturday
        expectedHol.push_back(Date(24, May, 2007))
        expectedHol.push_back(Date(6, June, 2007))
        expectedHol.push_back(Date(17, July, 2007))
        expectedHol.push_back(Date(15, August, 2007))
        expectedHol.push_back(Date(24, September, 2007))
        expectedHol.push_back(Date(25, September, 2007))
        expectedHol.push_back(Date(26, September, 2007))
        expectedHol.push_back(Date(3, October, 2007))
        expectedHol.push_back(Date(19, December, 2007))  # election
        expectedHol.push_back(Date(25, December, 2007))

        c = SouthKorea(SouthKorea.Settlement)
        hol = c.holidayList(Date(1, January, 2004), Date(31, December, 2007))
        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testKoreaStockExchange(self):
        TEST_MESSAGE("Testing Korea Stock Exchange holiday list...")

        expectedHol = DateVector()
        expectedHol.push_back(Date(1, January, 2004))
        expectedHol.push_back(Date(21, January, 2004))
        expectedHol.push_back(Date(22, January, 2004))
        expectedHol.push_back(Date(23, January, 2004))
        expectedHol.push_back(Date(1, March, 2004))
        expectedHol.push_back(Date(5, April, 2004))
        expectedHol.push_back(Date(15, April, 2004))  # election day
        #    expectedHol.push_back(Date(1,May,2004)) # Saturday
        expectedHol.push_back(Date(5, May, 2004))
        expectedHol.push_back(Date(26, May, 2004))
        #    expectedHol.push_back(Date(6,June,2004)) # Sunday
        #    expectedHol.push_back(Date(17,July,2004)) # Saturday
        #    expectedHol.push_back(Date(15,August,2004)) # Sunday
        expectedHol.push_back(Date(27, September, 2004))
        expectedHol.push_back(Date(28, September, 2004))
        expectedHol.push_back(Date(29, September, 2004))
        #    expectedHol.push_back(Date(3,October,2004)) # Sunday
        #    expectedHol.push_back(Date(25,December,2004)) # Saturday
        expectedHol.push_back(Date(31, December, 2004))
        #    expectedHol.push_back(Date(1,January,2005)) # Saturday
        expectedHol.push_back(Date(8, February, 2005))
        expectedHol.push_back(Date(9, February, 2005))
        expectedHol.push_back(Date(10, February, 2005))
        expectedHol.push_back(Date(1, March, 2005))
        expectedHol.push_back(Date(5, April, 2005))
        expectedHol.push_back(Date(5, May, 2005))
        #    expectedHol.push_back(Date(15,May,2005)) # Sunday
        expectedHol.push_back(Date(6, June, 2005))
        #    expectedHol.push_back(Date(17,July,2005)) # Sunday
        expectedHol.push_back(Date(15, August, 2005))
        #    expectedHol.push_back(Date(17,September,2005)) # Saturday
        #    expectedHol.push_back(Date(18,September,2005)) # Sunday
        expectedHol.push_back(Date(19, September, 2005))
        expectedHol.push_back(Date(3, October, 2005))
        #    expectedHol.push_back(Date(25,December,2005)) # Sunday
        expectedHol.push_back(Date(30, December, 2005))
        #    expectedHol.push_back(Date(1,January,2006)) # Sunday
        #    expectedHol.push_back(Date(28,January,2006)) # Saturday
        #    expectedHol.push_back(Date(29,January,2006)) # Sunday
        expectedHol.push_back(Date(30, January, 2006))
        expectedHol.push_back(Date(1, March, 2006))
        expectedHol.push_back(Date(1, May, 2006))
        expectedHol.push_back(Date(5, May, 2006))
        expectedHol.push_back(Date(31, May, 2006))  # election
        expectedHol.push_back(Date(6, June, 2006))
        expectedHol.push_back(Date(17, July, 2006))
        expectedHol.push_back(Date(15, August, 2006))
        expectedHol.push_back(Date(3, October, 2006))
        expectedHol.push_back(Date(5, October, 2006))
        expectedHol.push_back(Date(6, October, 2006))
        #    expectedHol.push_back(Date(7,October,2006)) # Saturday
        expectedHol.push_back(Date(25, December, 2006))
        expectedHol.push_back(Date(29, December, 2006))
        expectedHol.push_back(Date(1, January, 2007))
        #    expectedHol.push_back(Date(17,February,2007)) # Saturday
        #    expectedHol.push_back(Date(18,February,2007)) # Sunday
        expectedHol.push_back(Date(19, February, 2007))
        expectedHol.push_back(Date(1, March, 2007))
        expectedHol.push_back(Date(1, May, 2007))
        #    expectedHol.push_back(Date(5,May,2007)) # Saturday
        expectedHol.push_back(Date(24, May, 2007))
        expectedHol.push_back(Date(6, June, 2007))
        expectedHol.push_back(Date(17, July, 2007))
        expectedHol.push_back(Date(15, August, 2007))
        expectedHol.push_back(Date(24, September, 2007))
        expectedHol.push_back(Date(25, September, 2007))
        expectedHol.push_back(Date(26, September, 2007))
        expectedHol.push_back(Date(3, October, 2007))
        expectedHol.push_back(Date(19, December, 2007))  # election
        expectedHol.push_back(Date(25, December, 2007))
        expectedHol.push_back(Date(31, December, 2007))

        c = SouthKorea(SouthKorea.KRX)
        hol = c.holidayList(Date(1, January, 2004), Date(31, December, 2007))

        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testChinaSSE(self):
        TEST_MESSAGE("Testing China Shanghai Stock Exchange holiday list...")

        expectedHol = DateVector()

        # China Shanghai Securities Exchange holiday list in the year 2014
        expectedHol.push_back(Date(1, Jan, 2014))
        expectedHol.push_back(Date(31, Jan, 2014))
        expectedHol.push_back(Date(3, Feb, 2014))
        expectedHol.push_back(Date(4, Feb, 2014))
        expectedHol.push_back(Date(5, Feb, 2014))
        expectedHol.push_back(Date(6, Feb, 2014))
        expectedHol.push_back(Date(7, Apr, 2014))
        expectedHol.push_back(Date(1, May, 2014))
        expectedHol.push_back(Date(2, May, 2014))
        expectedHol.push_back(Date(2, Jun, 2014))
        expectedHol.push_back(Date(8, Sep, 2014))
        expectedHol.push_back(Date(1, Oct, 2014))
        expectedHol.push_back(Date(2, Oct, 2014))
        expectedHol.push_back(Date(3, Oct, 2014))
        expectedHol.push_back(Date(6, Oct, 2014))
        expectedHol.push_back(Date(7, Oct, 2014))
        # China Shanghai Securities Exchange holiday list in the year 2015
        expectedHol.push_back(Date(1, Jan, 2015))
        expectedHol.push_back(Date(2, Jan, 2015))
        expectedHol.push_back(Date(18, Feb, 2015))
        expectedHol.push_back(Date(19, Feb, 2015))
        expectedHol.push_back(Date(20, Feb, 2015))
        expectedHol.push_back(Date(23, Feb, 2015))
        expectedHol.push_back(Date(24, Feb, 2015))
        expectedHol.push_back(Date(6, Apr, 2015))
        expectedHol.push_back(Date(1, May, 2015))
        expectedHol.push_back(Date(22, Jun, 2015))
        expectedHol.push_back(Date(3, Sep, 2015))
        expectedHol.push_back(Date(4, Sep, 2015))
        expectedHol.push_back(Date(1, Oct, 2015))
        expectedHol.push_back(Date(2, Oct, 2015))
        expectedHol.push_back(Date(5, Oct, 2015))
        expectedHol.push_back(Date(6, Oct, 2015))
        expectedHol.push_back(Date(7, Oct, 2015))
        # China Shanghai Securities Exchange holiday list in the year 2016
        expectedHol.push_back(Date(1, Jan, 2016))
        expectedHol.push_back(Date(8, Feb, 2016))
        expectedHol.push_back(Date(9, Feb, 2016))
        expectedHol.push_back(Date(10, Feb, 2016))
        expectedHol.push_back(Date(11, Feb, 2016))
        expectedHol.push_back(Date(12, Feb, 2016))
        expectedHol.push_back(Date(4, Apr, 2016))
        expectedHol.push_back(Date(2, May, 2016))
        expectedHol.push_back(Date(9, Jun, 2016))
        expectedHol.push_back(Date(10, Jun, 2016))
        expectedHol.push_back(Date(15, Sep, 2016))
        expectedHol.push_back(Date(16, Sep, 2016))
        expectedHol.push_back(Date(3, Oct, 2016))
        expectedHol.push_back(Date(4, Oct, 2016))
        expectedHol.push_back(Date(5, Oct, 2016))
        expectedHol.push_back(Date(6, Oct, 2016))
        expectedHol.push_back(Date(7, Oct, 2016))
        # China Shanghai Securities Exchange holiday list in the year 2017
        expectedHol.push_back(Date(2, Jan, 2017))
        expectedHol.push_back(Date(27, Jan, 2017))
        expectedHol.push_back(Date(30, Jan, 2017))
        expectedHol.push_back(Date(31, Jan, 2017))
        expectedHol.push_back(Date(1, Feb, 2017))
        expectedHol.push_back(Date(2, Feb, 2017))
        expectedHol.push_back(Date(3, April, 2017))
        expectedHol.push_back(Date(4, April, 2017))
        expectedHol.push_back(Date(1, May, 2017))
        expectedHol.push_back(Date(29, May, 2017))
        expectedHol.push_back(Date(30, May, 2017))
        expectedHol.push_back(Date(2, Oct, 2017))
        expectedHol.push_back(Date(3, Oct, 2017))
        expectedHol.push_back(Date(4, Oct, 2017))
        expectedHol.push_back(Date(5, Oct, 2017))
        expectedHol.push_back(Date(6, Oct, 2017))
        # China Shanghai Securities Exchange holiday list in the year 2018
        expectedHol.push_back(Date(1, Jan, 2018))
        expectedHol.push_back(Date(15, Feb, 2018))
        expectedHol.push_back(Date(16, Feb, 2018))
        expectedHol.push_back(Date(19, Feb, 2018))
        expectedHol.push_back(Date(20, Feb, 2018))
        expectedHol.push_back(Date(21, Feb, 2018))
        expectedHol.push_back(Date(5, April, 2018))
        expectedHol.push_back(Date(6, April, 2018))
        expectedHol.push_back(Date(30, April, 2018))
        expectedHol.push_back(Date(1, May, 2018))
        expectedHol.push_back(Date(18, June, 2018))
        expectedHol.push_back(Date(24, September, 2018))
        expectedHol.push_back(Date(1, Oct, 2018))
        expectedHol.push_back(Date(2, Oct, 2018))
        expectedHol.push_back(Date(3, Oct, 2018))
        expectedHol.push_back(Date(4, Oct, 2018))
        expectedHol.push_back(Date(5, Oct, 2018))
        expectedHol.push_back(Date(31, December, 2018))
        # China Shanghai Securities Exchange holiday list in the year 2019
        expectedHol.push_back(Date(1, Jan, 2019))
        expectedHol.push_back(Date(4, Feb, 2019))
        expectedHol.push_back(Date(5, Feb, 2019))
        expectedHol.push_back(Date(6, Feb, 2019))
        expectedHol.push_back(Date(7, Feb, 2019))
        expectedHol.push_back(Date(8, Feb, 2019))
        expectedHol.push_back(Date(5, April, 2019))
        expectedHol.push_back(Date(1, May, 2019))
        expectedHol.push_back(Date(2, May, 2019))
        expectedHol.push_back(Date(3, May, 2019))
        expectedHol.push_back(Date(7, June, 2019))
        expectedHol.push_back(Date(13, September, 2019))
        expectedHol.push_back(Date(1, October, 2019))
        expectedHol.push_back(Date(2, October, 2019))
        expectedHol.push_back(Date(3, October, 2019))
        expectedHol.push_back(Date(4, October, 2019))
        expectedHol.push_back(Date(7, October, 2019))
        # China Shanghai Securities Exchange holiday list in the year 2020
        expectedHol.push_back(Date(1, Jan, 2020))
        expectedHol.push_back(Date(24, Jan, 2020))
        expectedHol.push_back(Date(27, Jan, 2020))
        expectedHol.push_back(Date(28, Jan, 2020))
        expectedHol.push_back(Date(29, Jan, 2020))
        expectedHol.push_back(Date(30, Jan, 2020))
        expectedHol.push_back(Date(31, Jan, 2020))
        expectedHol.push_back(Date(6, April, 2020))
        expectedHol.push_back(Date(1, May, 2020))
        expectedHol.push_back(Date(4, May, 2020))
        expectedHol.push_back(Date(5, May, 2020))
        expectedHol.push_back(Date(25, June, 2020))
        expectedHol.push_back(Date(26, June, 2020))
        expectedHol.push_back(Date(1, October, 2020))
        expectedHol.push_back(Date(2, October, 2020))
        expectedHol.push_back(Date(5, October, 2020))
        expectedHol.push_back(Date(6, October, 2020))
        expectedHol.push_back(Date(7, October, 2020))
        expectedHol.push_back(Date(8, October, 2020))
        # China Shanghai Securities Exchange holiday list in the year 2021
        expectedHol.push_back(Date(1, Jan, 2021))
        expectedHol.push_back(Date(11, Feb, 2021))
        expectedHol.push_back(Date(12, Feb, 2021))
        expectedHol.push_back(Date(15, Feb, 2021))
        expectedHol.push_back(Date(16, Feb, 2021))
        expectedHol.push_back(Date(17, Feb, 2021))
        expectedHol.push_back(Date(5, April, 2021))
        expectedHol.push_back(Date(3, May, 2021))
        expectedHol.push_back(Date(4, May, 2021))
        expectedHol.push_back(Date(5, May, 2021))
        expectedHol.push_back(Date(14, June, 2021))
        expectedHol.push_back(Date(20, September, 2021))
        expectedHol.push_back(Date(21, September, 2021))
        expectedHol.push_back(Date(1, October, 2021))
        expectedHol.push_back(Date(4, October, 2021))
        expectedHol.push_back(Date(5, October, 2021))
        expectedHol.push_back(Date(6, October, 2021))
        expectedHol.push_back(Date(7, October, 2021))
        # China Shanghai Securities Exchange holiday list in the year 2021
        expectedHol.push_back(Date(3, Jan, 2022))
        expectedHol.push_back(Date(31, Jan, 2022))
        expectedHol.push_back(Date(1, Feb, 2022))
        expectedHol.push_back(Date(2, Feb, 2022))
        expectedHol.push_back(Date(3, Feb, 2022))
        expectedHol.push_back(Date(4, Feb, 2022))
        expectedHol.push_back(Date(4, April, 2022))
        expectedHol.push_back(Date(5, April, 2022))
        expectedHol.push_back(Date(2, May, 2022))
        expectedHol.push_back(Date(3, May, 2022))
        expectedHol.push_back(Date(4, May, 2022))
        expectedHol.push_back(Date(3, June, 2022))
        expectedHol.push_back(Date(12, September, 2022))
        expectedHol.push_back(Date(3, October, 2022))
        expectedHol.push_back(Date(4, October, 2022))
        expectedHol.push_back(Date(5, October, 2022))
        expectedHol.push_back(Date(6, October, 2022))
        expectedHol.push_back(Date(7, October, 2022))

        c = China(China.SSE)
        hol = c.holidayList(Date(1, January, 2014), Date(31, December, 2022))

        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testChinaIB(self):
        TEST_MESSAGE("Testing China Inter Bank working weekends list...")

        expectedWorkingWeekEnds = DateVector()

        # China Inter Bank working weekends list in the year 2014
        expectedWorkingWeekEnds.push_back(Date(26, Jan, 2014))
        expectedWorkingWeekEnds.push_back(Date(8, Feb, 2014))
        expectedWorkingWeekEnds.push_back(Date(4, May, 2014))
        expectedWorkingWeekEnds.push_back(Date(28, Sep, 2014))
        expectedWorkingWeekEnds.push_back(Date(11, Oct, 2014))
        # China Inter Bank working weekends list in the year 2015
        expectedWorkingWeekEnds.push_back(Date(4, Jan, 2015))
        expectedWorkingWeekEnds.push_back(Date(15, Feb, 2015))
        expectedWorkingWeekEnds.push_back(Date(28, Feb, 2015))
        expectedWorkingWeekEnds.push_back(Date(6, Sep, 2015))
        expectedWorkingWeekEnds.push_back(Date(10, Oct, 2015))
        # China Inter Bank working weekends list in the year 2016
        expectedWorkingWeekEnds.push_back(Date(6, Feb, 2016))
        expectedWorkingWeekEnds.push_back(Date(14, Feb, 2016))
        expectedWorkingWeekEnds.push_back(Date(12, Jun, 2016))
        expectedWorkingWeekEnds.push_back(Date(18, Sep, 2016))
        expectedWorkingWeekEnds.push_back(Date(8, Oct, 2016))
        expectedWorkingWeekEnds.push_back(Date(9, Oct, 2016))
        # China Inter Bank working weekends list in the year 2017
        expectedWorkingWeekEnds.push_back(Date(22, Jan, 2017))
        expectedWorkingWeekEnds.push_back(Date(4, Feb, 2017))
        expectedWorkingWeekEnds.push_back(Date(1, April, 2017))
        expectedWorkingWeekEnds.push_back(Date(27, May, 2017))
        expectedWorkingWeekEnds.push_back(Date(30, Sep, 2017))
        # China Inter Bank working weekends list in the year 2018
        expectedWorkingWeekEnds.push_back(Date(11, Feb, 2018))
        expectedWorkingWeekEnds.push_back(Date(24, Feb, 2018))
        expectedWorkingWeekEnds.push_back(Date(8, April, 2018))
        expectedWorkingWeekEnds.push_back(Date(28, April, 2018))
        expectedWorkingWeekEnds.push_back(Date(29, Sep, 2018))
        expectedWorkingWeekEnds.push_back(Date(30, Sep, 2018))
        expectedWorkingWeekEnds.push_back(Date(29, December, 2018))
        # China Inter Bank working weekends list in the year 2019
        expectedWorkingWeekEnds.push_back(Date(2, Feb, 2019))
        expectedWorkingWeekEnds.push_back(Date(3, Feb, 2019))
        expectedWorkingWeekEnds.push_back(Date(28, April, 2019))
        expectedWorkingWeekEnds.push_back(Date(5, May, 2019))
        expectedWorkingWeekEnds.push_back(Date(29, September, 2019))
        expectedWorkingWeekEnds.push_back(Date(12, October, 2019))
        # China Inter Bank working weekends list in the year 2020
        expectedWorkingWeekEnds.push_back(Date(19, January, 2020))
        expectedWorkingWeekEnds.push_back(Date(26, April, 2020))
        expectedWorkingWeekEnds.push_back(Date(9, May, 2020))
        expectedWorkingWeekEnds.push_back(Date(28, June, 2020))
        expectedWorkingWeekEnds.push_back(Date(27, September, 2020))
        expectedWorkingWeekEnds.push_back(Date(10, October, 2020))
        # China Inter Bank working weekends list in the year 2021
        expectedWorkingWeekEnds.push_back(Date(7, Feb, 2021))
        expectedWorkingWeekEnds.push_back(Date(20, Feb, 2021))
        expectedWorkingWeekEnds.push_back(Date(25, April, 2021))
        expectedWorkingWeekEnds.push_back(Date(8, May, 2021))
        expectedWorkingWeekEnds.push_back(Date(18, September, 2021))
        expectedWorkingWeekEnds.push_back(Date(26, September, 2021))
        expectedWorkingWeekEnds.push_back(Date(9, October, 2021))

        c = China(China.IB)
        start = Date(1, Jan, 2014)
        end = Date(31, Dec, 2021)

        k = 0

        while start <= end:
            if c.isBusinessDay(start) and c.isWeekend(start.weekday()):
                self.assertFalse(expectedWorkingWeekEnds[k] != start)
                k += 1

            start += Period(1, Days)

        self.assertFalse(k != (len(expectedWorkingWeekEnds)))

    def testModifiedCalendars(self):
        TEST_MESSAGE("Testing calendar modification...")

        c1 = TARGET()
        c2 = UnitedStates(UnitedStates.NYSE)
        d1 = Date(1, May, 2004)  # holiday for both calendars
        d2 = Date(26, April, 2004)  # business day

        self.assertTrue(c1.isHoliday(d1))
        self.assertTrue(c1.isBusinessDay(d2))

        self.assertTrue(c2.isHoliday(d1))
        self.assertTrue(c2.isBusinessDay(d2))

        # modify the TARGET calendar
        c1.removeHoliday(d1)
        c1.addHoliday(d2)

        # test
        addedHolidays = c1.addedHolidays()
        removedHolidays = c1.removedHolidays()

        # addedHolidays = [a for a in addedHolidays]
        # removedHolidays = [r for r in removedHolidays]

        self.assertTrue(d1 not in addedHolidays)
        self.assertTrue(d2 in addedHolidays)
        self.assertTrue(d1 in removedHolidays)
        self.assertTrue(d2 not in removedHolidays)

        self.assertFalse(c1.isHoliday(d1))
        self.assertFalse(c1.isBusinessDay(d2))

        # any instance of TARGET should be modified...
        c3 = TARGET()
        self.assertFalse(c3.isHoliday(d1))
        self.assertFalse(c3.isBusinessDay(d2))

        # ...but not other calendars
        self.assertFalse(c2.isBusinessDay(d1))
        self.assertFalse(c2.isHoliday(d2))

        # restore original holiday set---test the other way around
        c3.addHoliday(d1)
        c3.removeHoliday(d2)

        self.assertFalse(c1.isBusinessDay(d1))
        self.assertFalse(c1.isHoliday(d2))

    def testJointCalendars(self):
        TEST_MESSAGE("Testing joint calendars...")

        c1 = TARGET()
        c2 = UnitedKingdom()
        c3 = UnitedStates(UnitedStates.NYSE)
        c4 = Japan()
        c5 = Germany()

        calendar_vect = CalendarVector()
        calendar_vect.reserve(5)
        calendar_vect.push_back(c1)
        calendar_vect.push_back(c2)
        calendar_vect.push_back(c3)
        calendar_vect.push_back(c4)
        calendar_vect.push_back(c5)

        c12h = JointCalendar(c1, c2, JoinHolidays)
        c12b = JointCalendar(c1, c2, JoinBusinessDays)
        c123h = JointCalendar(c1, c2, c3, JoinHolidays)
        c123b = JointCalendar(c1, c2, c3, JoinBusinessDays)
        c1234h = JointCalendar(c1, c2, c3, c4, JoinHolidays)
        c1234b = JointCalendar(c1, c2, c3, c4, JoinBusinessDays)
        cvh = JointCalendar(calendar_vect, JoinHolidays)

        # test one year, starting today
        firstDate = Date(16, Sep, 2015) # Date.todaysDate()
        endDate = firstDate + Period(1, Years)

        d = firstDate
        while d < endDate:
            # for (d = firstDate d < endDate d++) {
            b1 = c1.isBusinessDay(d)
            b2 = c2.isBusinessDay(d)
            b3 = c3.isBusinessDay(d)
            b4 = c4.isBusinessDay(d)
            b5 = c5.isBusinessDay(d)

            self.assertFalse((b1 and b2) != c12h.isBusinessDay(d))
            self.assertFalse((b1 or b2) != c12b.isBusinessDay(d))
            self.assertFalse((b1 and b2 and b3) != c123h.isBusinessDay(d))
            self.assertFalse((b1 or b2 or b3) != c123b.isBusinessDay(d))
            self.assertFalse((b1 and b2 and b3 and b4) != c1234h.isBusinessDay(d))
            self.assertFalse((b1 or b2 or b3 or b4) != c1234b.isBusinessDay(d))
            self.assertFalse((b1 and b2 and b3 and b4 and b5) != cvh.isBusinessDay(d))
            d += Period(1, Days)

    def testBespokeCalendars(self):
        TEST_MESSAGE("Testing bespoke calendars...")

        a1 = BespokeCalendar()
        b1 = BespokeCalendar()

        testDate1 = Date(4, October, 2008)  # Saturday
        testDate2 = Date(5, October, 2008)  # Sunday
        testDate3 = Date(6, October, 2008)  # Monday
        testDate4 = Date(7, October, 2008)  # Tuesday

        self.assertFalse(not a1.isBusinessDay(testDate1))
        self.assertFalse(not a1.isBusinessDay(testDate2))
        self.assertFalse(not a1.isBusinessDay(testDate3))
        self.assertFalse(not a1.isBusinessDay(testDate4))
        self.assertFalse(not b1.isBusinessDay(testDate1))
        self.assertFalse(not b1.isBusinessDay(testDate2))
        self.assertFalse(not b1.isBusinessDay(testDate3))
        self.assertFalse(not b1.isBusinessDay(testDate4))

        a1.addWeekend(Sunday)

        self.assertFalse(not a1.isBusinessDay(testDate1))
        self.assertFalse(a1.isBusinessDay(testDate2))
        self.assertFalse(not a1.isBusinessDay(testDate3))
        self.assertFalse(not a1.isBusinessDay(testDate4))
        self.assertFalse(not b1.isBusinessDay(testDate1))
        self.assertFalse(not b1.isBusinessDay(testDate2))
        self.assertFalse(not b1.isBusinessDay(testDate3))
        self.assertFalse(not b1.isBusinessDay(testDate4))

        a1.addHoliday(testDate3)

        self.assertFalse(not a1.isBusinessDay(testDate1))
        self.assertFalse(a1.isBusinessDay(testDate2))
        self.assertFalse(a1.isBusinessDay(testDate3))
        self.assertFalse(not a1.isBusinessDay(testDate4))
        self.assertFalse(not b1.isBusinessDay(testDate1))
        self.assertFalse(not b1.isBusinessDay(testDate2))
        self.assertFalse(not b1.isBusinessDay(testDate3))
        self.assertFalse(not b1.isBusinessDay(testDate4))

        a2 = a1  # linked to a1

        a2.addWeekend(Saturday)

        self.assertFalse(a1.isBusinessDay(testDate1))
        self.assertFalse(a1.isBusinessDay(testDate2))
        self.assertFalse(a1.isBusinessDay(testDate3))
        self.assertFalse(not a1.isBusinessDay(testDate4))
        self.assertFalse(a2.isBusinessDay(testDate1))
        self.assertFalse(a2.isBusinessDay(testDate2))
        self.assertFalse(a2.isBusinessDay(testDate3))
        self.assertFalse(not a2.isBusinessDay(testDate4))

        a2.addHoliday(testDate4)

        self.assertFalse(a1.isBusinessDay(testDate1))
        self.assertFalse(a1.isBusinessDay(testDate2))
        self.assertFalse(a1.isBusinessDay(testDate3))
        self.assertFalse(a1.isBusinessDay(testDate4))
        self.assertFalse(a2.isBusinessDay(testDate1))
        self.assertFalse(a2.isBusinessDay(testDate2))
        self.assertFalse(a2.isBusinessDay(testDate3))
        self.assertFalse(a2.isBusinessDay(testDate4))

    def testEndOfMonth(self):
        TEST_MESSAGE("Testing end-of-month calculation...")

        c = TARGET()  # any calendar would be OK

        counter = Date.minDate()
        last = Date.maxDate() - Period(2, Months)

        while counter <= last:
            eom = c.endOfMonth(counter)
            # check that eom is eom
            self.assertFalse(not c.isEndOfMonth(eom))
            # check that eom is in the same month as counter
            self.assertFalse(eom.month() != counter.month())
            counter = counter + 1

    def testBusinessDaysBetween(self):
        TEST_MESSAGE("Testing calculation of business days between dates...")

        testDates = DateVector()
        testDates.push_back(Date(1, February, 2002))  # isBusinessDay = true
        testDates.push_back(Date(4, February, 2002))  # isBusinessDay = true
        testDates.push_back(Date(16, May, 2003))  # isBusinessDay = true
        testDates.push_back(Date(17, December, 2003))  # isBusinessDay = true
        testDates.push_back(Date(17, December, 2004))  # isBusinessDay = true
        testDates.push_back(Date(19, December, 2005))  # isBusinessDay = true
        testDates.push_back(Date(2, January, 2006))  # isBusinessDay = true
        testDates.push_back(Date(13, March, 2006))  # isBusinessDay = true
        testDates.push_back(Date(15, May, 2006))  # isBusinessDay = true
        testDates.push_back(Date(17, March, 2006))  # isBusinessDay = true
        testDates.push_back(Date(15, May, 2006))  # isBusinessDay = true
        testDates.push_back(Date(26, July, 2006))  # isBusinessDay = true
        testDates.push_back(Date(26, July, 2006))  # isBusinessDay = true
        testDates.push_back(Date(27, July, 2006))  # isBusinessDay = true
        testDates.push_back(Date(29, July, 2006))  # isBusinessDay = false
        testDates.push_back(Date(29, July, 2006))  # isBusinessDay = false

        # default params: from date included, to excluded
        expected = [
            1, 321, 152, 251, 252, 10, 48, 42, -38, 38, 51, 0, 1, 2, 0]

        # exclude from, include to
        expected_include_to = [
            1, 321, 152, 251, 252, 10, 48, 42, -38, 38, 51, 0, 1, 1, 0]

        # include both from and to
        expected_include_all = [
            2, 322, 153, 252, 253, 11, 49, 43, -39, 39, 52, 1, 2, 2, 0]

        # exclude both from and to
        expected_exclude_all = [
            0, 320, 151, 250, 251, 9, 47, 41, -37, 37, 50, 0, 0, 1, 0]

        calendar = Brazil()

        for i in range(1, len(testDates)):
            calculated = calendar.businessDaysBetween(
                testDates[i - 1], testDates[i], true, false)
            self.assertFalse(calculated != expected[i - 1])

            calculated = calendar.businessDaysBetween(
                testDates[i - 1], testDates[i], false, true)
            self.assertFalse(calculated != expected_include_to[i - 1])

            calculated = calendar.businessDaysBetween(
                testDates[i - 1], testDates[i], true, true)
            self.assertFalse(calculated != expected_include_all[i - 1])

            calculated = calendar.businessDaysBetween(
                testDates[i - 1], testDates[i], false, false)
            self.assertFalse(calculated != expected_exclude_all[i - 1])

    def testIntradayAddHolidays(self):
        TEST_MESSAGE("Testing addHolidays with enable-intraday...")

        # test cases taken from testModifiedCalendars

        c1 = TARGET()
        c2 = UnitedStates(UnitedStates.NYSE)
        d1 = Date(1, May, 2004)  # holiday for both calendars
        d2 = Date(26, April, 2004, 0, 0, 1, 1)  # business day

        d1Mock = Date(1, May, 2004, 1, 1, 0, 0)  # holiday for both calendars
        d2Mock = Date(26, April, 2004)  # business day

        # this works anyhow because implementation uses day() month() etc
        self.assertTrue(c1.isHoliday(d1))
        self.assertTrue(c1.isBusinessDay(d2))

        self.assertTrue(c2.isHoliday(d1))
        self.assertTrue(c2.isBusinessDay(d2))

        # now with different hourly/min/sec
        self.assertTrue(c1.isHoliday(d1Mock))
        self.assertTrue(c1.isBusinessDay(d2Mock))

        self.assertTrue(c2.isHoliday(d1Mock))
        self.assertTrue(c2.isBusinessDay(d2Mock))

        # modify the TARGET calendar
        c1.removeHoliday(d1)
        c1.addHoliday(d2)

        # test
        self.assertFalse(c1.isHoliday(d1))
        self.assertFalse(c1.isBusinessDay(d2))

        self.assertFalse(c1.isHoliday(d1Mock))
        self.assertFalse(c1.isBusinessDay(d2Mock))

        # any instance of TARGET should be modified...
        c3 = TARGET()
        self.assertFalse(c3.isHoliday(d1))
        self.assertFalse(c3.isBusinessDay(d2))

        self.assertFalse(c3.isHoliday(d1Mock))
        self.assertFalse(c3.isBusinessDay(d2Mock))

        # ...but not other calendars
        self.assertFalse(c2.isBusinessDay(d1))
        self.assertFalse(c2.isHoliday(d2))

        self.assertFalse(c2.isBusinessDay(d1Mock))
        self.assertFalse(c2.isHoliday(d2Mock))

        # restore original holiday set---test the other way around
        c3.addHoliday(d1Mock)
        c3.removeHoliday(d2Mock)

        self.assertFalse(c1.isBusinessDay(d1))
        self.assertFalse(c1.isHoliday(d2))

        self.assertFalse(c1.isBusinessDay(d1Mock))
        self.assertFalse(c1.isHoliday(d2Mock))

    def testDayLists(self):
        TEST_MESSAGE("Testing holidayList and businessDaysList...")
        germany = Germany()
        firstDate = Settings.instance().evaluationDate
        endDate = firstDate + Period(1, Years)

        holidays = germany.holidayList(firstDate, endDate, true)
        businessDays = germany.businessDayList(firstDate, endDate)

        it_holidays = 0  # holidays.begin()
        it_businessDays = 0  # businessDays.begin()
        d = firstDate
        while d < endDate:
            self.assertFalse(
                d == holidays[it_holidays] and d == businessDays[it_businessDays])
            if it_holidays != len(holidays) - 1 and d == holidays[it_holidays]:
                it_holidays += 1

            if it_businessDays != len(businessDays) - 1 and d == businessDays[it_businessDays]:
                it_businessDays += 1
            d += Period(1, Days)
