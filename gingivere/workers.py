from multiprocessing import Pool

from gingivere.utilities import TransformationPipeline
from gingivere.data import generate_mat_paths, mask_tests
from gingivere import SETTINGS

def do_transformation_pipeline(target, transformations):
    print(transformations)
    pipeline = TransformationPipeline(transformations)
    pool = Pool(SETTINGS.N_jobs)
    results = pool.map(pipeline.run, [path for path in mask_tests(generate_mat_paths(target))])
    return results
