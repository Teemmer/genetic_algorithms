import random

from genalg.individuals import ClassicIndividual
from genalg.generations import BaseGeneration
from genalg.common import Parameter, BitArr


class ClassicGeneration(BaseGeneration):
    def __init__(self, 
                 params,
                 eval_func,
                 previous_generation=None,
                 num_population=28, 
                 num_tourn=2, 
                 chance_mutation=0.1, 
                 chance_crossing=0.8,
                 **kwargs):
        super().__init__(params, eval_func)
        self.num_population = num_population - 1 if num_population % 2 != 0 else num_population
        self.num_tourn = num_tourn
        self.chance_mutation = chance_mutation
        self.chance_crossing = chance_crossing
        self.individuals = self.generate() if not previous_generation else self.get_posterity(previous_generation)
        self.best_individual = min(self.individuals)

    def get_length(self):
        return sum(map(lambda x: x.bits_num, self.params))

    def generate(self):
        res = []
        for i in range(self.num_population):
            ind = BitArr([random.randint(0,1) for i in range(self.bits_lenght)], self.params)
            res.append(ClassicIndividual(ind, **self.__dict__))
        return res

    def get_posterity(self, prev_pop):
        res = []
        winners = [self.tournament(prev_pop) for t in range(self.num_population)]
        [ind.mutate() for ind in winners if random.random() < self.chance_mutation]
        for i in range(self.num_population // 2):
            ind_1 = random.randrange(0, self.num_population, 1)
            ind_2 = random.randrange(0, self.num_population, 1)
            if random.random() < self.chance_crossing:
                res.extend(winners[ind_1].cross(winners[ind_2]))
            else:
                res.extend([winners[ind_1], winners[ind_2]])
        return res
        

    def tournament(self, prev_pop):
        contenders = [prev_pop.individuals[random.randint(0, self.num_population - 1)] for i in range(self.num_tourn)]
        return min(contenders).copy()
