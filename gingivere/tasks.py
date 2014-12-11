from gingivere.utilities.time import Timer

from gingivere.preprocess import preprocess_data
from gingivere.process import process_data
from gingivere.postprocess import postprocess_data

def make_submission(post_processed):
    pass

def make_cv_scores(post_processed):
    pass

def make_submission_pipeline():
    pass

def make_cv_scores_pipeline():
    pass

def make_target_cv_scores_pipeline(target, feature_pipeline):
    t = Timer()
    current = preprocess_data(target, feature_pipeline)
    current = process_data(current)
    current = postprocess_data(current)
    make_cv_scores(current)
    print("Completed %s in %s" % (target, t.pretty_str()))

