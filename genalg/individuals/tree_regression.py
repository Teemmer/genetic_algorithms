import random
from copy import deepcopy
from functools import wraps

from genalg.individuals import BaseIndividual
# dict keys: vars, consts, funcs


class TreeRegressionIndividual(BaseIndividual):
    def __init__(self, possibilities, values, exacts, min_height, max_height, **kwargs):
        self.possibilities = possibilities
        self.values = values
        self.exacts = exacts
        self.min_height = min_height
        self.max_height = max_height
        self.tree = FuncNode(height=0, **self.__dict__)
        self.eval_value = self.evaluate()

    def copy(self):
        return deepcopy(self)

    def evaluate(self):
        res = 0
        for value, exact in zip(self.values, self.exacts):
            if isinstance(value, (int, float)):
                value = [value]
            res += abs(self.tree(list(value)) - exact)
        return res

    def mutate(self):
        node = self.tree.reservoire()[0]
        node.__dict__.update(type(node)(**node.__dict__).__dict__)
        self.eval_value = self.evaluate()
        return self

    def cross(self, other):
        first = self.copy()
        second = other.copy()
        cross_h = random.randint(1, self.min_height)
        f_node = first.tree.reservoire()[0]
        s_node = second.tree.reservoire()[0]
        while f_node.height != cross_h or type(f_node) != FuncNode:
            f_node = first.tree.reservoire()[0]
        while s_node.height != cross_h or type(s_node) != FuncNode:
            s_node = second.tree.reservoire()[0]
        
        buffer = deepcopy(f_node)
        f_node.__dict__.update(s_node.__dict__)
        s_node.__dict__.update(buffer.__dict__)
        return [first, second]

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.eval_value)

class FuncNode:
    def __init__(self, possibilities, min_height, max_height, height, **kwargs):
        self.height = height
        self.min_height = min_height
        self.max_height = max_height
        self.possibilities = possibilities
        self.childs = []
        one_child = True
        self.func = random.choice(possibilities['funcs'])
        is_l_son_terminal = random.random() < 0.5
        if self.func.num_childs != 1:
            one_child = False
            is_r_son_terminal = random.random() < 0.5

        if one_child:
            if height < min_height:
                self.childs.append(FuncNode(possibilities, min_height, max_height, height + 1))
            elif height >= max_height - 1:
                self.childs.append(TerminalNode(possibilities, min_height, max_height, height + 1))
            else:
                self.childs.append(TerminalNode(possibilities, min_height, max_height, height + 1) if 
                    is_l_son_terminal else FuncNode(possibilities, min_height, max_height, height + 1))
        else:
            if height >= max_height - 1:
                [self.childs.append(TerminalNode(possibilities, min_height, max_height, height + 1)) 
                    for i in range(2)]
            # can't add two terminal sons while tree height < min_height
            elif is_l_son_terminal and is_r_son_terminal and min_height > height:
                self.childs.append(TerminalNode(possibilities, min_height, max_height, height + 1))
                self.childs.append(FuncNode(possibilities, min_height, max_height, height + 1))
            else:
                self.childs.append(TerminalNode(possibilities, min_height, max_height, height + 1) if 
                    is_l_son_terminal else FuncNode(possibilities, min_height, max_height, height + 1))
                self.childs.append(TerminalNode(possibilities, min_height, max_height, height + 1) if 
                    is_r_son_terminal else FuncNode(possibilities, min_height, max_height, height + 1))

    def reservoire(self, selected=None, i=1):
        for child in self.childs:
            selected, i = child.reservoire(selected, i+1)
        if random.random() < 1/i:
            selected = self
        
        return selected, i

    def __call__(self, value):
        res = [child(value) for child in self.childs]
        return self.func.func(*res)

    def __repr__(self):
        return '{}-FuncNode({}) \n'.format(str(self.height), self.func.name)


class TerminalNode:
    def __init__(self, possibilities, min_height, max_height, height, **kwargs):
        self.childs = []
        self.height = height
        self.min_height = min_height
        self.max_height = max_height
        self.possibilities = possibilities
        self.value = random.choice(possibilities['vars'] + possibilities['consts'])
        self.is_number = isinstance(self.value, (int, float))
    
    def reservoire(self, selected=None, i=1):
        selected = selected or self
        for child in self.childs:
            selected, i = child.reservoire(selected, i+1)
        if random.random() < 1/i:
            selected = self
        return selected, i

    def __call__(self, value): 
        if self.is_number:
            return self.value
        return value[self.value.index]

    def __repr__(self):
        return '{}-TerminalNode({}) \n'.format(str(self.height), self.value)
