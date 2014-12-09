class Bin(object):
    def __init__(self, data):



class Mutation:
    def apply(self):


class Evolution:
    def __init__(self, mutations):
        self.mutations = mutations

    def apply(self):
        for transform in self.mutations:
            transform.apply()




