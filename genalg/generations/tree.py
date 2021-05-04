import random
from functools import namedtuple

Function = namedtuple('Func', ['num_childs', 'name', 'func'])
Variable = namedtuple('Var', ['name', 'index'])

# dict keys: vars, consts, funcs

class Individual:
    def __init__(self, possibilities, min_height, max_height, height=0):
        self.possibilities = possibilities
        self.node = FuncNode(possibilities, min_height, max_height, height)


class FuncNode:
    def __init__(self, possibilities, min_height, max_height, height):
        self.height = height
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
                self.childs.append(TerminalNode(possibilities, height + 1))
            else:
                self.childs.append(TerminalNode(possibilities, height + 1) if is_l_son_terminal
                                   else FuncNode(possibilities, min_height, max_height, height + 1))
        else:
            if height >= max_height - 1:
                [self.childs.append(TerminalNode(possibilities, height + 1)) for i in range(2)]
            # can't add two terminal sons while tree height < min_height
            elif is_l_son_terminal and is_r_son_terminal and min_height > height:
                self.childs.append(TerminalNode(possibilities, height + 1))
                self.childs.append(FuncNode(possibilities, min_height, max_height, height + 1))
            else:
                self.childs.append(TerminalNode(possibilities, height + 1) if is_l_son_terminal
                    else FuncNode(possibilities, min_height, max_height, height + 1))
                self.childs.append(TerminalNode(possibilities, height + 1) if is_r_son_terminal
                    else FuncNode(possibilities, min_height, max_height, height + 1))

    def __call__(self, value):
        res = [child(value) for child in self.childs]
        return self.func.func(*res)

    def __repr__(self):
        # res = []
        # res.append([str(child) for child in self.childs])
        # print()
        return '{}-FuncNode({}) \n'.format(str(self.height), self.func.name)


class TerminalNode:
    def __init__(self, possibilities, height):
        self.childs = []
        self.height = height
        self.value = random.choice(possibilities['vars'] + possibilities['consts'])
        self.is_number = isinstance(self.value, (int, float))
    
    def __call__(self, value):
        if self.is_number:
            return self.value
        return value[self.value.index]

    def __repr__(self):
        return '{}-TerminalNode({}) \n'.format(str(self.height), self.value)


def print_tree(root, level=0):
    print('  ' * level, str(root))
    for child in root.childs:
        print_tree(child, level+1)


plus = Function(2, 'plus', lambda x, y: x+y)
mult = Function(2, 'mult', lambda x, y: x*y)
abss = Function(1, 'abs', abs)

x1 = Variable('x1', 0)
x2 = Variable('x2', 1)

poss = {
    'funcs': [plus, mult, abss],
    'vars': [x1, x2],
    'consts': list(range(2))
}

t = Tree(poss, 2, 7)
print_tree(t.node)
print(t.node([3, 1]))