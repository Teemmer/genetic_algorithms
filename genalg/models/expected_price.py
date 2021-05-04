from genalg.models import ClassicModel

class ExpectedPriceModel(ClassicModel):
    def __init__(self, 
                 num_tourn=3, 
                 chance_mutation=0.2, 
                 chance_crossing=0.8, 
                 elite_percents=0.1,
                 kappa=0.8,
                 **kwargs):
        super().__init__(num_tourn, chance_mutation, chance_crossing, **kwargs)
        self.elite_percents = elite_percents
        self.kappa = kappa
