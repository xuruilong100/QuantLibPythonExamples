from QuantLib import Period, Days, Date, Sep, Settings

TEST_MESSAGE = print

true = True
false = False
skipSlowTest = True
knownGoodDefault = Date(16, Sep, 2015)

Settings.instance().evaluationDate = knownGoodDefault


def timeToDays(t,
               daysPerYear=360.0):
    return Period(round(t * daysPerYear), Days)


def norm(data, h):
    f2 = [0.0] * len(data)
    for i in range(len(f2)):
        f2[i] = data[i] * data[i]
    sum = 0.0
    for i in range(len(f2)):
        sum += f2[i]
    I = h * (sum - 0.5 * f2[0] - 0.5 * f2[-1])
    return I
