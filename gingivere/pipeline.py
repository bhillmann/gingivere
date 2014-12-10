class Pipeline:
    def __init__(self, transformations):
        self.transformations = transformations

    def run(self, origin):
        destination = origin
        for transform in self.transformations:
            destination = transform.apply(destination)
        return destination
