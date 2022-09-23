import unittest
from math import sqrt

from QuantLib import *

from utilities import *


def flatYts():
    return YieldTermStructureHandle(
        FlatForward(0, TARGET(), 0.03, Actual365Fixed()))


def flatSwaptionVts():
    return SwaptionVolatilityStructureHandle(
        ConstantSwaptionVolatility(
            0, TARGET(), ModifiedFollowing,
            0.20, Actual365Fixed()))


def flatOptionletVts():
    return OptionletVolatilityStructureHandle(
        ConstantOptionletVolatility(
            0, TARGET(), ModifiedFollowing,
            0.20, Actual365Fixed()))


def md0Yts():
    euribor6mEmpty = Euribor(Period(6, Months))

    q6m = []

    r6m = []

    q6mh = [
        0.0001, 0.0001, 0.0001, 0.0003, 0.00055, 0.0009,
        0.0014, 0.0019, 0.0025, 0.0031, 0.00325, 0.00313,
        0.0031, 0.00307, 0.00309, 0.00339, 0.00316, 0.00326,
        0.00335, 0.00343, 0.00358, 0.00351, 0.00388, 0.00404,
        0.00425, 0.00442, 0.00462, 0.00386, 0.00491, 0.00647,
        0.00837, 0.01033, 0.01218, 0.01382, 0.01527, 0.01654,
        0.0177, 0.01872, 0.01959, 0.0203, 0.02088, 0.02132,
        0.02164, 0.02186, 0.02202, 0.02213, 0.02222, 0.02229,
        0.02234, 0.02238, 0.02241, 0.02243, 0.02244, 0.02245,
        0.02247, 0.0225, 0.02284, 0.02336, 0.02407, 0.0245]

    q6mh1 = [
        Period(1, Days), Period(1, Days), Period(1, Days), Period(1, Weeks),
        Period(1, Months), Period(2, Months), Period(3, Months), Period(4, Months),
        Period(5, Months), Period(6, Months)]

    q6mh2 = [
        Period(7, Months), Period(8, Months), Period(9, Months), Period(10, Months), Period(11, Months),
        Period(1, Years), Period(13, Months), Period(14, Months), Period(15, Months), Period(16, Months),
        Period(17, Months), Period(18, Months), Period(19, Months), Period(20, Months), Period(21, Months),
        Period(22, Months), Period(23, Months), Period(2, Years), Period(3, Years), Period(4, Years),
        Period(5, Years), Period(6, Years), Period(7, Years), Period(8, Years), Period(9, Years),
        Period(10, Years), Period(11, Years), Period(12, Years), Period(13, Years), Period(14, Years),
        Period(15, Years), Period(16, Years), Period(17, Years), Period(18, Years), Period(19, Years),
        Period(20, Years), Period(21, Years), Period(22, Years), Period(23, Years), Period(24, Years),
        Period(25, Years), Period(26, Years), Period(27, Years), Period(28, Years), Period(29, Years),
        Period(30, Years), Period(35, Years), Period(40, Years), Period(50, Years), Period(60, Years)]

    for i in q6mh:
        q6m.append(SimpleQuote(i))

    for i in range(10):
        r6m.append(DepositRateHelper(
            QuoteHandle(q6m[i]), q6mh1[i],
            i if i < 2 else 2, TARGET(),
            ModifiedFollowing, false, Actual360()))

    for i in range(18):
        if i + 1 != 6 and i + 1 != 12 and i + 1 != 18:
            r6m.append(FraRateHelper(
                QuoteHandle(q6m[10 + i]), i + 1,
                                          i + 7, 2, TARGET(), ModifiedFollowing,
                false, Actual360()))

    for i in range(15 + 35):
        if i + 7 == 12 or i + 7 == 18 or i + 7 >= 24:
            r6m.append(SwapRateHelper(
                QuoteHandle(q6m[10 + i]), q6mh2[i],
                TARGET(), Annual, ModifiedFollowing,
                Actual360(), euribor6mEmpty))

    res = YieldTermStructureHandle(
        PiecewiseLogLinearDiscount(
            0, TARGET(), r6m, Actual365Fixed(), LogLinear()))
    res.currentLink().enableExtrapolation()

    return res


def md0SwaptionVts():
    optionTenors = [
        Period(1, Months), Period(2, Months), Period(3, Months), Period(6, Months),
        Period(9, Months), Period(1, Years), Period(18, Months), Period(2, Years),
        Period(3, Years), Period(4, Years), Period(5, Years), Period(6, Years),
        Period(7, Years), Period(8, Years), Period(9, Years), Period(10, Years),
        Period(15, Years), Period(20, Years), Period(25, Years), Period(30, Years)]

    swapTenors = [
        Period(1, Years), Period(2, Years), Period(3, Years), Period(4, Years),
        Period(5, Years), Period(6, Years), Period(7, Years), Period(8, Years),
        Period(9, Years), Period(10, Years), Period(15, Years), Period(20, Years),
        Period(25, Years), Period(30, Years)]

    qSwAtmh = [
        1.81, 0.897, 0.819, 0.692, 0.551, 0.47, 0.416, 0.379, 0.357,
        0.335, 0.283, 0.279, 0.283, 0.287, 1.717, 0.886, 0.79, 0.69,
        0.562, 0.481, 0.425, 0.386, 0.359, 0.339, 0.29, 0.287, 0.292,
        0.296, 1.762, 0.903, 0.804, 0.693, 0.582, 0.5, 0.448, 0.411,
        0.387, 0.365, 0.31, 0.307, 0.312, 0.317, 1.662, 0.882, 0.764,
        0.67, 0.586, 0.513, 0.468, 0.432, 0.408, 0.388, 0.331, 0.325,
        0.33, 0.334, 1.53, 0.854, 0.728, 0.643, 0.565, 0.503, 0.464,
        0.435, 0.415, 0.393, 0.337, 0.33, 0.333, 0.338, 1.344, 0.786,
        0.683, 0.609, 0.54, 0.488, 0.453, 0.429, 0.411, 0.39, 0.335,
        0.329, 0.332, 0.336, 1.1, 0.711, 0.617, 0.548, 0.497, 0.456,
        0.43, 0.408, 0.392, 0.374, 0.328, 0.323, 0.326, 0.33, 0.956,
        0.638, 0.553, 0.496, 0.459, 0.427, 0.403, 0.385, 0.371, 0.359,
        0.321, 0.318, 0.323, 0.327, 0.671, 0.505, 0.45, 0.42, 0.397,
        0.375, 0.36, 0.347, 0.337, 0.329, 0.305, 0.303, 0.309, 0.313,
        0.497, 0.406, 0.378, 0.36, 0.348, 0.334, 0.323, 0.315, 0.309,
        0.304, 0.289, 0.289, 0.294, 0.297, 0.404, 0.352, 0.334, 0.322,
        0.313, 0.304, 0.296, 0.291, 0.288, 0.286, 0.278, 0.277, 0.281,
        0.282, 0.345, 0.312, 0.302, 0.294, 0.286, 0.28, 0.276, 0.274,
        0.273, 0.273, 0.267, 0.265, 0.268, 0.269, 0.305, 0.285, 0.277,
        0.271, 0.266, 0.262, 0.26, 0.259, 0.26, 0.262, 0.259, 0.256,
        0.257, 0.256, 0.282, 0.265, 0.259, 0.254, 0.251, 0.25, 0.25,
        0.251, 0.253, 0.256, 0.253, 0.25, 0.249, 0.246, 0.263, 0.248,
        0.244, 0.241, 0.24, 0.24, 0.242, 0.245, 0.249, 0.252, 0.249,
        0.245, 0.243, 0.238, 0.242, 0.234, 0.232, 0.232, 0.233, 0.235,
        0.239, 0.243, 0.247, 0.249, 0.246, 0.242, 0.237, 0.231, 0.233,
        0.234, 0.241, 0.246, 0.249, 0.253, 0.257, 0.261, 0.263, 0.264,
        0.251, 0.236, 0.222, 0.214, 0.262, 0.26, 0.262, 0.263, 0.263,
        0.266, 0.268, 0.269, 0.269, 0.265, 0.237, 0.214, 0.202, 0.196,
        0.26, 0.26, 0.261, 0.261, 0.258, 0.255, 0.252, 0.248, 0.245,
        0.24, 0.207, 0.187, 0.182, 0.176, 0.236, 0.223, 0.221, 0.218,
        0.214, 0.21, 0.207, 0.204, 0.202, 0.2, 0.175, 0.167, 0.163,
        0.158]

    qSwAtm = []
    for i in range(20):

        qSwAtmTmp = []

        for j in range(14):
            qSwAtmTmp.append(
                QuoteHandle(SimpleQuote(qSwAtmh[i * 14 + j])))

        qSwAtm.append(qSwAtmTmp)

    swaptionVolAtm = SwaptionVolatilityStructureHandle(
        SwaptionVolatilityMatrix(
            TARGET(), ModifiedFollowing,
            optionTenors, swapTenors, qSwAtm,
            Actual365Fixed()))

    optionTenorsSmile = [
        Period(3, Months), Period(1, Years), Period(5, Years),
        Period(10, Years), Period(20, Years), Period(30, Years)]
    swapTenorsSmile = [
        Period(2, Years), Period(5, Years), Period(10, Years),
        Period(20, Years), Period(30, Years)]
    strikeSpreads = [
        -0.02, -0.01, -0.0050, -0.0025, 0.0,
        0.0025, 0.0050, 0.01, 0.02]

    qSwSmile = QuoteHandleVectorVector()

    qSwSmileh = [
        2.2562, 2.2562, 2.2562, 0.1851, 0.0, -0.0389, -0.0507,
        -0.0571, -0.06, 14.9619, 14.9619, 0.1249, 0.0328, 0.0,
        -0.0075, -0.005, 0.0078, 0.0328, 0.2296, 0.2296, 0.0717,
        0.0267, 0.0, -0.0115, -0.0126, -0.0002, 0.0345, 0.6665,
        0.1607, 0.0593, 0.0245, 0.0, -0.0145, -0.0204, -0.0164,
        0.0102, 0.6509, 0.1649, 0.0632, 0.027, 0.0, -0.018,
        -0.0278, -0.0303, -0.0105, 0.6303, 0.6303, 0.6303, 0.1169,
        0.0, -0.0469, -0.0699, -0.091, -0.1065, 0.4437, 0.4437,
        0.0944, 0.0348, 0.0, -0.0206, -0.0327, -0.0439, -0.0472,
        2.1557, 0.1501, 0.0531, 0.0225, 0.0, -0.0161, -0.0272,
        -0.0391, -0.0429, 0.4365, 0.1077, 0.0414, 0.0181, 0.0,
        -0.0137, -0.0237, -0.0354, -0.0401, 0.4415, 0.1117, 0.0437,
        0.0193, 0.0, -0.015, -0.0264, -0.0407, -0.0491, 0.4301,
        0.0776, 0.0283, 0.0122, 0.0, -0.0094, -0.0165, -0.0262,
        -0.035, 0.2496, 0.0637, 0.0246, 0.0109, 0.0, -0.0086,
        -0.0153, -0.0247, -0.0334, 0.1912, 0.0569, 0.023, 0.0104,
        0.0, -0.0085, -0.0155, -0.0256, -0.0361, 0.2095, 0.06,
        0.0239, 0.0107, 0.0, -0.0087, -0.0156, -0.0254, -0.0348,
        0.2357, 0.0669, 0.0267, 0.012, 0.0, -0.0097, -0.0174,
        -0.0282, -0.0383, 0.1291, 0.0397, 0.0158, 0.007, 0.0,
        -0.0056, -0.01, -0.0158, -0.0203, 0.1281, 0.0397, 0.0159,
        0.0071, 0.0, -0.0057, -0.0102, -0.0164, -0.0215, 0.1547,
        0.0468, 0.0189, 0.0085, 0.0, -0.0069, -0.0125, -0.0205,
        -0.0283, 0.1851, 0.0522, 0.0208, 0.0093, 0.0, -0.0075,
        -0.0135, -0.0221, -0.0304, 0.1782, 0.0506, 0.02, 0.0089,
        0.0, -0.0071, -0.0128, -0.0206, -0.0276, 0.2665, 0.0654,
        0.0255, 0.0113, 0.0, -0.0091, -0.0163, -0.0265, -0.0367,
        0.2873, 0.0686, 0.0269, 0.0121, 0.0, -0.0098, -0.0179,
        -0.0298, -0.043, 0.2993, 0.0688, 0.0273, 0.0123, 0.0,
        -0.0103, -0.0189, -0.0324, -0.0494, 0.1869, 0.0501, 0.0202,
        0.0091, 0.0, -0.0076, -0.014, -0.0239, -0.0358, 0.1573,
        0.0441, 0.0178, 0.008, 0.0, -0.0066, -0.0121, -0.0202,
        -0.0294, 0.196, 0.0525, 0.0204, 0.009, 0.0, -0.0071,
        -0.0125, -0.0197, -0.0253, 0.1795, 0.0497, 0.0197, 0.0088,
        0.0, -0.0071, -0.0128, -0.0208, -0.0286, 0.1401, 0.0415,
        0.0171, 0.0078, 0.0, -0.0066, -0.0122, -0.0209, -0.0318,
        0.112, 0.0344, 0.0142, 0.0065, 0.0, -0.0055, -0.01,
        -0.0171, -0.0256, 0.1077, 0.0328, 0.0134, 0.0061, 0.0,
        -0.005, -0.0091, -0.0152, -0.0216, ]

    for i in range(30):

        qSwSmileTmp = []

        for j in range(9):
            qSwSmileTmp.append(
                QuoteHandle(SimpleQuote(qSwSmileh[i * 9 + j])))

        qSwSmile.append(qSwSmileTmp)

    qSwSmileh1 = [
        0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2,
        0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2,
        0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2,
        0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2,
        0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2,
        0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2,
        0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2,
        0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2,
        0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2,
        0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2, 0.01, 0.2, 0.8, -0.2]

    parameterFixed = [false, false, false, false]

    parameterGuess = []
    for i in range(30):

        parameterGuessTmp = []

        for j in range(4):
            parameterGuessTmp.append(
                QuoteHandle(SimpleQuote(qSwSmileh1[i * 4 + j])))

        parameterGuess.append(parameterGuessTmp)

    ec = EndCriteria(50000, 250, 1E-6, 1E-6, 1E-6)

    swapIndex = EuriborSwapIsdaFixA(
        Period(30, Years), md0Yts())
    shortSwapIndex = EuriborSwapIsdaFixA(
        Period(1, Years),
        md0Yts())

    res = SwaptionVolatilityStructureHandle(
        SwaptionVolCube1(
            swaptionVolAtm, optionTenorsSmile, swapTenorsSmile,
            strikeSpreads, qSwSmile, swapIndex, shortSwapIndex, true,
            parameterGuess, parameterFixed, true, ec,
            0.0050))

    res.currentLink().enableExtrapolation()
    return res


def md0OptionletVts():
    nOptTen = 16
    nStrikes = 12

    optionTenors = [
        Period(1, Years), Period(18, Months), Period(2, Years), Period(3, Years),
        Period(4, Years), Period(5, Years), Period(6, Years), Period(7, Years),
        Period(8, Years), Period(9, Years), Period(10, Years), Period(12, Years),
        Period(15, Years), Period(20, Years), Period(25, Years), Period(30, Years)]

    strikes = [
        0.0025, 0.0050, 0.0100, 0.0150, 0.0200, 0.0225,
        0.0250, 0.0300, 0.0350, 0.0400, 0.0500, 0.0600]

    vols = Matrix(nOptTen, nStrikes)
    volsa = [
        (1.3378, 1.3032, 1.2514, 1.081, 1.019, 0.961, 0.907, 0.862, 0.822, 0.788, 0.758, 0.709, 0.66, 0.619, 0.597, 0.579),
        (1.1882, 1.1057, 0.9823, 0.879, 0.828, 0.779, 0.736, 0.7, 0.67, 0.644, 0.621, 0.582, 0.544, 0.513, 0.496, 0.482),
        (1.1646, 1.0356, 0.857, 0.742, 0.682, 0.626, 0.585, 0.553, 0.527, 0.506, 0.488, 0.459, 0.43, 0.408, 0.396, 0.386),
        (1.1932, 1.0364, 0.8291, 0.691, 0.618, 0.553, 0.509, 0.477, 0.452, 0.433, 0.417, 0.391, 0.367, 0.35, 0.342, 0.335),
        (1.2233, 1.0489, 0.8268, 0.666, 0.582, 0.51, 0.463, 0.43, 0.405, 0.387, 0.372, 0.348, 0.326, 0.312, 0.306, 0.301),
        (1.2369, 1.0555, 0.8283, 0.659, 0.57, 0.495, 0.447, 0.414, 0.388, 0.37, 0.355, 0.331, 0.31, 0.298, 0.293, 0.289),
        (1.2498, 1.0622, 0.8307, 0.653, 0.56, 0.483, 0.434, 0.4, 0.374, 0.356, 0.341, 0.318, 0.297, 0.286, 0.282, 0.279),
        (1.2719, 1.0747, 0.8368, 0.646, 0.546, 0.465, 0.415, 0.38, 0.353, 0.335, 0.32, 0.296, 0.277, 0.268, 0.265, 0.263),
        (1.2905, 1.0858, 0.8438, 0.643, 0.536, 0.453, 0.403, 0.367, 0.339, 0.32, 0.305, 0.281, 0.262, 0.255, 0.254, 0.252),
        (1.3063, 1.0953, 0.8508, 0.642, 0.53, 0.445, 0.395, 0.358, 0.329, 0.31, 0.294, 0.271, 0.252, 0.246, 0.246, 0.244),
        (1.332, 1.1108, 0.8631, 0.642, 0.521, 0.436, 0.386, 0.348, 0.319, 0.298, 0.282, 0.258, 0.24, 0.237, 0.237, 0.236),
        (1.3513, 1.1226, 0.8732, 0.645, 0.517, 0.43, 0.381, 0.344, 0.314, 0.293, 0.277, 0.252, 0.235, 0.233, 0.234, 0.233),
        (1.395, 1.1491, 0.9003, 0.661, 0.511, 0.425, 0.38, 0.344, 0.314, 0.292, 0.275, 0.251, 0.236, 0.236, 0.238, 0.235)]

    for i in range(nStrikes):
        for j in range(nOptTen):
            vols[j][i] = volsa[i][j]

    iborIndex = Euribor(Period(6, Months), md0Yts())
    cf = CapFloorTermVolSurface(
        0, TARGET(), ModifiedFollowing, optionTenors, strikes, vols)
    stripper = OptionletStripper1(cf, iborIndex)

    return OptionletVolatilityStructureHandle(
        StrippedOptionletAdapter(stripper))


def expiriesCalBasket1():
    res = DateVector()
    referenceDate_ = Settings.instance().evaluationDate

    for i in range(1, 5 + 1):
        res.append(TARGET().advance(referenceDate_, Period(i, Years)))

    return res


def tenorsCalBasket1():
    res = PeriodVector(5, Period(10, Years))

    return res


def expiriesCalBasket2():
    referenceDate_ = Settings.instance().evaluationDate

    res = [
        TARGET().advance(referenceDate_, Period(6, Months)),
        TARGET().advance(referenceDate_, Period(12, Months)),
        TARGET().advance(referenceDate_, Period(18, Months)),
        TARGET().advance(referenceDate_, Period(24, Months)),
        TARGET().advance(referenceDate_, Period(30, Months)),
        TARGET().advance(referenceDate_, Period(36, Months)),
        TARGET().advance(referenceDate_, Period(42, Months)),
        TARGET().advance(referenceDate_, Period(48, Months)),
        TARGET().advance(referenceDate_, Period(54, Months)),
        TARGET().advance(referenceDate_, Period(60, Months))]

    return res


def expiriesCalBasket3():
    referenceDate_ = Settings.instance().evaluationDate

    res = [
        TARGET().advance(referenceDate_, Period(1, Years)),
        TARGET().advance(referenceDate_, Period(2, Years)),
        TARGET().advance(referenceDate_, Period(3, Years)),
        TARGET().advance(referenceDate_, Period(4, Years)),
        TARGET().advance(referenceDate_, Period(5, Years)),
        TARGET().advance(referenceDate_, Period(6, Years)),
        TARGET().advance(referenceDate_, Period(7, Years)),
        TARGET().advance(referenceDate_, Period(8, Years)),
        TARGET().advance(referenceDate_, Period(9, Years))]

    return res


def tenorsCalBasket3():
    res = [
        Period(9, Years), Period(8, Years), Period(7, Years), Period(6, Years), Period(5, Years),
        Period(4, Years), Period(3, Years), Period(2, Years), Period(1, Years)]
    return res


def impliedStdDevs(atm,
                   strikes,
                   prices):
    result = DoubleVector()

    for i in range(prices.size()):
        result.append(blackFormulaImpliedStdDev(
            Option.Call, strikes[i],
            atm, prices[i], 1.0, 0.0,
            0.2, 1E-8, 1000))

    return result


class MarkovFunctionalTest(unittest.TestCase):

    def testMfStateProcess(self):

        tolerance = 1E-10
        TEST_MESSAGE(
            "Testing Markov functional state process...")

        times1 = Array(0)
        vols1 = Array(1, 1.0)
        sp1 = MfStateProcess(0.00, times1, vols1)
        var11 = sp1.variance(0.0, 0.0, 1.0)
        var12 = sp1.variance(0.0, 0.0, 2.0)
        self.assertFalse(abs(var11 - 1.0) > tolerance)
        self.assertFalse(abs(var12 - 2.0) > tolerance)

        times2 = Array(2)
        vols2 = Array(3)
        times2[0] = 1.0
        times2[1] = 2.0
        vols2[0] = 1.0
        vols2[1] = 2.0
        vols2[2] = 3.0
        sp2 = MfStateProcess(0.00, times2, vols2)
        dif21 = sp2.diffusion(0.0, 0.0)
        dif22 = sp2.diffusion(0.99, 0.0)
        dif23 = sp2.diffusion(1.0, 0.0)
        dif24 = sp2.diffusion(1.9, 0.0)
        dif25 = sp2.diffusion(2.0, 0.0)
        dif26 = sp2.diffusion(3.0, 0.0)
        dif27 = sp2.diffusion(5.0, 0.0)
        self.assertFalse(abs(dif21 - 1.0) > tolerance)
        self.assertFalse(abs(dif22 - 1.0) > tolerance)
        self.assertFalse(abs(dif23 - 2.0) > tolerance)
        self.assertFalse(abs(dif24 - 2.0) > tolerance)
        self.assertFalse(abs(dif25 - 3.0) > tolerance)
        self.assertFalse(abs(dif26 - 3.0) > tolerance)
        self.assertFalse(abs(dif27 - 3.0) > tolerance)
        var21 = sp2.variance(0.0, 0.0, 0.0)
        var22 = sp2.variance(0.0, 0.0, 0.5)
        var23 = sp2.variance(0.0, 0.0, 1.0)
        var24 = sp2.variance(0.0, 0.0, 1.5)
        var25 = sp2.variance(0.0, 0.0, 3.0)
        var26 = sp2.variance(0.0, 0.0, 5.0)
        var27 = sp2.variance(1.2, 0.0, 1.0)
        self.assertFalse(abs(var21 - 0.0) > tolerance)
        self.assertFalse(abs(var22 - 0.5) > tolerance)
        self.assertFalse(abs(var23 - 1.0) > tolerance)
        self.assertFalse(abs(var24 - 3.0) > tolerance)
        self.assertFalse(abs(var25 - 14.0) > tolerance)
        self.assertFalse(abs(var26 - 32.0) > tolerance)
        self.assertFalse(abs(var27 - 5.0) > tolerance)

        sp3 = MfStateProcess(0.01, times2, vols2)
        var31 = sp3.variance(0.0, 0.0, 0.0)
        var32 = sp3.variance(0.0, 0.0, 0.5)
        var33 = sp3.variance(0.0, 0.0, 1.0)
        var34 = sp3.variance(0.0, 0.0, 1.5)
        var35 = sp3.variance(0.0, 0.0, 3.0)
        var36 = sp3.variance(0.0, 0.0, 5.0)
        var37 = sp3.variance(1.2, 0.0, 1.0)
        self.assertFalse(abs(var31 - 0.0) > tolerance)
        self.assertFalse(abs(var32 - 0.502508354208) > tolerance)
        self.assertFalse(abs(var33 - 1.01006700134) > tolerance)
        self.assertFalse(abs(var34 - 3.06070578669) > tolerance)
        self.assertFalse(abs(var35 - 14.5935513933) > tolerance)
        self.assertFalse(abs(var36 - 34.0940185819) > tolerance)
        self.assertFalse(abs(var37 - 5.18130257358) > tolerance)

    @unittest.skip("testKahaleSmileSection: ksec31 failed")
    def testKahaleSmileSection(self):

        TEST_MESSAGE(
            "Testing Kahale smile section...")

        tol = 1E-8

        atm = 0.05
        t = 1.0

        strikes0 = [
            0.01, 0.02, 0.03, 0.04, 0.05,
            0.06, 0.07, 0.08, 0.09, 0.10]

        strikes = strikes0
        money = DoubleVector()
        calls0 = DoubleVector()

        for strike in strikes:
            money.append(strike / atm)
            calls0.append(
                blackFormula(Option.Call, strike, atm, 0.50 * sqrt(t), 1.0, 0.0))

        stdDevs0 = impliedStdDevs(atm, strikes, calls0)
        sec1 = LinearInterpolatedSmileSection(
            t, strikes, stdDevs0, atm)

        ksec11 = KahaleSmileSection(
            sec1, atm, false, false, false, money)

        self.assertFalse(abs(ksec11.leftCoreStrike() - 0.01) > tol)
        self.assertFalse(abs(ksec11.rightCoreStrike() - 0.10) > tol)

        k = strikes[0]
        while k <= strikes[-1] + tol:
            pric0 = sec1.optionPrice(k)
            pric1 = ksec11.optionPrice(k)
            self.assertFalse(abs(pric0 - pric1) > tol)

            k += 0.0001

        ksec12 = KahaleSmileSection(
            sec1, atm, true, false, false, money)

        self.assertFalse(
            abs(ksec12.leftCoreStrike() - 0.02) > tol and
            abs(ksec12.leftCoreStrike() - 0.01) > tol)
        self.assertFalse(
            abs(ksec12.rightCoreStrike() - 0.10) > tol)

        for i in range(1, len(strikes)):
            pric0 = sec1.optionPrice(strikes[i])
            pric1 = ksec12.optionPrice(strikes[i])
            self.assertFalse(abs(pric0 - pric1) > tol)

        k = 0.0010
        dig00 = 1.0
        dig10 = 1.0
        while k <= 2.0 * strikes[-1] + tol:
            dig0 = ksec11.digitalOptionPrice(k)
            dig1 = ksec12.digitalOptionPrice(k)
            self.assertFalse(not (dig0 <= dig00 + tol and dig0 >= 0.0))
            self.assertFalse(not (dig1 <= dig10 + tol and dig1 >= 0.0))
            dig00 = dig0
            dig10 = dig1
            k += 0.0001

        ksec13 = KahaleSmileSection(sec1, atm, false, true, false, money)

        k = strikes[-1]
        dig0 = ksec13.digitalOptionPrice(k - 0.0010)
        while k <= 10.0 * strikes[-1] + tol:
            dig = ksec13.digitalOptionPrice(k)
            self.assertFalse(not (dig <= dig0 + tol and dig >= 0.0))
            k += 0.0001

        calls1 = calls0
        calls1[0] = (atm - strikes[0]) + 0.0010
        stdDevs1 = impliedStdDevs(atm, strikes, calls1)
        sec2 = LinearInterpolatedSmileSection(t, strikes, stdDevs1, atm)

        ksec21 = KahaleSmileSection(sec2, atm, false, false, false, money)
        ksec22 = KahaleSmileSection(sec2, atm, true, false, true, money)

        self.assertFalse(abs(ksec21.leftCoreStrike() - 0.02) > tol)
        self.assertFalse(abs(ksec22.leftCoreStrike() - 0.02) > tol)
        self.assertFalse(abs(ksec21.rightCoreStrike() - 0.10) > tol)
        self.assertFalse(abs(ksec22.rightCoreStrike() - 0.10) > tol)

        k = 0.0010
        dig00 = dig10 = 1.0
        while k <= 2.0 * strikes[-1] + tol:
            dig0 = ksec21.digitalOptionPrice(k)
            dig1 = ksec22.digitalOptionPrice(k)
            self.assertFalse(not (dig0 <= dig00 + tol and dig0 >= 0.0))
            self.assertFalse(not (dig1 <= dig10 + tol and dig1 >= 0.0))
            dig00 = dig0
            dig10 = dig1
            k += 0.0001

        calls2 = calls0
        calls2[8] = 0.9 * calls2[9] + 0.1 * calls2[8]
        stdDevs2 = impliedStdDevs(atm, strikes, calls2)
        sec3 = LinearInterpolatedSmileSection(t, strikes, stdDevs2, atm)

        ksec31 = KahaleSmileSection(sec3, atm, false, false, false, money)
        ksec32 = KahaleSmileSection(sec3, atm, true, false, true, money)

        self.assertFalse(abs(ksec31.leftCoreStrike() - 0.01) > tol)

        self.assertFalse(
            abs(ksec32.leftCoreStrike() - 0.02) > tol and
            abs(ksec32.leftCoreStrike() - 0.01) > tol)
        self.assertFalse(abs(ksec31.rightCoreStrike() - 0.08) > tol)
        self.assertFalse(abs(ksec32.rightCoreStrike() - 0.10) > tol)
        k = 0.0010
        dig00 = dig10 = 1.0
        while k <= 2.0 * strikes[-1] + tol:
            dig0 = ksec31.digitalOptionPrice(k)
            dig1 = ksec32.digitalOptionPrice(k)
            self.assertFalse(not (dig0 <= dig00 + tol and dig0 >= 0.0))
            self.assertFalse(not (dig1 <= dig10 + tol and dig1 >= 0.0))
            dig00 = dig0
            dig10 = dig1
            k += 0.0001

    def testCalibrationOneInstrumentSet(self):

        tol0 = 0.0001

        tol1 = 0.0001

        TEST_MESSAGE(
            "Testing Markov functional calibration to one instrument set...")

        savedEvalDate = Settings.instance().evaluationDate
        referenceDate = Date(14, November, 2012)
        Settings.instance().evaluationDate = referenceDate

        flatYts_ = flatYts()
        md0Yts_ = md0Yts()
        flatSwaptionVts_ = flatSwaptionVts()
        md0SwaptionVts_ = md0SwaptionVts()
        flatOptionletVts_ = flatOptionletVts()
        md0OptionletVts_ = md0OptionletVts()

        swapIndexBase = EuriborSwapIsdaFixA(Period(1, Years))
        iborIndex = Euribor(Period(6, Months))

        volStepDates = DateVector()
        vols = [1.0]

        money = [0.1, 0.25, 0.50, 0.75, 1.0, 1.25, 1.50, 2.0, 5.0]

        mf1 = MarkovFunctional(
            flatYts_, 0.01, volStepDates, vols, flatSwaptionVts_,
            expiriesCalBasket1(), tenorsCalBasket1(), swapIndexBase,
            MarkovFunctionalSettings()
            .withYGridPoints(64)
            .withYStdDevs(7.0)
            .withGaussHermitePoints(32)
            .withDigitalGap(1e-5)
            .withMarketRateAccuracy(1e-7)
            .withLowerRateBound(0.0)
            .withUpperRateBound(2.0)
            .withAdjustments(
                MarkovFunctionalSettings.KahaleSmile |
                MarkovFunctionalSettings.SmileExponentialExtrapolation)
            .withSmileMoneynessCheckpoints(money))

        outputs1 = mf1.modelOutputs()

        for i in range(outputs1.expiries_.size()):
            self.assertFalse(abs(outputs1.marketZerorate_[i] - outputs1.modelZerorate_[i]) > tol0)

        for i in range(outputs1.expiries_.size()):
            for j in range(len(outputs1.smileStrikes_[i])):
                self.assertFalse(abs(outputs1.marketCallPremium_[i][j] - outputs1.modelCallPremium_[i][j]) > tol1)
                self.assertFalse(abs(outputs1.marketPutPremium_[i][j] - outputs1.modelPutPremium_[i][j]) > tol1)

        mf2 = MarkovFunctional(
            flatYts_, 0.01, volStepDates, vols, flatOptionletVts_,
            expiriesCalBasket2(), iborIndex,
            MarkovFunctionalSettings()
            .withYGridPoints(64)
            .withYStdDevs(7.0)
            .withGaussHermitePoints(32)
            .withDigitalGap(1e-5)
            .withMarketRateAccuracy(1e-7)
            .withLowerRateBound(0.0)
            .withUpperRateBound(2.0)
            .withAdjustments(MarkovFunctionalSettings.AdjustNone)
            .withSmileMoneynessCheckpoints(money))

        outputs2 = mf2.modelOutputs()

        for i in range(outputs2.expiries_.size()):
            self.assertFalse(abs(outputs2.marketZerorate_[i] - outputs2.modelZerorate_[i]) > tol0)

        for i in range(outputs2.expiries_.size()):
            for j in range(len(outputs2.smileStrikes_[i])):
                self.assertFalse(
                    abs(outputs2.marketCallPremium_[i][j] - outputs2.modelCallPremium_[i][j]) > tol1)
                self.assertFalse(
                    abs(outputs2.marketPutPremium_[i][j] - outputs2.modelPutPremium_[i][j]) > tol1)

        mf3 = MarkovFunctional(
            md0Yts_, 0.01, volStepDates, vols, md0SwaptionVts_,
            expiriesCalBasket1(), tenorsCalBasket1(), swapIndexBase,
            MarkovFunctionalSettings()
            .withYGridPoints(128)
            .withYStdDevs(7.0)
            .withGaussHermitePoints(64)
            .withDigitalGap(1e-5)
            .withMarketRateAccuracy(1e-7)
            .withLowerRateBound(0.0)
            .withUpperRateBound(2.0)
            .withSmileMoneynessCheckpoints(money))

        outputs3 = mf3.modelOutputs()

        for i in range(outputs3.expiries_.size()):
            self.assertFalse(abs(outputs3.marketZerorate_[i] - outputs3.modelZerorate_[i]) > tol0)

        for i in range(outputs3.expiries_.size()):
            for j in range(len(outputs3.smileStrikes_[i])):
                self.assertFalse(abs(outputs3.marketCallPremium_[i][j] - outputs3.modelCallPremium_[i][j]) > tol1)

                self.assertFalse(abs(outputs3.marketPutPremium_[i][j] - outputs3.modelPutPremium_[i][j]) > tol1)

        mf4 = MarkovFunctional(
            md0Yts_, 0.01, volStepDates, vols,
            md0OptionletVts_, expiriesCalBasket2(), iborIndex,
            MarkovFunctionalSettings()
            .withYGridPoints(64)
            .withYStdDevs(7.0)
            .withGaussHermitePoints(32)
            .withDigitalGap(1e-5)
            .withMarketRateAccuracy(1e-7)
            .withLowerRateBound(0.0)
            .withUpperRateBound(2.0)
            .withSmileMoneynessCheckpoints(money))

        outputs4 = mf4.modelOutputs()

        for i in range(outputs4.expiries_.size()):
            self.assertFalse(abs(outputs4.marketZerorate_[i] - outputs4.modelZerorate_[i]) > tol0)

        for i in range(outputs4.expiries_.size()):
            for j in range(len(outputs4.smileStrikes_[i])):
                self.assertFalse(abs(outputs4.marketCallPremium_[i][j] - outputs4.modelCallPremium_[i][j]) > tol1)
                self.assertFalse(abs(outputs4.marketPutPremium_[i][j] - outputs4.modelPutPremium_[i][j]) > tol1)

        Settings.instance().evaluationDate = savedEvalDate

    def testVanillaEngines(self):

        tol1 = 0.0001

        TEST_MESSAGE(
            "Testing Markov functional vanilla engines...")

        savedEvalDate = Settings.instance().evaluationDate
        referenceDate = Date(14, November, 2012)
        Settings.instance().evaluationDate = referenceDate

        flatYts_ = flatYts()
        md0Yts_ = md0Yts()
        flatSwaptionVts_ = flatSwaptionVts()
        md0SwaptionVts_ = md0SwaptionVts()
        flatOptionletVts_ = flatOptionletVts()
        md0OptionletVts_ = md0OptionletVts()

        swapIndexBase = EuriborSwapIsdaFixA(Period(1, Years))

        volStepDates = DateVector()
        vols = [1.0]

        money = [0.1, 0.25, 0.50, 0.75, 1.0, 1.25, 1.50, 2.0, 5.0]

        iborIndex1 = Euribor(Period(6, Months), flatYts_)

        mf1 = MarkovFunctional(
            flatYts_, 0.01, volStepDates, vols, flatSwaptionVts_,
            expiriesCalBasket1(), tenorsCalBasket1(), swapIndexBase,
            MarkovFunctionalSettings()
            .withYGridPoints(64)
            .withYStdDevs(7.0)
            .withGaussHermitePoints(32)
            .withDigitalGap(1e-5)
            .withMarketRateAccuracy(1e-7)
            .withLowerRateBound(0.0)
            .withUpperRateBound(2.0)
            .withSmileMoneynessCheckpoints(money))

        outputs1 = mf1.modelOutputs()

        mfSwaptionEngine1 = Gaussian1dSwaptionEngine(mf1, 64, 7.0)
        blackSwaptionEngine1 = BlackSwaptionEngine(flatYts_, flatSwaptionVts_)

        for i in range(outputs1.expiries_.size()):
            for j in range(len(outputs1.smileStrikes_[0])):
                underlyingCall = MakeVanillaSwap(
                    outputs1.tenors_[i], iborIndex1,
                    outputs1.smileStrikes_[i][j])
                underlyingCall.withEffectiveDate(
                    TARGET().advance(outputs1.expiries_[i], 2, Days))
                underlyingCall.receiveFixed(false)
                underlyingCall = underlyingCall.makeVanillaSwap()
                underlyingPut = MakeVanillaSwap(
                    outputs1.tenors_[i], iborIndex1,
                    outputs1.smileStrikes_[i][j])
                underlyingPut.withEffectiveDate(
                    TARGET().advance(outputs1.expiries_[i], 2, Days))
                underlyingPut.receiveFixed(true)
                underlyingPut = underlyingPut.makeVanillaSwap()
                exercise = EuropeanExercise(outputs1.expiries_[i])
                swaptionC = Swaption(underlyingCall, exercise)
                swaptionP = Swaption(underlyingPut, exercise)
                swaptionC.setPricingEngine(blackSwaptionEngine1)
                swaptionP.setPricingEngine(blackSwaptionEngine1)
                blackPriceCall = swaptionC.NPV()
                blackPricePut = swaptionP.NPV()
                swaptionC.setPricingEngine(mfSwaptionEngine1)
                swaptionP.setPricingEngine(mfSwaptionEngine1)
                mfPriceCall = swaptionC.NPV()
                mfPricePut = swaptionP.NPV()
                self.assertFalse(abs(blackPriceCall - mfPriceCall) > tol1)
                self.assertFalse(abs(blackPricePut - mfPricePut) > tol1)

        iborIndex2 = Euribor(Period(6, Months), flatYts_)

        mf2 = MarkovFunctional(
            flatYts_, 0.01, volStepDates, vols, flatOptionletVts_,
            expiriesCalBasket2(), iborIndex2,
            MarkovFunctionalSettings()
            .withYGridPoints(64)
            .withYStdDevs(7.0)
            .withGaussHermitePoints(16)
            .withDigitalGap(1e-5)
            .withMarketRateAccuracy(1e-7)
            .withLowerRateBound(0.0)
            .withUpperRateBound(2.0)
            .withSmileMoneynessCheckpoints(money))

        outputs2 = mf2.modelOutputs()

        blackCapFloorEngine2 = BlackCapFloorEngine(flatYts_, flatOptionletVts_)
        mfCapFloorEngine2 = Gaussian1dCapFloorEngine(mf2, 64, 7.0)
        c2 = [
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex2, 0.01).makeCapFloor(),
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex2, 0.02).makeCapFloor(),
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex2, 0.03).makeCapFloor(),
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex2, 0.04).makeCapFloor(),
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex2, 0.05).makeCapFloor(),
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex2, 0.07).makeCapFloor(),
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex2, 0.10).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex2, 0.01).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex2, 0.02).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex2, 0.03).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex2, 0.04).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex2, 0.05).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex2, 0.07).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex2, 0.10).makeCapFloor()]

        for i in c2:
            i.setPricingEngine(blackCapFloorEngine2)
            blackPrice = i.NPV()
            i.setPricingEngine(mfCapFloorEngine2)
            mfPrice = i.NPV()
            self.assertFalse(abs(blackPrice - mfPrice) > tol1)

        iborIndex3 = Euribor(Period(6, Months), md0Yts_)

        mf3 = MarkovFunctional(
            md0Yts_, 0.01, volStepDates, vols, md0SwaptionVts_,
            expiriesCalBasket1(), tenorsCalBasket1(), swapIndexBase,
            MarkovFunctionalSettings()
            .withYGridPoints(64)
            .withYStdDevs(7.0)
            .withGaussHermitePoints(32)
            .withDigitalGap(1e-5)
            .withMarketRateAccuracy(1e-7)
            .withLowerRateBound(0.0)
            .withUpperRateBound(2.0)
            .withSmileMoneynessCheckpoints(money))

        mfSwaptionEngine3 = Gaussian1dSwaptionEngine(mf3, 64, 7.0)
        blackSwaptionEngine3 = BlackSwaptionEngine(md0Yts_, md0SwaptionVts_)

        outputs3 = mf3.modelOutputs()

        for i in range(outputs3.expiries_.size()):
            for j in range(len(outputs3.smileStrikes_[0])):
                underlyingCall = MakeVanillaSwap(
                    outputs3.tenors_[i], iborIndex3,
                    outputs3.smileStrikes_[i][j])
                underlyingCall.withEffectiveDate(
                    TARGET().advance(outputs3.expiries_[i], 2, Days))
                underlyingCall.receiveFixed(false)
                underlyingCall = underlyingCall.makeVanillaSwap()
                underlyingPut = MakeVanillaSwap(
                    outputs3.tenors_[i], iborIndex3,
                    outputs3.smileStrikes_[i][j])
                underlyingPut.withEffectiveDate(
                    TARGET().advance(outputs3.expiries_[i], 2, Days))
                underlyingPut.receiveFixed(true)
                underlyingPut = underlyingPut.makeVanillaSwap()
                exercise = EuropeanExercise(outputs3.expiries_[i])
                swaptionC = Swaption(underlyingCall, exercise)
                swaptionP = Swaption(underlyingPut, exercise)
                swaptionC.setPricingEngine(blackSwaptionEngine3)
                swaptionP.setPricingEngine(blackSwaptionEngine3)
                blackPriceCall = swaptionC.NPV()
                blackPricePut = swaptionP.NPV()
                swaptionC.setPricingEngine(mfSwaptionEngine3)
                swaptionP.setPricingEngine(mfSwaptionEngine3)
                mfPriceCall = swaptionC.NPV()
                mfPricePut = swaptionP.NPV()
                smileCorrectionCall = outputs3.marketCallPremium_[i][j] - outputs3.marketRawCallPremium_[i][j]

                smileCorrectionPut = outputs3.marketPutPremium_[i][j] - outputs3.marketRawPutPremium_[i][j]
                self.assertFalse(abs(blackPriceCall - mfPriceCall + smileCorrectionCall) > tol1)
                self.assertFalse(abs(blackPricePut - mfPricePut + smileCorrectionPut) > tol1)

        iborIndex4 = Euribor(Period(6, Months), md0Yts_)

        mf4 = MarkovFunctional(
            md0Yts_, 0.01, volStepDates, vols, md0OptionletVts_,
            expiriesCalBasket2(), iborIndex4,
            MarkovFunctionalSettings()
            .withYGridPoints(64)
            .withYStdDevs(7.0)
            .withGaussHermitePoints(32)
            .withDigitalGap(1e-5)
            .withMarketRateAccuracy(1e-7)
            .withLowerRateBound(0.0)
            .withUpperRateBound(2.0)
            .withSmileMoneynessCheckpoints(money))

        outputs4 = mf4.modelOutputs()

        blackCapFloorEngine4 = BlackCapFloorEngine(md0Yts_, md0OptionletVts_)
        mfCapFloorEngine4 = Gaussian1dCapFloorEngine(mf4, 64, 7.0)

        c4 = [
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex4, 0.01).makeCapFloor(),
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex4, 0.02).makeCapFloor(),
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex4, 0.03).makeCapFloor(),
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex4, 0.04).makeCapFloor(),
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex4, 0.05).makeCapFloor(),
            MakeCapFloor(CapFloor.Cap, Period(5, Years), iborIndex4, 0.06).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex4, 0.01).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex4, 0.02).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex4, 0.03).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex4, 0.04).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex4, 0.05).makeCapFloor(),
            MakeCapFloor(CapFloor.Floor, Period(5, Years), iborIndex4, 0.06).makeCapFloor()]

        for i in c4:
            i.setPricingEngine(blackCapFloorEngine4)
            blackPrice = i.NPV()
            i.setPricingEngine(mfCapFloorEngine4)
            mfPrice = i.NPV()
            self.assertFalse(abs(blackPrice - mfPrice) > tol1)

        Settings.instance().evaluationDate = savedEvalDate

    def testCalibrationTwoInstrumentSets(self):

        tol1 = 0.1

        TEST_MESSAGE(
            "Testing Markov functional calibration to two instrument sets...")

        savedEvalDate = Settings.instance().evaluationDate
        referenceDate = Date(14, November, 2012)
        Settings.instance().evaluationDate = referenceDate

        flatYts_ = flatYts()
        md0Yts_ = md0Yts()
        flatSwaptionVts_ = flatSwaptionVts()
        md0SwaptionVts_ = md0SwaptionVts()
        flatOptionletVts_ = flatOptionletVts()
        md0OptionletVts_ = md0OptionletVts()

        swapIndexBase = EuriborSwapIsdaFixA(Period(1, Years))

        volStepDates = [
            TARGET().advance(referenceDate, Period(1, Years)),
            TARGET().advance(referenceDate, Period(2, Years)),
            TARGET().advance(referenceDate, Period(3, Years)),
            TARGET().advance(referenceDate, Period(4, Years))]
        vols = [1.0, 1.0, 1.0, 1.0, 1.0]
        money = [0.1, 0.25, 0.50, 0.75, 1.0, 1.25, 1.50, 2.0, 5.0]

        om = LevenbergMarquardt()

        ec = EndCriteria(1000, 500, 1e-2, 1e-2, 1e-2)

        iborIndex1 = Euribor(Period(6, Months), flatYts_)

        calibrationHelper1 = []
        calibrationHelperVols1 = [0.20, 0.20, 0.20, 0.20]

        calibrationHelper1.append(
            SwaptionHelper(
                Period(1, Years), Period(4, Years),
                QuoteHandle(
                    SimpleQuote(calibrationHelperVols1[0])),
                iborIndex1, Period(1, Years), Thirty360(Thirty360.BondBasis), Actual360(),
                flatYts_))
        calibrationHelper1.append(
            SwaptionHelper(
                Period(2, Years), Period(3, Years),
                QuoteHandle(
                    SimpleQuote(calibrationHelperVols1[1])),
                iborIndex1, Period(1, Years), Thirty360(Thirty360.BondBasis), Actual360(),
                flatYts_))
        calibrationHelper1.append(
            SwaptionHelper(
                Period(3, Years), Period(2, Years),
                QuoteHandle(
                    SimpleQuote(calibrationHelperVols1[2])),
                iborIndex1, Period(1, Years), Thirty360(Thirty360.BondBasis), Actual360(),
                flatYts_))
        calibrationHelper1.append(
            SwaptionHelper(
                Period(4, Years), Period(1, Years),
                QuoteHandle(
                    SimpleQuote(calibrationHelperVols1[3])),
                iborIndex1, Period(1, Years), Thirty360(Thirty360.BondBasis), Actual360(),
                flatYts_))

        mf1 = MarkovFunctional(
            flatYts_, 0.01, volStepDates, vols, flatSwaptionVts_,
            expiriesCalBasket1(), tenorsCalBasket1(), swapIndexBase,
            MarkovFunctionalSettings()
            .withYGridPoints(64)
            .withYStdDevs(7.0)
            .withGaussHermitePoints(32)
            .withDigitalGap(1e-5)
            .withMarketRateAccuracy(1e-7)
            .withLowerRateBound(0.0)
            .withUpperRateBound(2.0)
            .withSmileMoneynessCheckpoints(money))

        mfSwaptionEngine1 = Gaussian1dSwaptionEngine(mf1, 64, 7.0)
        calibrationHelper1[0].setPricingEngine(mfSwaptionEngine1)
        calibrationHelper1[1].setPricingEngine(mfSwaptionEngine1)
        calibrationHelper1[2].setPricingEngine(mfSwaptionEngine1)
        calibrationHelper1[3].setPricingEngine(mfSwaptionEngine1)

        mf1.calibrate(calibrationHelper1, om, ec)

        ch1 = []
        ch1.append(
            MakeSwaption(
                EuriborSwapIsdaFixA(Period(4, Years), flatYts_),
                Period(1, Years)).makeSwaption())
        ch1.append(
            MakeSwaption(
                EuriborSwapIsdaFixA(Period(3, Years), flatYts_),
                Period(2, Years)).makeSwaption())
        ch1.append(
            MakeSwaption(
                EuriborSwapIsdaFixA(Period(2, Years), flatYts_),
                Period(3, Years)).makeSwaption())
        ch1.append(
            MakeSwaption(
                EuriborSwapIsdaFixA(Period(1, Years), flatYts_),
                Period(4, Years)).makeSwaption())

        for i in range(len(ch1)):
            blackEngine = BlackSwaptionEngine(
                flatYts_, calibrationHelperVols1[i])
            ch1[i].setPricingEngine(blackEngine)
            blackPrice = ch1[i].NPV()
            blackVega = ch1[i].resultScalar("vega")
            ch1[i].setPricingEngine(mfSwaptionEngine1)
            mfPrice = ch1[i].NPV()
            self.assertFalse(abs(blackPrice - mfPrice) / blackVega > tol1)

        iborIndex2 = Euribor(Period(6, Months), md0Yts_)

        mf2 = MarkovFunctional(
            md0Yts_, 0.01, volStepDates, vols, md0SwaptionVts_,
            expiriesCalBasket1(), tenorsCalBasket1(), swapIndexBase,
            MarkovFunctionalSettings()
            .withYGridPoints(64)
            .withYStdDevs(7.0)
            .withGaussHermitePoints(32)
            .withDigitalGap(1e-5)
            .withMarketRateAccuracy(1e-7)
            .withLowerRateBound(0.0)
            .withUpperRateBound(2.0)
            .withSmileMoneynessCheckpoints(money))

        calibrationHelper2 = []
        calibrationHelperVols2 = []
        calibrationHelperVols2.append(md0SwaptionVts_.volatility(
            Period(1, Years), Period(4, Years),
            as_swaption_volatility_cube(
                md0SwaptionVts_.currentLink()).atmStrike(Period(1, Years), Period(4, Years))))
        calibrationHelperVols2.append(md0SwaptionVts_.volatility(
            Period(2, Years), Period(3, Years),
            as_swaption_volatility_cube(
                md0SwaptionVts_.currentLink()).atmStrike(Period(2, Years), Period(3, Years))))
        calibrationHelperVols2.append(md0SwaptionVts_.volatility(
            Period(3, Years), Period(2, Years),
            as_swaption_volatility_cube(
                md0SwaptionVts_.currentLink()).atmStrike(Period(3, Years), Period(2, Years))))
        calibrationHelperVols2.append(md0SwaptionVts_.volatility(
            Period(4, Years), Period(1, Years),
            as_swaption_volatility_cube(
                md0SwaptionVts_.currentLink()).atmStrike(Period(4, Years), Period(1, Years))))

        calibrationHelper2.append(
            SwaptionHelper(
                Period(1, Years), Period(4, Years),
                QuoteHandle(
                    SimpleQuote(calibrationHelperVols2[0])),
                iborIndex2, Period(1, Years), Thirty360(Thirty360.BondBasis), Actual360(),
                md0Yts_))
        calibrationHelper2.append(
            SwaptionHelper(
                Period(2, Years), Period(3, Years),
                QuoteHandle(
                    SimpleQuote(calibrationHelperVols2[1])),
                iborIndex2, Period(1, Years), Thirty360(Thirty360.BondBasis), Actual360(),
                md0Yts_))
        calibrationHelper2.append(
            SwaptionHelper(
                Period(3, Years), Period(2, Years),
                QuoteHandle(
                    SimpleQuote(calibrationHelperVols2[2])),
                iborIndex2, Period(1, Years), Thirty360(Thirty360.BondBasis), Actual360(),
                md0Yts_))
        calibrationHelper2.append(
            SwaptionHelper(
                Period(4, Years), Period(1, Years),
                QuoteHandle(
                    SimpleQuote(calibrationHelperVols2[3])),
                iborIndex2, Period(1, Years), Thirty360(Thirty360.BondBasis), Actual360(),
                md0Yts_))

        mfSwaptionEngine2 = Gaussian1dSwaptionEngine(mf2, 64, 7.0)
        calibrationHelper2[0].setPricingEngine(mfSwaptionEngine2)
        calibrationHelper2[1].setPricingEngine(mfSwaptionEngine2)
        calibrationHelper2[2].setPricingEngine(mfSwaptionEngine2)
        calibrationHelper2[3].setPricingEngine(mfSwaptionEngine2)

        mf2.calibrate(calibrationHelper2, om, ec)

        ch2 = []
        ch2.append(MakeSwaption(
            EuriborSwapIsdaFixA(Period(4, Years), md0Yts_),
            Period(1, Years)).makeSwaption())
        ch2.append(MakeSwaption(
            EuriborSwapIsdaFixA(Period(3, Years), md0Yts_),
            Period(2, Years)).makeSwaption())
        ch2.append(MakeSwaption(
            EuriborSwapIsdaFixA(Period(2, Years), md0Yts_),
            Period(3, Years)).makeSwaption())
        ch2.append(MakeSwaption(
            EuriborSwapIsdaFixA(Period(1, Years), md0Yts_),
            Period(4, Years)).makeSwaption())

        for i in range(len(ch2)):
            blackEngine = BlackSwaptionEngine(md0Yts_, calibrationHelperVols2[i])
            ch2[i].setPricingEngine(blackEngine)
            blackPrice = ch2[i].NPV()
            blackVega = ch2[i].resultScalar("vega")
            ch2[i].setPricingEngine(mfSwaptionEngine2)
            mfPrice = ch2[i].NPV()
            self.assertFalse(abs(blackPrice - mfPrice) / blackVega > tol1)

        Settings.instance().evaluationDate = savedEvalDate

    def testBermudanSwaption(self):

        tol0 = 0.0001

        TEST_MESSAGE(
            "Testing Markov functional Bermudan swaption engine...")

        savedEvalDate = Settings.instance().evaluationDate
        referenceDate = Date(14, November, 2012)
        Settings.instance().evaluationDate = referenceDate

        flatYts_ = flatYts()
        md0Yts_ = md0Yts()
        flatSwaptionVts_ = flatSwaptionVts()
        md0SwaptionVts_ = md0SwaptionVts()
        flatOptionletVts_ = flatOptionletVts()
        md0OptionletVts_ = md0OptionletVts()

        swapIndexBase = EuriborSwapIsdaFixA(Period(1, Years))

        volStepDates = DateVector()
        vols = [1.0]

        iborIndex1 = Euribor(Period(6, Months), md0Yts_)

        mf1 = MarkovFunctional(
            md0Yts_, 0.01, volStepDates, vols, md0SwaptionVts_,
            expiriesCalBasket3(), tenorsCalBasket3(),
            swapIndexBase, MarkovFunctionalSettings()
            .withYGridPoints(32)
            .withYStdDevs(7.0)
            .withGaussHermitePoints(16)
            .withMarketRateAccuracy(1e-7)
            .withDigitalGap(1e-5)
            .withLowerRateBound(0.0)
            .withUpperRateBound(2.0))

        mfSwaptionEngine1 = Gaussian1dSwaptionEngine(mf1, 64, 7.0)

        underlyingCall = MakeVanillaSwap(Period(10, Years), iborIndex1, 0.03)
        underlyingCall.withEffectiveDate(TARGET().advance(referenceDate, 2, Days))

        underlyingCall.receiveFixed(false)
        underlyingCall = underlyingCall.makeVanillaSwap()

        europeanExercises = []
        expiries = expiriesCalBasket3()
        europeanSwaptions = []
        for i in range(len(expiries)):
            europeanExercises.append(
                EuropeanExercise(expiries[i]))
            europeanSwaptions.append(Swaption(underlyingCall, europeanExercises[i]))
            europeanSwaptions[-1].setPricingEngine(mfSwaptionEngine1)

        bermudanExercise = BermudanExercise(expiries)
        bermudanSwaption = Swaption(underlyingCall, bermudanExercise)
        bermudanSwaption.setPricingEngine(mfSwaptionEngine1)

        cachedValues = [
            0.0030757, 0.0107344, 0.0179862,
            0.0225881, 0.0243215, 0.0229148,
            0.0191415, 0.0139035, 0.0076354]
        cachedValue = 0.0327776

        for i in range(len(expiries)):
            npv = europeanSwaptions[i].NPV()
            self.assertFalse(abs(npv - cachedValues[i]) > tol0)

        npv = bermudanSwaption.NPV()
        self.assertFalse(abs(npv - cachedValue) > tol0)

        Settings.instance().evaluationDate = savedEvalDate
