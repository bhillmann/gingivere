__author__ = 'Benjamin'

from multiprocessing import Pool
from gingivere import *

def run_prepare_data_for_cross_validation(targets, pipelines):
    pass

def run_cross_validation(settings, targets, classifiers, pipelines):
    print('Cross-validation task')
    print('Targets', ', '.join(targets))
    print('Pipelines:\n ', '\n  '.join([p.get_name() for p in pipelines]))
    print('Classifiers', ', '.join([c[1] for c in classifiers]))

    run_prepare_data_for_cross_validation(targets, pipelines)

    # run on pool first, then show results after
    pool = Pool(SETTINGS.N_jobs)
    for i, pipeline in enumerate(pipelines):
        for j, (classifier, classifier_name) in enumerate(classifiers):
            for k, target in enumerate(targets):
                progress_str = 'P=%d/%d C=%d/%d T=%d/%d' % (i+1, len(pipelines), j+1, len(classifiers), k+1, len(targets))
                cross_validation_score(settings, target, pipeline, classifier, classifier_name,
                                       strategy=cross_validation_strategy, pool=pool, progress_str=progress_str, return_data=False, quiet=True)
    pool.close()
    pool.join()

    summaries = []
    best = {}
    for p_num, pipeline in enumerate(pipelines):
        for c_num, (classifier, classifier_name) in enumerate(classifiers):
            mean_scores = []
            median_scores = []
            datas = []
            for target in targets:
                print 'Running %s pipeline %s classifier %s' % (target, pipeline.get_name(), classifier_name)
                data = cross_validation_score(settings, target, pipeline, classifier, classifier_name,
                                              strategy=cross_validation_strategy, quiet=True)
                datas.append(data)
                if data.mean_score != data.median_score:
                    print '%.3f (mean)' % data.mean_score, data.mean_scores
                    print '%.3f (median)' % data.median_score, data.median_scores
                else:
                    print '%.3f' % data.mean_score
                mean_scores.append(data.mean_score)
                median_scores.append(data.median_score)

                best_score = best.get(target, [0, None, None, None])[0]
                cur_score = max(data.mean_score, data.median_score)
                if cur_score > best_score:
                    best[target] = [cur_score, pipeline, classifier, classifier_name]

            name = 'p=%d c=%d %s mean %s' % (p_num, c_num, classifier_name, pipeline.get_name())
            summary = get_score_summary(name, mean_scores)
            summaries.append((summary, np.mean(mean_scores)))
            print summary
            name = 'p=%d c=%d %s median %s' % (p_num, c_num, classifier_name, pipeline.get_name())
            summary = get_score_summary(name, median_scores)
            summaries.append((summary, np.mean(median_scores)))
            print summary

    print_results(summaries)

    print '\nbest'
    for target in targets:
        pipeline = best[target][1]
        classifier_name = best[target][3]
        print target, best[target][0], classifier_name, pipeline.get_names()