import scipy.io
import json
import re
import os


def walk_files(patient, path="default"):
    if path == 'default':
        path = DATA_PATH + '/' + patient
    for file in os.listdir(path):
        if 'interictal' in file:
            yield (path, file, 'interictal')
        elif 'preictal' in file:
            yield (path, file, 'preictal')
        elif 'test' in file:
            yield (path, file, 'test')

def walk_training_mats(patient):
    for data in walk_files(patient):
        path, file, state = data
        yield load_mat(path, file, state)

def load_mat(path, file, state):
    mat = scipy.io.loadmat("%s/%s" % (path, file))
    keys = ['data', 'data_length_sec', 'sampling_frequency', 'channels', 'sequence']
    if state == 'test':
        keys = keys[:-1]
    number = int(re.match(r'\d+', file.split('_')[-1]).group())
    values = mat['%s_segment_%d' % (state, number)][0, 0]
    data = dict(zip(keys, values))
    data['data'] = data['data'].astype('float64')
    # Clean the data
    for key in keys[1:]:
        if key == 'channels':
            channels = data[key][0]
            channels = [i[0] for i in channels]
            continue
        data[key] = data[key].flatten()[0]
    data['channels'] = channels
    if state != 'test':
        data['sequence'] = int(data['sequence'])
    data['data_length_sec'] = int(data['data_length_sec'])
    data['state'] = state
    data['file'] = file
    return data


def get_data_path():
    with open('config.json', 'r') as f:
        config = json.load(f)
        f.close()
    return config['data']


DATA_PATH = get_data_path()

def main():
    for data in walk_training_mats("Dog_2"):
        print(data['data'].shape)

if __name__ == "__main__":
    main()
