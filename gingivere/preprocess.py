from multiprocessing import Pool

from gingivere import SETTINGS
from gingivere.data import generate_mat_cvs
from gingivere.features import FeaturePipeline

def preprocess_data(target, feature_pipeline, preprocess_pipeline):
    pool = Pool(SETTINGS.N_jobs)
    paths = [path for path in generate_mat_cvs(target)]
    feature_pipeline = FeaturePipeline(feature_pipeline)
    results = pool.map(feature_pipeline.run, paths)
    return results

def preprocess_dataframe():
    pass
