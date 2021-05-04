from functools import wraps


def update_value(decorated):
    wraps(decorated)
    def decor(self, *args, **kwargs):
        decorated(self, *args, **kwargs)
        self.m = 2
    return decor

class BaseIndividual:
    """
    """

    # class update_value:
    #     def __init__(self, decorated):
    #         self.decorated = decorated

    #     def __call__(self):
    #         wraps(self.decorated)
    #         print(self.decorated)
    #         def func():
    #             self.m = 2
    #         print(func)
    #         return func

    def __init__(self, m):
        self.m = m

    @update_value
    def upd(self, val):
        print('self.m = val')


# b = BaseIndividual(3)
# print(b.m)
# b.upd(3)
# print(b.m)

class BaseOptions:

    def __init__(self,
                 params,
                 eval_func,
                 num_population=100,
                 max_populations=400,
                 max_no_change=50):
        self.params = params
        self.eval_func = eval_func
        self.num_population = num_population
        self.max_populations = max_populations
        self.max_no_change = max_no_change


class ClassicOptions(BaseOptions):

    def __init__(self, num_tourn=3, chance_mutation=0.2, chance_crossing=0.8, **kwargs):
        super().__init__(**kwargs)
        self.num_tourn = num_tourn
        self.chance_mutation = chance_mutation
        self.chance_crossing = chance_crossing
        


class OptionsBuilder:

    def __init__(self, cls, opt_class):
        cls.__dict__.update(opt_class.__dict__)



class Solver:

    def __init__(self, options):
        OptionsBuilder(self, options)


opts = ClassicOptions(params=[1,2], eval_func='func')
opts2 = ClassicOptions(params=[1,2], eval_func='func22', num_tourn=4)

solv = Solver(opts)
solv2 = Solver(opts2)
print(solv.__dict__)
print(solv2.__dict__)
print(type(solv.max_populations))