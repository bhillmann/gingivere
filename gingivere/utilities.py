def run_transformation_pipeline(transformations, origin):
    destination = origin
    for transform, kargs in transformations:
        destination = transform(destination, **kargs)
    return destination

# (funct,kargs={})