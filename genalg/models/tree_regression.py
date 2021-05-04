    
class TreeRegressionModel:
    def __init__(self, 
                 possibilities,
                 values,
                 exacts,
                 generation_class,
                 min_height=4,
                 max_height=9,
                 num_population=28, 
                 num_tourn=2, 
                 chance_mutation=0.1, 
                 chance_crossing=0.8,
                 elite_percents=0.15,
                 max_populations=100,
                 max_no_change=50,
                 **kwargs):
        self.possibilities = possibilities
        self.values = values
        self.exacts = exacts
        self.generation_class = generation_class
        self.num_population = num_population - 1 if num_population % 2 != 0 else num_population
        self.num_tourn = num_tourn
        self.min_height = min_height
        self.max_height = max_height
        self.chance_mutation = chance_mutation
        self.chance_crossing = chance_crossing
        self.max_populations = max_populations
        self.max_no_change = max_no_change