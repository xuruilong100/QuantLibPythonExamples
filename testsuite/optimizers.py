import unittest
from math import sqrt, floor, cos

from QuantLib import *

from utilities import *


class CommonVars(object):

    def __init__(self):
        self.costFunctions_ = []
        self.constraints_ = []
        self.initialValues_ = []
        self.maxIterations_ = []
        self.maxStationaryStateIterations_ = []
        self.rootEpsilons_ = DoubleVector()
        self.functionEpsilons_ = DoubleVector()
        self.gradientNormEpsilons_ = DoubleVector()
        self.endCriterias_ = []
        self.optimizationMethods_ = []
        self.xMinExpected_ = []
        self.yMinExpected_ = []

    def setup(self):
        a = 1
        b = 1
        c = 1
        coefficients = Array(3)
        coefficients[0] = c
        coefficients[1] = b
        coefficients[2] = a
        self.costFunctions_.append(
            CustomCostFunction(OneDimensionalPolynomialDegreeN(coefficients)))

        self.constraints_.append(NoConstraint())

        initialValue = Array(1)
        initialValue[0] = -100
        self.initialValues_.append(initialValue)

        self.maxIterations_.append(10000)
        self.maxStationaryStateIterations_.append(100)
        self.rootEpsilons_.append(1e-8)
        self.functionEpsilons_.append(1e-8)
        self.gradientNormEpsilons_.append(1e-8)
        self.endCriterias_.append(EndCriteria(
            self.maxIterations_[-1], self.maxStationaryStateIterations_[-1],
            self.rootEpsilons_[-1], self.functionEpsilons_[-1],
            self.gradientNormEpsilons_[-1]))

        optimizationMethodTypes = [
            OptimizationMethodType.simplex, OptimizationMethodType.levenbergMarquardt,
            OptimizationMethodType.levenbergMarquardt2, OptimizationMethodType.conjugateGradient,
            OptimizationMethodType.bfgs]
        simplexLambda = 0.1
        levenbergMarquardtEpsfcn = 1.0e-8
        levenbergMarquardtXtol = 1.0e-8
        levenbergMarquardtGtol = 1.0e-8
        self.optimizationMethods_.append(
            makeOptimizationMethods(
                optimizationMethodTypes,
                simplexLambda, levenbergMarquardtEpsfcn, levenbergMarquardtXtol,
                levenbergMarquardtGtol))

        xMinExpected = Array(1)
        yMinExpected = Array(1)
        xMinExpected[0] = -b / (2.0 * a)
        yMinExpected[0] = -(b * b - 4.0 * a * c) / (4.0 * a)
        self.xMinExpected_.append(xMinExpected)
        self.yMinExpected_.append(yMinExpected)


class OneDimensionalPolynomialDegreeN(object):

    def __init__(self, coefficients):
        self.coefficients_ = coefficients
        self.polynomialDegree_ = len(coefficients) - 1

    def value(self, x):
        y = 0
        for i in range(0, self.polynomialDegree_ + 1):
            y += self.coefficients_[i] * pow(x[0], int(i))
        return y

    def values(self, x):
        y = Array(1)
        y[0] = self.value(x)
        return y


class OptimizationBasedCostFunction(object):
    def __init__(self):
        pass

    def value(self, x):
        return 1.0

    def values(self, x):
        coefficients = DoubleVector(3, 1.0)
        oneDimensionalPolynomialDegreeN = CustomCostFunction(
            OneDimensionalPolynomialDegreeN(coefficients))
        constraint = NoConstraint()
        initialValues = Array(1, 100.0)
        problem = Problem(
            oneDimensionalPolynomialDegreeN, constraint,
            initialValues)
        optimizationMethod = LevenbergMarquardt()

        endCriteria = EndCriteria(1000, 100, 1e-5, 1e-5, 1e-5)
        optimizationMethod.minimize(problem, endCriteria)

        dummy = Array(1, 0)
        return dummy


class OptimizationMethodType(object):
    simplex = 1
    levenbergMarquardt = 2
    levenbergMarquardt2 = 3
    conjugateGradient = 4
    conjugateGradient_goldstein = 5
    steepestDescent = 6
    steepestDescent_goldstein = 7
    bfgs = 8
    bfgs_goldstein = 9

    def __init__(self):
        pass


def optimizationMethodTypeToString(type):
    if type == OptimizationMethodType.simplex:
        return "Simplex"
    if type == OptimizationMethodType.levenbergMarquardt:
        return "Levenberg Marquardt"
    if type == OptimizationMethodType.levenbergMarquardt2:
        return "Levenberg Marquardt (cost function's jacbobian)"
    if type == OptimizationMethodType.conjugateGradient:
        return "Conjugate Gradient"
    if type == OptimizationMethodType.steepestDescent:
        return "Steepest Descent"
    if type == OptimizationMethodType.bfgs:
        return "BFGS"
    if type == OptimizationMethodType.conjugateGradient_goldstein:
        return "Conjugate Gradient (Goldstein line search)"
    if type == OptimizationMethodType.steepestDescent_goldstein:
        return "Steepest Descent (Goldstein line search)"
    if type == OptimizationMethodType.bfgs_goldstein:
        return "BFGS (Goldstein line search)"


class NamedOptimizationMethod(object):
    def __init__(self):
        self.optimizationMethod = None
        self.name = None


def makeOptimizationMethod(optimizationMethodType,
                           simplexLambda,
                           levenbergMarquardtEpsfcn,
                           levenbergMarquardtXtol,
                           levenbergMarquardtGtol):
    if optimizationMethodType == OptimizationMethodType.simplex:
        return Simplex(simplexLambda)
    if optimizationMethodType == OptimizationMethodType.levenbergMarquardt:
        return LevenbergMarquardt(
            levenbergMarquardtEpsfcn,
            levenbergMarquardtXtol,
            levenbergMarquardtGtol)
    if optimizationMethodType == OptimizationMethodType.levenbergMarquardt2:
        return LevenbergMarquardt(
            levenbergMarquardtEpsfcn,
            levenbergMarquardtXtol,
            levenbergMarquardtGtol,
            true)
    if optimizationMethodType == OptimizationMethodType.conjugateGradient:
        return ConjugateGradient()
    if optimizationMethodType == OptimizationMethodType.steepestDescent:
        return SteepestDescent()
    if optimizationMethodType == OptimizationMethodType.bfgs:
        return BFGS()
    if optimizationMethodType == OptimizationMethodType.conjugateGradient_goldstein:
        return ConjugateGradient(GoldsteinLineSearch())
    if optimizationMethodType == OptimizationMethodType.steepestDescent_goldstein:
        return SteepestDescent(GoldsteinLineSearch())
    if optimizationMethodType == OptimizationMethodType.bfgs_goldstein:
        return BFGS(GoldsteinLineSearch())


def makeOptimizationMethods(optimizationMethodTypes,
                            simplexLambda,
                            levenbergMarquardtEpsfcn,
                            levenbergMarquardtXtol,
                            levenbergMarquardtGtol):
    results = []
    for optimizationMethodType in optimizationMethodTypes:
        namedOptimizationMethod = NamedOptimizationMethod()
        namedOptimizationMethod.optimizationMethod = makeOptimizationMethod(
            optimizationMethodType, simplexLambda, levenbergMarquardtEpsfcn,
            levenbergMarquardtXtol, levenbergMarquardtGtol)
        namedOptimizationMethod.name = optimizationMethodTypeToString(
            optimizationMethodType)
        results.append(namedOptimizationMethod)

    return results


def maxDifference(a, b):
    diff = a - b
    maxDiff = 0.0
    for i in diff:
        maxDiff = max(maxDiff, abs(i))
    return maxDiff


class FirstDeJong(object):
    def __init__(self):
        pass

    def values(self, x):
        retVal = Array(len(x), self.value(x))
        return retVal

    def value(self, x):
        return DotProduct(x, x)


class SecondDeJong(object):
    def __init__(self):
        pass

    def values(self, x):
        retVal = Array(len(x), self.value(x))
        return retVal

    def value(self, x):
        return 100.0 * (x[0] * x[0] - x[1]) * (x[0] * x[0] - x[1]) + (1.0 - x[0]) * (1.0 - x[0])


class ModThirdDeJong(object):
    def __init__(self):
        pass

    def values(self, x):
        retVal = Array(len(x), self.value(x))
        return retVal

    def value(self, x):
        fx = 0.0
        for i in x:
            fx += floor(i) * floor(i)

        return fx


class ModFourthDeJong(object):

    def __init__(self):
        self.uniformRng_ = MersenneTwisterUniformRng(4711)

    def values(self, x):
        retVal = Array(len(x), self.value(x))
        return retVal

    def value(self, x):
        fx = 0.0
        for i in range(len(x)):
            fx += (i + 1.0) * pow(x[i], 4.0) + self.uniformRng_.nextReal()

        return fx


class Griewangk(object):
    def __init__(self):
        pass

    def values(self, x):
        retVal = Array(len(x), self.value(x))
        return retVal

    def value(self, x):
        fx = 0.0
        for i in x:
            fx += i * i / 4000.0

        p = 1.0
        for i in range(len(x)):
            p *= cos(x[i] / sqrt(i + 1.0))

        return fx - p + 1.0


class OptimizersTest(unittest.TestCase):

    @unittest.skip("test")
    def test(self):
        TEST_MESSAGE(
            "Testing optimizers...")
        var = CommonVars()
        var.setup()

        for i in range(len(var.costFunctions_)):
            problem = Problem(
                var.costFunctions_[i],
                var.constraints_[i],
                var.initialValues_[i])
            initialValues = problem.currentValue()

            for j in range(len(var.optimizationMethods_[i])):
                rootEpsilon = var.endCriterias_[i].rootEpsilon()
                endCriteriaTests = 1

                for k in range(endCriteriaTests):
                    problem.setCurrentValue(initialValues)
                    endCriteria = EndCriteria(
                        var.endCriterias_[i].maxIterations(),
                        var.endCriterias_[i].maxStationaryStateIterations(),
                        rootEpsilon,
                        var.endCriterias_[i].functionEpsilon(),
                        var.endCriterias_[i].gradientNormEpsilon())
                    rootEpsilon *= .1
                    endCriteriaResult = var.optimizationMethods_[i][j].optimizationMethod.minimize(
                        problem, endCriteria)
                    xMinCalculated = problem.currentValue()
                    yMinCalculated = problem.values(xMinCalculated)

                    if endCriteriaResult == EndCriteria.NoCriteria or \
                            endCriteriaResult == EndCriteria.MaxIterations or \
                            endCriteriaResult == EndCriteria.Unknown:
                        completed = false
                    else:
                        completed = true

                    xError = maxDifference(xMinCalculated, var.xMinExpected_[i])
                    yError = maxDifference(yMinCalculated, var.yMinExpected_[i])

                    correct = (xError <= endCriteria.rootEpsilon() or
                               yError <= endCriteria.functionEpsilon())

                    if not completed or not correct:
                        print(
                            "costFunction",
                            "\nOptimizer: ", var.optimizationMethods_[i][j].name,
                            "\n    function evaluations: ", problem.functionEvaluation(),
                            "\n    gradient evaluations: ", problem.gradientEvaluation(),
                            "\n    x expected:           ", var.xMinExpected_[i],
                            "\n    x calculated:         ", xMinCalculated,
                            "\n    x difference:         ", var.xMinExpected_[i] - xMinCalculated,
                            "\n    rootEpsilon:          ", endCriteria.rootEpsilon(),
                            "\n    y expected:           ", var.yMinExpected_[i],
                            "\n    y calculated:         ", yMinCalculated,
                            "\n    y difference:         ", var.yMinExpected_[i] - yMinCalculated,
                            "\n    functionEpsilon:      ", endCriteria.functionEpsilon(),
                            "\n    endCriteriaResult:    ", endCriteriaResult)

    def testNestedOptimizationTest(self):
        TEST_MESSAGE(
            "Testing nested optimizations...")
        optimizationBasedCostFunction = CustomCostFunction(OptimizationBasedCostFunction())
        constraint = NoConstraint()
        initialValues = Array(1, 0.0)
        problem = Problem(optimizationBasedCostFunction, constraint,
                          initialValues)
        optimizationMethod = LevenbergMarquardt()

        endCriteria = EndCriteria(1000, 100, 1e-5, 1e-5, 1e-5)
        optimizationMethod.minimize(problem, endCriteria)

    def testDifferentialEvolution(self):
        TEST_MESSAGE(
            "Testing differential evolution...")

        conf = DifferentialEvolutionConfiguration()
        conf.withStepsizeWeight(0.4)
        conf.withBounds()
        conf.withCrossoverProbability(0.35)
        conf.withPopulationMembers(500)
        conf.withStrategy(DifferentialEvolution.BestMemberWithJitter)
        conf.withCrossoverType(DifferentialEvolution.Normal)
        conf.withAdaptiveCrossover()
        conf.withSeed(3242)
        deOptim = DifferentialEvolution(conf)

        conf2 = DifferentialEvolutionConfiguration()
        conf2.withStepsizeWeight(1.8)
        conf2.withBounds()
        conf2.withCrossoverProbability(0.9)
        conf2.withPopulationMembers(1000)
        conf2.withStrategy(DifferentialEvolution.Rand1SelfadaptiveWithRotation)
        conf2.withCrossoverType(DifferentialEvolution.Normal)
        conf2.withAdaptiveCrossover()
        conf2.withSeed(3242)
        deOptim2 = DifferentialEvolution(conf2)

        diffEvolOptimisers = [
            deOptim,
            deOptim,
            deOptim,
            deOptim,
            deOptim2]

        costFunctions = [
            CustomCostFunction(FirstDeJong()),
            CustomCostFunction(SecondDeJong()),
            CustomCostFunction(ModThirdDeJong()),
            CustomCostFunction(ModFourthDeJong()),
            CustomCostFunction(Griewangk())]

        constraints = [
            BoundaryConstraint(-10.0, 10.0),
            BoundaryConstraint(-10.0, 10.0),
            BoundaryConstraint(-10.0, 10.0),
            BoundaryConstraint(-10.0, 10.0),
            BoundaryConstraint(-600.0, 600.0)]

        initialValues = [
            Array(3, 5.0),
            Array(2, 5.0),
            Array(5, 5.0),
            Array(30, 5.0),
            Array(10, 100.0)]

        endCriteria = [
            EndCriteria(100, 10, 1e-10, 1e-8, NullReal()),
            EndCriteria(100, 10, 1e-10, 1e-8, NullReal()),
            EndCriteria(100, 10, 1e-10, 1e-8, NullReal()),
            EndCriteria(500, 100, 1e-10, 1e-8, NullReal()),
            EndCriteria(1000, 800, 1e-12, 1e-10, NullReal())]

        minima = [
            0.0,
            0.0,
            0.0,
            10.9639796558,
            0.0]

        for i in range(len(costFunctions)):
            problem = Problem(
                costFunctions[i],
                constraints[i],
                initialValues[i])

            diffEvolOptimisers[i].minimize(problem, endCriteria[i])
            if i != 3:
                self.assertFalse(abs(problem.functionValue() - minima[i]) > 1e-8)
            else:
                self.assertFalse(problem.functionValue() > 15)
