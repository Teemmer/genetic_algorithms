from typing import Union, Any


class Parameter:
    """
    Parameter properties for evaluation function in genetic algorithm.

    For the next equation:
        x + y = 0,  x∈[-1, 1] and  y∈[0, 2]
    
    Let h = 0.01
    Then x = Parameter(-1, 1, 0.01) and
         y = Parameter(0, 2, 0.01)

    bits_num is calculated as first k that  2**k >= (b-a)/h

    2/0.01 = 200 < 256 = 2**8, therefore bits_num = 8


    Attributes
    __________
    a : (int, float)
        Start of segment, where parameter is defined, a < b.
    b : (int, float)
        End of segment, where parameter is defined, a < b.
    h : (int, float)
        Step of segment fragmentation.
    bits_num : int
        Number of bits, just enough for reflection of segment with selected step
        into bit number.
    m_fraq : float
        Just useful value for M-vector calculations in Individual class, so it's better to calculate it once.
    """

    a: Union[int, float]
    b: Union[int, float]
    h: Union[int, float]
    bits_num: int
    m_fraq: float

    def __init__(self, a, b, h=1e-6) -> None:
        self.a = a
        self.b = b
        self.h = h
        self.bits_num = self.get_num()
        self.m_fraq = (b - a) / ((2 ** self.bits_num) - 1)

    def get_num(self) -> float:
        """
        Calculates bits_num for parameter
        """
        k = 1
        while 2 ** k <= (self.b - self.a) / self.h:
            k += 1
        return k
