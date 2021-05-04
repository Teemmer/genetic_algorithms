class BaseGeneration:

    def __init__(self, params, eval_func, **kwargs):
        self.params = params
        self.bits_lenght = self.get_length()
        self.eval_func = eval_func

    def get_length(self):
        return sum(map(lambda x: x.bits_num, self.params))