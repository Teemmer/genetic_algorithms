from genalg.individuals import ClassicIndividual


class ExpectedPriceIndividual(ClassicIndividual):
    def __init__(self, bit_arr, eval_func, **kwargs):
        super().__init__(bit_arr, eval_func, **kwargs)
        self.boosted_eval = self.eval_value

    def __lt__(self, other):
        return self.boosted_eval < other.boosted_eval

    def __gt__(self, other):
        return self.boosted_eval > other.boosted_eval

    def __le__(self, other):
        return self.boosted_eval <= other.boosted_eval

    def __eq__(self, other):
        return abs(self.boosted_eval - other.boosted_eval) < 1e-7

    def __repr__(self):
        return "{}(bits:{}, eval_value: {}, boosted_eval:{} M: {})".format(
            self.__class__.__name__, self.bit_arr.bits, self.eval_value, self.boosted_eval, self.M)