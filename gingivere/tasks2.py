from gingivere.utilities.time import Timer

def process_data(pre_processed, process_pipeline, train=True):
    pass

def postprocess_data(processed, post_process_pipeline):
    pass

def make_submission(post_processed):
    pass

def make_cv_scores(post_processed):
    pass

def make_submission_pipeline():
    pass

def make_cv_scores_pipeline():
    pass

def make_target_cv_scores_pipeline(target, feature_pipeline, preprocess_pipeline, process_pipeline, post_process_pipeline):
    t = Timer
    current = preprocess_data(target, feature_pipeline, preprocess_pipeline)
    current = process_data(current, process_pipeline)
    current = postprocess_data(current, post_process_pipeline)
    make_cv_scores(current)
    print("Completed %s in %s" % (target, t.pretty_str()))

