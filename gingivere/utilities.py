class TransformationPipeline:
    def __init__(self, transformations):
        self.transformations = transformations

    def run(self, origin):
        destination = origin
        for transform, kargs in self.transformations:
            destination = transform(destination, **kargs)
        return destination

# (funct,kargs={})