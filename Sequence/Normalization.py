import math
class Normalization:
    def __init__(self):
        self.numerator = 0.5
        self.denominator = 1

    def set_numerator(self, numerator):
        self.numerator = numerator

    def set_denominator(self, denominator):
        self.denominator = denominator

    # arg total_count is the count of the entire 2048 binary seq counts,
    # arg single_count is the count at each binary seq counts.
    def log2func(self, total_count, single_count):
        return math.log2((single_count + self.numerator) / (total_count + self.denominator) * 1000000)

