import math
import time

from genalg_old import GeneticSolver, Parameter

def default_func(M):
    return abs(abs(M[0]) + math.sin(M[1]) - 0.5) + abs(M[0]**2 + M[1]**2 - 1)
    # return math.sin(10*M[0]) + M[0] * math.cos(2*math.pi*M[1])
    # return M[0]**2 - 3
    return M[0] * math.sin(10 * math.pi * M[0]) + 1

if __name__ == "__main__":
    step = 1e-6

    x1 = Parameter(-2, 2, step)
    x2 = Parameter(-1, 1, step)

    # x2 = Parameter(0,1, step)

    mm = GeneticSolver(
        params=[x1, x2],
        eval_func=default_func,
        num_population=80,
        num_tourn=4,
        chance_mutation=0.35,
        chance_crossing=0.75,
        max_populations=400,
        max_no_change=100
    )

    start = time.time()
    b = mm.run()
    print('elapsed: {}'.format(time.time() - start))
    print(b)
    print(len(b[1].bit_arr.bits))
    mm.plot()
