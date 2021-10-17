from QuantLib import Period, Days

TEST_MESSAGE = print

true = True
false = False
skipSlowTest = True


def timeToDays(t,
               daysPerYear=360.0):
    return Period(round(t * daysPerYear), Days)
