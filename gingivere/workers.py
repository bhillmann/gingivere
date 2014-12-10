from multiprocessing import Pool

from gingivere.utilities import TransformationPipeline
from gingivere.data import generate_mat_paths, generate_mat_cvs
from gingivere import SETTINGS

def do_transformation_pipeline(target, transformations):
    pipeline = TransformationPipeline(transformations)
    pool = Pool(SETTINGS.N_jobs)
    paths = [path for path in generate_mat_cvs(target)]
    results = pool.map(pipeline.run, paths)
    return results, paths
