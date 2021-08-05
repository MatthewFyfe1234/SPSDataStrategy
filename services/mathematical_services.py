import math


class MathematicalServices:
    @staticmethod
    def mean(val_set):
        tot = 0
        for val in val_set:
            tot += float(val)
        return tot/len(val_set)

    @staticmethod
    def sqr(val):
        return val * val

    @staticmethod
    def variance(val_set):
        mean_ = MathematicalServices.mean(val_set)
        var_sum = 0
        for val in val_set:
            var_sum += MathematicalServices.sqr(val - mean_)
        return var_sum/len(val_set)

    @staticmethod
    def std_dev(val_set):
        return math.sqrt(MathematicalServices.variance(val_set))

    @staticmethod
    def coeff_of_std_deviation(val_set):
        return MathematicalServices.std_dev(val_set)/MathematicalServices.mean(val_set)
