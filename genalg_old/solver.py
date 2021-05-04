import matplotlib.pyplot as plt
from collections import namedtuple

from genalg_old.population import Population

class GeneticSolver:
    """
    kwargs: 
        bool: multiple_solutions - find multiple solutions (False by default)
        int: solutions_number - solutions number if multiple_solutions == True 
    """
    def __init__(self,
                 params,
                 eval_func,
                 num_population=100,
                 num_tourn=3,
                 chance_mutation=0.1,
                 chance_crossing=0.8,
                 max_populations=100,
                 max_no_change=10,
                 **kwargs):
        self.params = params
        self.eval_func = eval_func
        self.num_population = num_population
        self.num_tourn = num_tourn
        self.chance_mutation = chance_mutation
        self.chance_crossing = chance_crossing
        self.max_populations = max_populations
        self.max_no_change = max_no_change
        self.populations = []
        self.multiple_solutions = True if kwargs.get('multiple_solutions', False) else False
        self.solutions_number = kwargs.get(solutions_number, 1) if self.multiple_solutions else 1

    def run(self):
        no_change = 0
        best_of_all = None
        for i in range(self.max_populations):
            if i == 0:
                self.populations.append(Population(**self.__dict__))
                #best_of_all = self.populations[i].best_individual
                continue
            self.populations.append(Population(previous_population=self.populations[i - 1], **self.__dict__))
            # print(str(i) + str(self.populations[i].best_individual))
            if self.populations[i - 1].best_individual <= self.populations[i].best_individual:
                no_change += 1
            else:
                if not best_of_all or best_of_all[1] > self.populations[i].best_individual:
                    best_of_all = (i, self.populations[i].best_individual)
                # elif best_of_all[1] < 
                # best_of_all = self.populations[i].best_individual
                no_change = 0
            if no_change > self.max_no_change:
                break
        self.best_of_all = best_of_all
        return best_of_all

    def plot(self):
        if not self.best_of_all:
            raise ValueError("Nothing to plot, execute run() first.")
        plt.plot(list(range(len(self.populations))), list(map(lambda x: x.best_individual.eval_value, self.populations)))
        plt.plot(self.best_of_all[0], self.best_of_all[1].eval_value, color='red', marker='o')
        plt.show()
