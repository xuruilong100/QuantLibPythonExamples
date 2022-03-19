import unittest
from utilities import *
from QuantLib import *


class CommonVars(object):

    def __init__(self):
        self.accuracy = 1.0e-6
        self.tolerance = 2.5e-8
        self.optionTenors = PeriodVector()
        self.strikes = DoubleVector()
        self.yieldTermStructure = RelinkableYieldTermStructureHandle()
        self.discountingYTS = RelinkableYieldTermStructureHandle()
        self.forwardingYTS = RelinkableYieldTermStructureHandle()
        self.backup = SavedSettings()

    def setTermStructure(self):

        self.calendar = TARGET()
        self.dayCounter = Actual365Fixed()

        self.flatFwdRate = 0.04
        self.yieldTermStructure = RelinkableYieldTermStructureHandle()
        self.discountingYTS = RelinkableYieldTermStructureHandle()
        self.forwardingYTS = RelinkableYieldTermStructureHandle()
        self.yieldTermStructure.linkTo(
            FlatForward(
                0,
                self.calendar,
                self.flatFwdRate,
                self.dayCounter))

    def setRealTermStructure(self):

        self.calendar = TARGET()
        self.dayCounter = Actual365Fixed()

        datesTmp = [
            42124, 42129, 42143, 42221, 42254, 42282, 42313, 42345,
            42374, 42405, 42465, 42495, 42587, 42681, 42772, 42860, 43227,
            43956, 44321, 44686, 45051, 45418, 45782, 46147, 46512, 47609,
            49436, 51263, 53087, 56739, 60392]

        dates = DateVector()
        # dates.reserve(datesTmp.size())
        for it in datesTmp:
            dates.append(Date(it))

        rates = [
            -0.00292, -0.00292, -0.001441, -0.00117, -0.001204,
            -0.001212, -0.001223, -0.001236, -0.001221, -0.001238,
            -0.001262, -0.00125, -0.001256, -0.001233, -0.00118, -0.001108,
            -0.000619, 0.000833, 0.001617, 0.002414, 0.003183, 0.003883,
            0.004514, 0.005074, 0.005606, 0.006856, 0.00813, 0.008709,
            0.009136, 0.009601, 0.009384]

        self.discountingYTS.linkTo(
            # InterpolatedZeroCurve< Linear > >(
            ZeroCurve(
                dates, rates,
                self.dayCounter, self.calendar))

        datesTmp.clear()
        dates.clear()
        rates.clear()

        datesTmp = [
            42124, 42313, 42436, 42556, 42618, 42800, 42830, 42860,
            43227, 43591, 43956, 44321, 44686, 45051, 45418, 45782, 46147,
            46512, 46878, 47245, 47609, 47973, 48339, 48704, 49069, 49436,
            49800, 50165, 50530, 50895, 51263, 51627, 51991, 52356, 52722,
            53087, 54913, 56739, 60392, 64045]

        for it in datesTmp:
            dates.append(Date(it))

        rates = [
            0.000649, 0.000649, 0.000684, 0.000717, 0.000745, 0.000872,
            0.000905, 0.000954, 0.001532, 0.002319, 0.003147, 0.003949,
            0.004743, 0.00551, 0.006198, 0.006798, 0.007339, 0.007832,
            0.008242, 0.008614, 0.008935, 0.009205, 0.009443, 0.009651,
            0.009818, 0.009952, 0.010054, 0.010146, 0.010206, 0.010266,
            0.010315, 0.010365, 0.010416, 0.010468, 0.010519, 0.010571,
            0.010757, 0.010806, 0.010423, 0.010217
        ]

        self.forwardingYTS.linkTo(
            ZeroCurve(
                dates, rates, self.dayCounter, self.calendar))

    def setFlatTermVolCurve(self):

        self.setTermStructure()

        self.optionTenors = PeriodVector(10)
        for i in range(len(self.optionTenors)):
            self.optionTenors[i] = Period(i + 1, Years)

        flatVol = .18

        curveVHandle = QuoteHandleVector(len(self.optionTenors))
        for i in range(len(self.optionTenors)):
            curveVHandle[i] = QuoteHandle(
                SimpleQuote(flatVol))

        self.flatTermVolCurve = CapFloorTermVolCurveHandle(
            CapFloorTermVolCurve(
                0, self.calendar, Following, self.optionTenors,
                curveVHandle, self.dayCounter))

    def setFlatTermVolSurface(self):

        self.setTermStructure()

        self.optionTenors.resize(10)
        for i in range(len(self.optionTenors)):
            self.optionTenors[i] = Period(i + 1, Years)

        self.strikes = DoubleVector()
        self.strikes.resize(10)
        for j in range(len(self.strikes)):
            self.strikes[j] = (j + 1) / 100.0

        flatVol = .18
        self.termV = Matrix(len(self.optionTenors), len(self.strikes), flatVol)
        self.flatTermVolSurface = CapFloorTermVolSurface(
            0, self.calendar, Following,
            self.optionTenors, self.strikes,
            self.termV, self.dayCounter)

    def setCapFloorTermVolCurve(self):

        self.setTermStructure()

        # atm cap volatility curve
        optionTenors = [
            Period(1, Years),
            Period(18, Months),
            Period(2, Years),
            Period(3, Years),
            Period(4, Years),
            Period(5, Years),
            Period(6, Years),
            Period(7, Years),
            Period(8, Years),
            Period(9, Years),
            Period(10, Years),
            Period(12, Years),
            Period(15, Years),
            Period(20, Years),
            Period(25, Years),
            Period(30, Years)]

        # atm capfloor vols from mkt vol matrix using flat yield curve
        atmTermV = [
            0.090304,
            0.12180,
            0.13077,
            0.14832,
            0.15570,
            0.15816,
            0.15932,
            0.16035,
            0.15951,
            0.15855,
            0.15754,
            0.15459,
            0.15163,
            0.14575,
            0.14175,
            0.13889]
        self.atmTermVolHandle = QuoteHandleVector()

        self.atmTermVolHandle.resize(len(optionTenors))
        for i in range(len(optionTenors)):
            self.atmTermVolHandle[i] = QuoteHandle(
                SimpleQuote(atmTermV[i]))

        self.capFloorVolCurve = CapFloorTermVolCurveHandle(
            CapFloorTermVolCurve(
                0, self.calendar, Following,
                optionTenors, self.atmTermVolHandle,
                self.dayCounter))

    def setCapFloorTermVolSurface(self):

        self.setTermStructure()

        # cap volatility smile matrix
        self.optionTenors = [
            Period(1, Years),
            Period(18, Months),
            Period(2, Years),
            Period(3, Years),
            Period(4, Years),
            Period(5, Years),
            Period(6, Years),
            Period(7, Years),
            Period(8, Years),
            Period(9, Years),
            Period(10, Years),
            Period(12, Years),
            Period(15, Years),
            Period(20, Years),
            Period(25, Years),
            Period(30, Years)]

        self.strikes = [
            0.015,
            0.0175,
            0.02,
            0.0225,
            0.025,
            0.03,
            0.035,
            0.04,
            0.05,
            0.06,
            0.07,
            0.08,
            0.1]

        self.termV = Matrix(len(self.optionTenors), len(self.strikes))
        self.termV[0][0] = 0.287
        self.termV[0][1] = 0.274
        self.termV[0][2] = 0.256
        self.termV[0][3] = 0.245
        self.termV[0][4] = 0.227
        self.termV[0][5] = 0.148
        self.termV[0][6] = 0.096
        self.termV[0][7] = 0.09
        self.termV[0][8] = 0.11
        self.termV[0][9] = 0.139
        self.termV[0][10] = 0.166
        self.termV[0][11] = 0.19
        self.termV[0][12] = 0.214
        self.termV[1][0] = 0.303
        self.termV[1][1] = 0.258
        self.termV[1][2] = 0.22
        self.termV[1][3] = 0.203
        self.termV[1][4] = 0.19
        self.termV[1][5] = 0.153
        self.termV[1][6] = 0.126
        self.termV[1][7] = 0.118
        self.termV[1][8] = 0.147
        self.termV[1][9] = 0.165
        self.termV[1][10] = 0.18
        self.termV[1][11] = 0.192
        self.termV[1][12] = 0.212
        self.termV[2][0] = 0.303
        self.termV[2][1] = 0.257
        self.termV[2][2] = 0.216
        self.termV[2][3] = 0.196
        self.termV[2][4] = 0.182
        self.termV[2][5] = 0.154
        self.termV[2][6] = 0.134
        self.termV[2][7] = 0.127
        self.termV[2][8] = 0.149
        self.termV[2][9] = 0.166
        self.termV[2][10] = 0.18
        self.termV[2][11] = 0.192
        self.termV[2][12] = 0.212
        self.termV[3][0] = 0.305
        self.termV[3][1] = 0.266
        self.termV[3][2] = 0.226
        self.termV[3][3] = 0.203
        self.termV[3][4] = 0.19
        self.termV[3][5] = 0.167
        self.termV[3][6] = 0.151
        self.termV[3][7] = 0.144
        self.termV[3][8] = 0.16
        self.termV[3][9] = 0.172
        self.termV[3][10] = 0.183
        self.termV[3][11] = 0.193
        self.termV[3][12] = 0.209
        self.termV[4][0] = 0.294
        self.termV[4][1] = 0.261
        self.termV[4][2] = 0.216
        self.termV[4][3] = 0.201
        self.termV[4][4] = 0.19
        self.termV[4][5] = 0.171
        self.termV[4][6] = 0.158
        self.termV[4][7] = 0.151
        self.termV[4][8] = 0.163
        self.termV[4][9] = 0.172
        self.termV[4][10] = 0.181
        self.termV[4][11] = 0.188
        self.termV[4][12] = 0.201
        self.termV[5][0] = 0.276
        self.termV[5][1] = 0.248
        self.termV[5][2] = 0.212
        self.termV[5][3] = 0.199
        self.termV[5][4] = 0.189
        self.termV[5][5] = 0.172
        self.termV[5][6] = 0.16
        self.termV[5][7] = 0.155
        self.termV[5][8] = 0.162
        self.termV[5][9] = 0.17
        self.termV[5][10] = 0.177
        self.termV[5][11] = 0.183
        self.termV[5][12] = 0.195
        self.termV[6][0] = 0.26
        self.termV[6][1] = 0.237
        self.termV[6][2] = 0.21
        self.termV[6][3] = 0.198
        self.termV[6][4] = 0.188
        self.termV[6][5] = 0.172
        self.termV[6][6] = 0.161
        self.termV[6][7] = 0.156
        self.termV[6][8] = 0.161
        self.termV[6][9] = 0.167
        self.termV[6][10] = 0.173
        self.termV[6][11] = 0.179
        self.termV[6][12] = 0.19
        self.termV[7][0] = 0.25
        self.termV[7][1] = 0.231
        self.termV[7][2] = 0.208
        self.termV[7][3] = 0.196
        self.termV[7][4] = 0.187
        self.termV[7][5] = 0.172
        self.termV[7][6] = 0.162
        self.termV[7][7] = 0.156
        self.termV[7][8] = 0.16
        self.termV[7][9] = 0.165
        self.termV[7][10] = 0.17
        self.termV[7][11] = 0.175
        self.termV[7][12] = 0.185
        self.termV[8][0] = 0.244
        self.termV[8][1] = 0.226
        self.termV[8][2] = 0.206
        self.termV[8][3] = 0.195
        self.termV[8][4] = 0.186
        self.termV[8][5] = 0.171
        self.termV[8][6] = 0.161
        self.termV[8][7] = 0.156
        self.termV[8][8] = 0.158
        self.termV[8][9] = 0.162
        self.termV[8][10] = 0.166
        self.termV[8][11] = 0.171
        self.termV[8][12] = 0.18
        self.termV[9][0] = 0.239
        self.termV[9][1] = 0.222
        self.termV[9][2] = 0.204
        self.termV[9][3] = 0.193
        self.termV[9][4] = 0.185
        self.termV[9][5] = 0.17
        self.termV[9][6] = 0.16
        self.termV[9][7] = 0.155
        self.termV[9][8] = 0.156
        self.termV[9][9] = 0.159
        self.termV[9][10] = 0.163
        self.termV[9][11] = 0.168
        self.termV[9][12] = 0.177
        self.termV[10][0] = 0.235
        self.termV[10][1] = 0.219
        self.termV[10][2] = 0.202
        self.termV[10][3] = 0.192
        self.termV[10][4] = 0.183
        self.termV[10][5] = 0.169
        self.termV[10][6] = 0.159
        self.termV[10][7] = 0.154
        self.termV[10][8] = 0.154
        self.termV[10][9] = 0.156
        self.termV[10][10] = 0.16
        self.termV[10][11] = 0.164
        self.termV[10][12] = 0.173
        self.termV[11][0] = 0.227
        self.termV[11][1] = 0.212
        self.termV[11][2] = 0.197
        self.termV[11][3] = 0.187
        self.termV[11][4] = 0.179
        self.termV[11][5] = 0.166
        self.termV[11][6] = 0.156
        self.termV[11][7] = 0.151
        self.termV[11][8] = 0.149
        self.termV[11][9] = 0.15
        self.termV[11][10] = 0.153
        self.termV[11][11] = 0.157
        self.termV[11][12] = 0.165
        self.termV[12][0] = 0.22
        self.termV[12][1] = 0.206
        self.termV[12][2] = 0.192
        self.termV[12][3] = 0.183
        self.termV[12][4] = 0.175
        self.termV[12][5] = 0.162
        self.termV[12][6] = 0.153
        self.termV[12][7] = 0.147
        self.termV[12][8] = 0.144
        self.termV[12][9] = 0.144
        self.termV[12][10] = 0.147
        self.termV[12][11] = 0.151
        self.termV[12][12] = 0.158
        self.termV[13][0] = 0.211
        self.termV[13][1] = 0.197
        self.termV[13][2] = 0.185
        self.termV[13][3] = 0.176
        self.termV[13][4] = 0.168
        self.termV[13][5] = 0.156
        self.termV[13][6] = 0.147
        self.termV[13][7] = 0.142
        self.termV[13][8] = 0.138
        self.termV[13][9] = 0.138
        self.termV[13][10] = 0.14
        self.termV[13][11] = 0.144
        self.termV[13][12] = 0.151
        self.termV[14][0] = 0.204
        self.termV[14][1] = 0.192
        self.termV[14][2] = 0.18
        self.termV[14][3] = 0.171
        self.termV[14][4] = 0.164
        self.termV[14][5] = 0.152
        self.termV[14][6] = 0.143
        self.termV[14][7] = 0.138
        self.termV[14][8] = 0.134
        self.termV[14][9] = 0.134
        self.termV[14][10] = 0.137
        self.termV[14][11] = 0.14
        self.termV[14][12] = 0.148
        self.termV[15][0] = 0.2
        self.termV[15][1] = 0.187
        self.termV[15][2] = 0.176
        self.termV[15][3] = 0.167
        self.termV[15][4] = 0.16
        self.termV[15][5] = 0.148
        self.termV[15][6] = 0.14
        self.termV[15][7] = 0.135
        self.termV[15][8] = 0.131
        self.termV[15][9] = 0.132
        self.termV[15][10] = 0.135
        self.termV[15][11] = 0.139
        self.termV[15][12] = 0.146

        self.capFloorVolSurface = CapFloorTermVolSurface(
            0, self.calendar, Following,
            self.optionTenors, self.strikes,
            self.termV, self.dayCounter)

    def setRealCapFloorTermVolSurface(self):

        self.setRealTermStructure()

        # cap volatility smile matrix
        self.optionTenors = [
            Period(1, Years),
            Period(18, Months),
            Period(2, Years),
            Period(3, Years),
            Period(4, Years),
            Period(5, Years),
            Period(6, Years),
            Period(7, Years),
            Period(8, Years),
            Period(9, Years),
            Period(10, Years),
            Period(12, Years),
            Period(15, Years),
            Period(20, Years),
            Period(25, Years),
            Period(30, Years)]
        # 16

        self.strikes = [
            -0.005,
            -0.0025,
            -0.00125,
            0.0,
            0.00125,
            0.0025,
            0.005,
            0.01,
            0.015,
            0.02,
            0.03,
            0.05,
            0.1]
        # 13

        rawVols = [
            0.49, 0.39, 0.34, 0.31, 0.34, 0.37, 0.50, 0.75, 0.99, 1.21, 1.64, 2.44, 4.29,
            0.44, 0.36, 0.33, 0.31, 0.33, 0.35, 0.45, 0.65, 0.83, 1.00, 1.32, 1.93, 3.30,
            0.40, 0.35, 0.33, 0.31, 0.33, 0.34, 0.41, 0.55, 0.69, 0.82, 1.08, 1.56, 2.68,
            0.42, 0.39, 0.38, 0.37, 0.38, 0.39, 0.43, 0.54, 0.64, 0.74, 0.94, 1.31, 2.18,
            0.46, 0.43, 0.42, 0.41, 0.42, 0.43, 0.47, 0.56, 0.66, 0.75, 0.93, 1.28, 2.07,
            0.49, 0.47, 0.46, 0.45, 0.46, 0.47, 0.51, 0.59, 0.68, 0.76, 0.93, 1.25, 1.99,
            0.51, 0.49, 0.49, 0.48, 0.49, 0.50, 0.54, 0.62, 0.70, 0.78, 0.94, 1.24, 1.94,
            0.52, 0.51, 0.51, 0.51, 0.52, 0.53, 0.56, 0.63, 0.71, 0.79, 0.94, 1.23, 1.89,
            0.53, 0.52, 0.52, 0.52, 0.53, 0.54, 0.57, 0.65, 0.72, 0.79, 0.94, 1.21, 1.83,
            0.55, 0.54, 0.54, 0.54, 0.55, 0.56, 0.59, 0.66, 0.72, 0.79, 0.91, 1.15, 1.71,
            0.56, 0.56, 0.56, 0.56, 0.57, 0.58, 0.61, 0.67, 0.72, 0.78, 0.89, 1.09, 1.59,
            0.59, 0.58, 0.58, 0.59, 0.59, 0.60, 0.63, 0.68, 0.73, 0.78, 0.86, 1.03, 1.45,
            0.61, 0.61, 0.61, 0.61, 0.62, 0.62, 0.64, 0.69, 0.73, 0.77, 0.85, 1.02, 1.44,
            0.62, 0.62, 0.63, 0.63, 0.64, 0.64, 0.65, 0.69, 0.72, 0.76, 0.82, 0.96, 1.32,
            0.62, 0.63, 0.63, 0.63, 0.65, 0.66, 0.66, 0.68, 0.72, 0.74, 0.80, 0.93, 1.25,
            0.62, 0.62, 0.62, 0.62, 0.66, 0.67, 0.67, 0.67, 0.72, 0.72, 0.78, 0.90, 1.25]

        self.termV = Matrix(len(self.optionTenors), len(self.strikes))
        # copy(rawVols.begin(), rawVols.end(), termV.begin())
        for i in range(self.termV.rows()):
            for j in range(self.termV.columns()):
                self.termV[i][j] = rawVols[i * len(self.strikes) + j] / 100.0
        # termV /= 100.0

        self.capFloorVolRealSurface = CapFloorTermVolSurface(
            0, self.calendar, Following,
            self.optionTenors, self.strikes, self.termV,
            self.dayCounter)


class OptionletStripperTest(unittest.TestCase):

    def testFlatTermVolatilityStripping1(self):
        TEST_MESSAGE(
            "Testing forward/forward vol stripping from flat term vol "
            "surface using OptionletStripper1 class...")

        vars = CommonVars()
        Settings.instance().evaluationDate = Date(28, October, 2013)

        vars.setFlatTermVolSurface()

        iborIndex = Euribor6M(vars.yieldTermStructure)

        optionletStripper1 = OptionletStripper1(
            vars.flatTermVolSurface,
            iborIndex,
            NullReal(),
            vars.accuracy)

        strippedOptionletAdapter = StrippedOptionletAdapter(optionletStripper1)

        vol = OptionletVolatilityStructureHandle(strippedOptionletAdapter)

        vol.enableExtrapolation()

        strippedVolEngine = BlackCapFloorEngine(
            vars.yieldTermStructure, vol)

        # cap
        for tenorIndex in range(len(vars.optionTenors)):
            for strikeIndex in range(len(vars.strikes)):
                cap = MakeCapFloor(
                    CapFloor.Cap,
                    vars.optionTenors[tenorIndex],
                    iborIndex,
                    vars.strikes[strikeIndex],
                    Period(0, Days))
                cap.withPricingEngine(strippedVolEngine)
                cap = cap.makeCapFloor()

                priceFromStrippedVolatility = cap.NPV()

                blackCapFloorEngineConstantVolatility = BlackCapFloorEngine(
                    vars.yieldTermStructure,
                    vars.termV[tenorIndex][strikeIndex])

                cap.setPricingEngine(blackCapFloorEngineConstantVolatility)
                priceFromConstantVolatility = cap.NPV()

                error = abs(priceFromStrippedVolatility - priceFromConstantVolatility)
                self.assertFalse(error > vars.tolerance)

    def testTermVolatilityStripping1(self):
        TEST_MESSAGE(
            "Testing forward/forward vol stripping from non-flat term "
            "vol surface using OptionletStripper1 class...")

        vars = CommonVars()
        Settings.instance().evaluationDate = Date(28, October, 2013)

        vars.setCapFloorTermVolSurface()

        iborIndex = Euribor6M(vars.yieldTermStructure)

        optionletStripper1 = OptionletStripper1(
            vars.capFloorVolSurface,
            iborIndex,
            NullReal(),
            vars.accuracy)

        strippedOptionletAdapter = StrippedOptionletAdapter(optionletStripper1)

        vol = OptionletVolatilityStructureHandle(strippedOptionletAdapter)

        vol.enableExtrapolation()

        strippedVolEngine = BlackCapFloorEngine(
            vars.yieldTermStructure, vol)

        # cap
        for tenorIndex in range(len(vars.optionTenors)):
            for strikeIndex in range(len(vars.strikes)):
                cap = MakeCapFloor(
                    CapFloor.Cap,
                    vars.optionTenors[tenorIndex],
                    iborIndex,
                    vars.strikes[strikeIndex],
                    Period(0, Days))
                cap.withPricingEngine(strippedVolEngine)
                cap = cap.makeCapFloor()

                priceFromStrippedVolatility = cap.NPV()

                blackCapFloorEngineConstantVolatility = BlackCapFloorEngine(
                    vars.yieldTermStructure,
                    vars.termV[tenorIndex][strikeIndex])

                cap.setPricingEngine(blackCapFloorEngineConstantVolatility)
                priceFromConstantVolatility = cap.NPV()

                error = abs(priceFromStrippedVolatility - priceFromConstantVolatility)
                self.assertFalse(error > vars.tolerance)

    def testTermVolatilityStrippingNormalVol(self):
        TEST_MESSAGE(
            "Testing forward/forward vol stripping from non-flat normal vol term "
            "vol surface for normal vol setup using OptionletStripper1 class...")

        vars = CommonVars()
        Settings.instance().evaluationDate = Date(30, April, 2015)

        vars.setRealCapFloorTermVolSurface()

        iborIndex = Euribor6M(vars.forwardingYTS)

        optionletStripper1 = OptionletStripper1(
            vars.capFloorVolRealSurface, iborIndex,
            NullReal(), vars.accuracy, 100,
            vars.discountingYTS, Normal)

        strippedOptionletAdapter = StrippedOptionletAdapter(
            optionletStripper1)

        vol = OptionletVolatilityStructureHandle(strippedOptionletAdapter)

        vol.enableExtrapolation()

        strippedVolEngine = BachelierCapFloorEngine(vars.discountingYTS, vol)

        # ext.shared_ptr< CapFloor > cap
        for tenorIndex in range(len(vars.optionTenors)):
            for strikeIndex in range(len(vars.strikes)):
                cap = MakeCapFloor(
                    CapFloor.Cap, vars.optionTenors[tenorIndex],
                    iborIndex, vars.strikes[strikeIndex],
                    Period(0, Days))
                cap.withPricingEngine(strippedVolEngine)
                cap = cap.makeCapFloor()

                priceFromStrippedVolatility = cap.NPV()

                bachelierCapFloorEngineConstantVolatility = BachelierCapFloorEngine(
                    vars.discountingYTS,
                    vars.termV[tenorIndex][strikeIndex])

                cap.setPricingEngine(bachelierCapFloorEngineConstantVolatility)
                priceFromConstantVolatility = cap.NPV()

                error = abs(priceFromStrippedVolatility -
                            priceFromConstantVolatility)
                self.assertFalse(error > vars.tolerance)

    def testTermVolatilityStrippingShiftedLogNormalVol(self):
        TEST_MESSAGE(
            "Testing forward/forward vol stripping from non-flat normal vol term "
            "vol surface for normal vol setup using OptionletStripper1 class...")

        vars = CommonVars()
        shift = 0.03
        Settings.instance().evaluationDate = Date(30, April, 2015)

        vars.setRealCapFloorTermVolSurface()

        iborIndex = Euribor6M(vars.forwardingYTS)

        optionletStripper1 = OptionletStripper1(
            vars.capFloorVolRealSurface, iborIndex,
            NullReal(), vars.accuracy, 100,
            vars.discountingYTS, ShiftedLognormal, shift,
            true)

        strippedOptionletAdapter = StrippedOptionletAdapter(
            optionletStripper1)

        vol = OptionletVolatilityStructureHandle(strippedOptionletAdapter)

        vol.enableExtrapolation()

        strippedVolEngine = BlackCapFloorEngine(vars.discountingYTS, vol)

        # ext.shared_ptr< CapFloor > cap
        for strikeIndex in range(len(vars.strikes)):
            for tenorIndex in range(len(vars.optionTenors)):
                cap = MakeCapFloor(
                    CapFloor.Cap, vars.optionTenors[tenorIndex],
                    iborIndex, vars.strikes[strikeIndex],
                    Period(0, Days))
                cap.withPricingEngine(strippedVolEngine)
                cap = cap.makeCapFloor()

                priceFromStrippedVolatility = cap.NPV()

                blackCapFloorEngineConstantVolatility = BlackCapFloorEngine(
                    vars.discountingYTS, vars.termV[tenorIndex][strikeIndex],
                    vars.capFloorVolRealSurface.dayCounter(), shift)

                cap.setPricingEngine(blackCapFloorEngineConstantVolatility)
                priceFromConstantVolatility = cap.NPV()

                error = abs(priceFromStrippedVolatility -
                            priceFromConstantVolatility)
                self.assertFalse(error > vars.tolerance)

    def testFlatTermVolatilityStripping2(self):
        TEST_MESSAGE(
            "Testing forward/forward vol stripping from flat term vol "
            "surface using OptionletStripper2 class...")

        vars = CommonVars()
        Settings.instance().evaluationDate = Date.todaysDate()

        vars.setFlatTermVolCurve()
        vars.setFlatTermVolSurface()

        iborIndex = Euribor6M(vars.yieldTermStructure)

        # optionletstripper1
        optionletStripper1 = OptionletStripper1(
            vars.flatTermVolSurface,
            iborIndex,
            NullReal(),
            vars.accuracy)

        strippedOptionletAdapter1 = StrippedOptionletAdapter(optionletStripper1)

        vol1 = OptionletVolatilityStructureHandle(strippedOptionletAdapter1)

        vol1.enableExtrapolation()

        # optionletstripper2
        optionletStripper2 = OptionletStripper2(optionletStripper1, vars.flatTermVolCurve)

        strippedOptionletAdapter2 = StrippedOptionletAdapter(optionletStripper2)

        vol2 = OptionletVolatilityStructureHandle(strippedOptionletAdapter2)

        vol2.enableExtrapolation()

        # consistency check: diff(stripped vol1-stripped vol2)
        for strikeIndex in range(len(vars.strikes)):
            for tenorIndex in range(len(vars.optionTenors)):
                strippedVol1 = vol1.volatility(
                    vars.optionTenors[tenorIndex],
                    vars.strikes[strikeIndex], true)

                strippedVol2 = vol2.volatility(
                    vars.optionTenors[tenorIndex],
                    vars.strikes[strikeIndex], true)

                # vol from flat vol surface (for comparison only)
                flatVol = vars.flatTermVolSurface.volatility(
                    vars.optionTenors[tenorIndex],
                    vars.strikes[strikeIndex], true)

                error = abs(strippedVol1 - strippedVol2)
                self.assertFalse(error > vars.tolerance)

    def testTermVolatilityStripping2(self):
        TEST_MESSAGE(
            "Testing forward/forward vol stripping from non-flat term vol "
            "surface using OptionletStripper2 class...")

        vars = CommonVars()
        Settings.instance().evaluationDate = Date.todaysDate()

        vars.setCapFloorTermVolCurve()
        vars.setCapFloorTermVolSurface()

        iborIndex = Euribor6M(vars.yieldTermStructure)

        # optionletstripper1
        optionletStripper1 = OptionletStripper1(
            vars.capFloorVolSurface,
            iborIndex,
            NullReal(),
            vars.accuracy)

        strippedOptionletAdapter1 = StrippedOptionletAdapter(optionletStripper1)

        vol1 = OptionletVolatilityStructureHandle(strippedOptionletAdapter1)
        vol1.enableExtrapolation()

        # optionletstripper2
        optionletStripper2 = OptionletStripper2(
            optionletStripper1, vars.capFloorVolCurve)

        strippedOptionletAdapter2 = StrippedOptionletAdapter(optionletStripper2)

        vol2 = OptionletVolatilityStructureHandle(strippedOptionletAdapter2)
        vol2.enableExtrapolation()

        # consistency check: diff(stripped vol1-stripped vol2)
        for strikeIndex in range(len(vars.strikes)):
            for tenorIndex in range(len(vars.optionTenors)):
                strippedVol1 = vol1.volatility(
                    vars.optionTenors[tenorIndex],
                    vars.strikes[strikeIndex], true)

                strippedVol2 = vol2.volatility(
                    vars.optionTenors[tenorIndex],
                    vars.strikes[strikeIndex], true)

                # vol from flat vol surface (for comparison only)
                flatVol = vars.capFloorVolSurface.volatility(
                    vars.optionTenors[tenorIndex],
                    vars.strikes[strikeIndex], true)

                error = abs(strippedVol1 - strippedVol2)
                self.assertFalse(error > vars.tolerance)

    def testSwitchStrike(self):
        TEST_MESSAGE("Testing switch strike level and recalibration of level "
                     "in case of curve relinking...")

        usingAtParCoupons = IborCouponSettings.instance().usingAtParCoupons()

        vars = CommonVars()
        Settings.instance().evaluationDate = Date(28, October, 2013)
        vars.setCapFloorTermVolSurface()

        yieldTermStructure = RelinkableYieldTermStructureHandle()
        yieldTermStructure.linkTo(FlatForward(
            0, vars.calendar, 0.03, vars.dayCounter))

        iborIndex = Euribor6M(yieldTermStructure)

        optionletStripper1 = OptionletStripper1(
            vars.capFloorVolSurface, iborIndex,
            NullReal(), vars.accuracy)

        expected = 0.02981223 if usingAtParCoupons else 0.02981258

        error = abs(optionletStripper1.switchStrike() - expected)
        self.assertFalse(error > vars.tolerance)

        yieldTermStructure.linkTo(FlatForward(
            0, vars.calendar, 0.05, vars.dayCounter))

        expected = 0.0499371 if usingAtParCoupons else 0.0499381

        error = abs(optionletStripper1.switchStrike() - expected)
        self.assertFalse(error > vars.tolerance)
