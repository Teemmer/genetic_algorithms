import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import namedtuple

#from genalg.population import Population


class OptionsBuilder:

    def __init__(self, cls, opt_class):
        cls.__dict__.update(opt_class.__dict__)


PopInfo = namedtuple('PopInfo', ['params', 'best_individuals', 'best_of_all'])


class GeneticSolver:
    """
    kwargs: 
        bool: multiple_solutions - find multiple solutions (False by default)
        int: solutions_number - solutions number if multiple_solutions == True 
    """
    def __init__(self, options, num_runs=1):
        OptionsBuilder(self, options)
        self.first_gen = self.generation_class(**self.__dict__)
        self.num_runs = num_runs
        self.iterables = {}
        self.iter_counter = 0
        for arg, value in self.__dict__.items():
            if isinstance(value, (tuple, list)) and arg not in ('params', 'iterables', 'exacts', 'values'):
                self.iter_counter += 1
                self.iterables[arg] = value

        if self.iter_counter > 2:
            raise ValueError("Solver accepts no more than 2 iterable parameters, got {}: {}".format(
                self.iter_counter, ', '.join(self.iterables.keys())
            ))

        self.populations = []

    def _run(self, par_dict, first_gen=None):
        start = time.time()
        try:
            max_populations = par_dict['max_populations']
            max_no_change = par_dict['max_no_change']
        except KeyError:
            raise KeyError('No max_populations or max_no_change specified.')
        generations = []
        no_change = 0
        best_of_all = None
        print("i'm here")
        for i in range(max_populations):
            if i == 0 and not first_gen:
                generations.append(self.generation_class(**par_dict))
                best_of_all = (i, generations[i].best_individual)
                continue
            elif i == 0 and first_gen:
                generations.append(first_gen)
                best_of_all = (i, generations[i].best_individual)
                continue
            generations.append(
                self.generation_class(previous_generation=generations[i - 1], **par_dict)
            )
            if generations[i - 1].best_individual <= generations[i].best_individual:
                no_change += 1
            else:
                if not best_of_all or best_of_all[1] > generations[i].best_individual:
                    best_of_all = (i, generations[i].best_individual)
                no_change = 0
            if no_change > max_no_change:
                break
        info = PopInfo(par_dict, list(map(lambda x: x.best_individual, generations)), best_of_all)
        self.populations.append(info)
        print('elapsed: {}'.format(time.time() - start))
        return info

    def run(self):
        dicts = []
        if self.iter_counter == 0:
            dicts.append(self.__dict__)
        else:
            params, values = list(self.iterables.keys()), list(self.iterables.values())
            for val1 in values[0]:
                if self.iter_counter == 2:
                    for val2 in values[1]:
                        d = self.__dict__.copy()
                        # del d.iterables
                        # del d.populations
                        d[params[0]] = val1
                        d[params[1]] = val2
                        dicts.append(d)
                else:
                    d = self.__dict__.copy()
                    # del d.iterables
                    # del d.populations
                    d[params[0]] = val1
                    dicts.append(d)
        # print('dicts', dicts)
        res = []
        

        for d in dicts:
            res.append(self._run(d, first_gen=self.first_gen))
        return res


    def plot(self):
        if not self.populations:
            raise ValueError("Nothing to plot, execute run() first.")
        if self.iter_counter == 0:
            pop = self.populations[0]
            plt.plot(list(range(len(pop.best_individuals))), 
                     list(map(lambda x: x.eval_value, pop.best_individuals)))
            plt.plot(pop.best_of_all[0], pop.best_of_all[1].eval_value, color='red', marker='o')
        else:
            rest = self.populations
            params, values = list(self.iterables.keys()), list(self.iterables.values())
            x = len(values[0])
            y = len(values[1]) if self.iter_counter == 2 else 1
            fig, axs = plt.subplots(x, y)
            for i, val1 in enumerate(values[0]):
                if self.iter_counter == 2:
                    for j, val2 in enumerate(values[1]):
                        pop, rest = rest[0], rest[1:]
                        # print(type(pop))
                        # print(range(len(pop.best_individuals)))
                        # print(map(lambda x: x.eval_value, pop.best_individuals))
                        # print(len(list(map(lambda x: x.eval_value, pop.best_individuals))))
                        # try:
                        #     pop.best_of_all[1].boosted_eval
                        #     boosted = True
                        # except AttributeError:
                        #     boosted = False

                        axs[i, j].plot(list(range(len(pop.best_individuals))), 
                                    list(map(lambda x: x.eval_value, pop.best_individuals)))
                        axs[i, j].plot(pop.best_of_all[0], pop.best_of_all[1].eval_value, color='red', marker='o')

                        patches = [mpatches.Patch(label='{}:{}'.format(params[0], val1)),
                                mpatches.Patch(label='{}:{}'.format(params[1], val2)),
                                mpatches.Patch(label='{}:{}'.format('eval', pop.best_of_all[1].eval_value)),
                                ]
                        axs[i, j].legend(handles=patches)
                        # axs[i, j].legend(handles='{}:{}, {}:{}, {}:{}'.format(params[0], val1, 
                        #                                               params[1], val2, 
                        #                                               'eval', pop.best_of_all[1].eval_value).split(','))
                else:
                    d = self.__dict__.copy()
                    # del d.iterables
                    # del d.populations
                    d[params[0]] = val1
                    dicts.append(d)
        plt.show()


