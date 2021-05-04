import random

from functools import wraps
from collections import namedtuple


BitArr = namedtuple('BitArr', ['bits', 'params'])


def update_value(decorated):
    wraps(decorated)
    def decor(self, *args, **kwargs):
        res = decorated(self, *args, **kwargs)
        self.M = self.M_func()
        self.eval_value = self.eval_func(self.M)
        return res
    return decor


class Individual:
    """
    Parameters:
        - bit_arr: namedtuple('BitArr', ['bits', 'params'])
            bits: list(int)
            params: list(Parameter)
    """
    def __init__(self, bit_arr, eval_func, *args, **kwargs):
        self.bit_arr = bit_arr
        self.length = len(self.bit_arr.bits)
        self.eval_func = eval_func
        self.M = self.M_func()
        self.eval_value = self.eval_func(self.M)

    # @property
    # def M(self):
    #     return self.M_func()

    # @property
    # def eval_value(self):
    #     return self.eval_func(self.M)

    def M_func(self):
        res = []
        bit_arr = self.bit_arr.bits[:]
        for param in self.bit_arr.params:
            p_bits, bit_arr = bit_arr[:param.bits_num], bit_arr[param.bits_num:]
            p_bits.reverse()
            res.append(sum([param.a] + list(map(lambda x: (2**x[0]) * x[1] * param.m_fraq, enumerate(p_bits)))))
        return res

    @update_value
    def mutate(self):
        bit_index = random.randrange(0, self.length, 1)
        self.bit_arr.bits[bit_index] = abs(self.bit_arr.bits[bit_index] - 1)
        return self

    @update_value
    def cross(self, other):
        first = self.copy()
        second = other.copy()
        bit_index = random.randrange(0, self.length, 1)
        first.bit_arr = BitArr(first.bit_arr.bits[:bit_index] + second.bit_arr.bits[bit_index:], self.bit_arr.params)
        second.bit_arr = BitArr(second.bit_arr.bits[:bit_index] + first.bit_arr.bits[bit_index:], self.bit_arr.params)
        # self.bit_arr.bits = other.bit_arr.bits[:bit_index] + self.bit_arr.bits[bit_index:]
        return [first, second]

    def copy(self):
        copied = self.__dict__.copy()
        del copied['bit_arr']
        arr = BitArr(self.bit_arr.bits[:], self.bit_arr.params)
        return Individual(arr, **copied)

    def __lt__(self, other):
        return self.eval_value < other.eval_value

    def __gt__(self, other):
        return self.eval_value > other.eval_value

    def __le__(self, other):
        return self.eval_value <= other.eval_value

    def __eq__(self, other):
        return abs(self.eval_value - other.eval_value) < 1e-7

    def __repr__(self):
        return "Individual(bits:{}, eval_value: {}, M: {})".format(self.bit_arr.bits, self.eval_value, self.M)
