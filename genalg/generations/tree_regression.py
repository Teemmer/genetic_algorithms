import random
from genalg.individuals import TreeRegressionIndividual

class TreeRegressionGeneration:
    def __init__(self, 
                 possibilities,
                 values,
                 exacts,
                 previous_generation=None,
                 min_height=4,
                 max_height=9,
                 num_population=28, 
                 num_tourn=2, 
                 chance_mutation=0.1, 
                 chance_crossing=0.8,
                 elite_percents=0.15,
                 **kwargs):
        self.possibilities = possibilities
        self.values = values
        self.exacts = exacts
        self.num_population = num_population - 1 if num_population % 2 != 0 else num_population
        self.num_tourn = num_tourn
        self.min_height = min_height
        self.max_height = max_height
        self.chance_mutation = chance_mutation
        self.chance_crossing = chance_crossing
        self.elite_percents = elite_percents
        self.individuals = self.generate() if not previous_generation else self.get_posterity(previous_generation.individuals)
        self.best_individual = min(self.individuals)

    def generate(self):
        res = []
        for i in range(self.num_population):
            res.append(TreeRegressionIndividual(**self.__dict__))
        return res

    def get_posterity(self, prev_pop):
        res = []

        # elite moved to next generaton
        prev_pop = sorted(prev_pop) 
        elite_num = int(self.num_population * self.elite_percents)
        res.extend(prev_pop[:elite_num])
        prev_pop = prev_pop[elite_num:]

        not_elite_num = len(prev_pop)

        winners = [self.tournament(prev_pop, not_elite_num) for t in range(not_elite_num)]
        [ind.mutate() for ind in winners if random.random() < self.chance_mutation]
        # res.extend(winners)

        if not_elite_num % 2 != 0:
            res.append(min(winners))
            winners = winners[1:]
            not_elite_num -= 1

        for i in range(not_elite_num // 2):
            ind_1 = random.randrange(0, not_elite_num, 1)
            ind_2 = random.randrange(0, not_elite_num, 1)
            if random.random() < self.chance_crossing:
                res.extend(winners[ind_1].cross(winners[ind_2]))
            else:
                res.extend([winners[ind_1], winners[ind_2]])
        return res


    def tournament(self, prev_pop, lenght):
        contenders = [prev_pop[random.randint(0, lenght - 1)] for i in range(self.num_tourn)]
        return min(contenders).copy()