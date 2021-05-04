import random

from genalg.common import BitArr, update_eval

from .base import BaseIndividual


class ClassicIndividual(BaseIndividual):
    """
    Parameters:
        - bit_arr: namedtuple('BitArr', ['bits', 'params'])
            bits: list(int)
            params: list(Parameter)
    """
    def __init__(self, bit_arr, eval_func, **kwargs):
        super().__init__(bit_arr, eval_func, **kwargs)

    @update_eval
    def mutate(self):
        bit_index = random.randrange(0, self.length, 1)
        self.bit_arr.bits[bit_index] = abs(self.bit_arr.bits[bit_index] - 1)
        return self

    @update_eval
    def cross(self, other):
        first = self.copy()
        second = other.copy()
        bit_index = random.randrange(0, self.length, 1)
        first.bit_arr = BitArr(first.bit_arr.bits[:bit_index] + second.bit_arr.bits[bit_index:], self.bit_arr.params)
        second.bit_arr = BitArr(second.bit_arr.bits[:bit_index] + first.bit_arr.bits[bit_index:], self.bit_arr.params)
        # self.bit_arr.bits = other.bit_arr.bits[:bit_index] + self.bit_arr.bits[bit_index:]
        return [first, second]
