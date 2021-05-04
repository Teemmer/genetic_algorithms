class BaseModel:

    def __init__(self,
                 params,
                 eval_func,
                 generation_class,
                 num_population=100,
                 max_populations=400,
                 max_no_change=50):
        self.params = params
        self.eval_func = eval_func
        self.generation_class = generation_class
        self.num_population = num_population
        self.max_populations = max_populations
        self.max_no_change = max_no_change
