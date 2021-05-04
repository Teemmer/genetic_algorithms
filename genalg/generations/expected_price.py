import random

from genalg.generations import BaseGeneration
from genalg.individuals import ExpectedPriceIndividual
from genalg.common import BitArr

class ExpectedPriceGeneration(BaseGeneration):
    def __init__(self, 
                 params,
                 eval_func,
                 previous_generation=None,
                 num_population=28, 
                 num_tourn=2, 
                 chance_mutation=0.1, 
                 chance_crossing=0.8,
                 elite_percents=0.1,
                 kappa=0.8,
                 **kwargs):
        super().__init__(params, eval_func)
        self.num_population = num_population - 1 if num_population % 2 != 0 else num_population
        self.num_tourn = num_tourn
        self.chance_mutation = chance_mutation
        self.chance_crossing = chance_crossing
        self.elite_percents = elite_percents
        self.kappa = kappa
        self.individuals = self.generate() if not previous_generation else self.get_posterity(previous_generation)
        self.best_individual = min(self.individuals)


    def generate(self):
        res = []
        for i in range(self.num_population):
            ind = BitArr([random.randint(0,1) for i in range(self.bits_lenght)], self.params)
            res.append(ExpectedPriceIndividual(ind, **self.__dict__))
        return res

    def make_pos_eval(self, inds):
        min_eval = min(inds).eval_value
        for ind in inds:
            ind.eval_value += 1 - min_eval
        return inds

    def linear_boost(self, inds):
        min_eval = min(inds).eval_value
        eval_sum = sum(map(lambda x: x.eval_value, inds))
        alpha = ((eval_sum - self.num_population * self.kappa * min_eval) / 
                 (eval_sum - self.num_population * min_eval))
        beta = (self.kappa - alpha) * min_eval
        for ind in inds:
            ind.boosted_eval = alpha * ind.eval_value + beta
        return inds

    def get_posterity(self, prev_pop):
        res = []
        not_elite = []
        prev_inds = [ind.copy() for ind in prev_pop.individuals]
        if any(map(lambda x: x.eval_value <= 0, prev_inds)):
            prev_inds = self.make_pos_eval(prev_inds)

        self.linear_boost(prev_inds)

        avg_eval = sum(map(lambda x: x.boosted_eval, prev_inds)) / self.num_population
        # print('###################')
        for ind in prev_inds:
            ind.i_count = avg_eval / ind.boosted_eval
            # print(ind.i_count)

        
        # elite moved to next generaton
        prev_inds = sorted(prev_inds) 
        elite_num = int(self.num_population * self.elite_percents)
        res.extend(prev_inds[:elite_num])
        prev_inds = prev_inds[elite_num:]

        not_elite_num = self.num_population - len(res)
        while len(not_elite) < not_elite_num:
            while True:
                r = random.randrange(0, len(prev_inds), 1)
                if prev_inds[r].i_count > 0:
                    prev_inds[r].i_count -= 1.5
                    break
                else:
                    del prev_inds[r]
            not_elite.append(prev_inds[r].copy())

        [ind.mutate() for ind in not_elite if random.random() < self.chance_mutation]

        if not_elite_num % 2 != 0:
            res.append(max(not_elite))
            not_elite = not_elite[1:]
            not_elite_num -= 1

        # print(not_elite_num, int(self.num_population * self.elite_percents))

        for i in range(not_elite_num // 2):
            ind_1 = random.randrange(0, not_elite_num, 1)
            ind_2 = random.randrange(0, not_elite_num, 1)
            if random.random() < self.chance_crossing:
                res.extend(not_elite[ind_1].cross(not_elite[ind_2]))
            else:
                res.extend([not_elite[ind_1], not_elite[ind_2]])
        # print(len(res))
        return res



