import scipy.io
import json
# from sklearn.decomposition import PCA
#
# from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import chi2
#
# import tables


def load_mat(dir):
    # mat = scipy.io.loadmat(DATA_DIR + "Dog_22/Dog_2_preictal_segment_0001.mat")
    # xx = mat['preictal_segment_1'][0,0]
    # data = xx[0]
    # data_length_sec = xx[1]
    # sampling_frequency = xx[2]
    # channels = xx[3]
    # sequence = xx[4]
    # return{

    # }
    pass


if __name__ == "__main__":
    with open('config.json', 'r') as f:
        DATA_DIR = json.load(f)
        f.close()
    mat = scipy.io.loadmat(DATA_DIR + "Dog_22/Dog_2_preictal_segment_0001.mat")
    xx = mat['preictal_segment_1'][0, 0]
    data = xx[0]
    data_length_sec = xx[1]
    sampling_frequency = xx[2]

    channels = xx[3]
    # Clean the channels
    channels = [x[0] for x in channels[0]]
    sequence = xx[4]
    print(DATA_DIR)