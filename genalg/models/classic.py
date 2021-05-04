from .base import BaseModel

class ClassicModel(BaseModel):

    def __init__(self, num_tourn=3, chance_mutation=0.2, chance_crossing=0.8, **kwargs):
        super().__init__(**kwargs)
        self.num_tourn = num_tourn
        self.chance_mutation = chance_mutation
        self.chance_crossing = chance_crossing
