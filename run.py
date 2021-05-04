import time
import math
import numpy as np

from genalg import GeneticSolver, Parameter
from genalg.models import ClassicModel, ExpectedPriceModel, TreeRegressionModel
from genalg.generations import ClassicGeneration, ExpectedPriceGeneration, TreeRegressionGeneration
from genalg.common import Variable, Function, print_tree


def default_func(M):
    return abs(abs(M[0]) + math.sin(M[1]) - 0.5) + abs(M[0]**2 + M[1]**2 - 1)
    # return math.sin(10*M[0]) + M[0] * math.cos(2*math.pi*M[1])
    # return M[0]**2 - 3
    return M[0] * math.sin(10 * math.pi * M[0]) + 1


# елітарна модель, модель очікуваної вартості та лінійне масштабування
# для різних значень p_el, k


# алгоритм резервуару, елітар, турнір
#

def classic_main():
    step = 1e-6

    x1 = Parameter(-2, 2, step)
    x2 = Parameter(-1, 0, step)

    opts2 = ClassicModel(
        params=[x1, x2],
        eval_func=default_func,
        generation_class=ClassicGeneration,
        num_population=80,
        num_tourn=4,
        chance_mutation=0.35,
        chance_crossing=0.75,
        max_populations=400,
        max_no_change=100
    )

    opts = ClassicModel(
        params=[x1, x2],
        eval_func=default_func,
        generation_class=ClassicGeneration,
        num_population=80,
        num_tourn=4,
        chance_mutation=[0.35, 0.25, 0.6],
        chance_crossing=[0.75, 0.8, 0.85, 0.65],
        max_populations=400,
        max_no_change=100
    )

    opts_e = ExpectedPriceModel(
        params=[x1, x2],
        eval_func=default_func,
        generation_class=ExpectedPriceGeneration,
        num_population=80,
        num_tourn=2,
        chance_mutation=0.15,
        chance_crossing=0.75,
        max_populations=400,
        max_no_change=100,
        elite_percents=0.15,
        kappa=0.7
    )

    mm = GeneticSolver(opts_e)
    start = time.time()
    b = mm.run()
    print('elapsed total: {}'.format(time.time() - start))
    # print(b)
    print(b[0].best_of_all)
    # print(b[1].best_of_all)
    # print(len(b[1].bit_arr.bits))
    mm.plot()
    # print(mm.__dict__)


def tree_main():
    funcs = []
    funcs.append(Function(2, 'plus', lambda x, y: x+y))
    funcs.append(Function(2, 'minus', lambda x, y: x-y))
    funcs.append(Function(2, 'mult', lambda x, y: x*y))
    funcs.append(Function(2, 'div', lambda x, y: 1 if y == 0 else x/y))
    # funcs.append(Function(2, 'pow', lambda x, y: 0 if x == 0 else pow(x, y)))
    funcs.append(Function(1, 'abs', abs))

    x1 = Variable('x1', 0)
    x2 = Variable('x2', 1)

    poss = {
        'funcs': funcs,
        'vars': [x1]*4,
        'consts': list(range(-2, 5, 1))
    }

    exact_func = lambda x: (x+2)**2 - 2

    x = list(np.arange(0, 2, 0.2))
    y = list(map(exact_func, x))

    opts = TreeRegressionModel(
        generation_class=TreeRegressionGeneration,
        possibilities=poss,
        values=x,
        exacts=y,
        min_height=3,
        max_height=7,
        num_population=40,
        num_tourn=3,
        chance_mutation=0.7,
        chance_crossing=0.3,
        elite_percents=0.05,
        max_populations=400,
        max_no_change=70,
    )
    solver = GeneticSolver(opts)
    start = time.time()
    b = solver.run()
    print('elapsed total: {}'.format(time.time() - start))
    # print(b)
    print_tree(b[0].best_of_all[1].tree)
    # print(b[1].best_of_all)
    # print(len(b[1].bit_arr.bits))
    solver.plot()

if __name__ == "__main__":
    # classic_main()
    tree_main()