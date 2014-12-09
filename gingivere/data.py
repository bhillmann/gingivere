import scipy.io
import re

def walk_files(patient):
    if path == 'default':
        path = DATA_PATH + '/' + patient
    for file in os.listdir(path):
        if 'interictal' in file:
            yield (path, file, 'interictal')
        elif 'preictal' in file:
            yield (path, file, 'preictal')
        elif 'test' in file:
            yield (path, file, 'test')

def generate_mats(target):
    for data in walk_files(target):
        path, file, state = data
        yield load_mat(path, file, state)

def load_mat(path):
    with scipy.io.loadmat(path) as mat:
        keys = ['data', 'data_length_sec', 'sampling_frequency', 'channels', 'sequence']
        if 'test' in path:
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
    with open('SETTINGS.json', 'r') as f:
        config = json.load(f)
        f.close()
    return config['data']

def main():
    for data in walk_training_mats("Dog_2"):
        print(data['data'].shape)

if __name__ == "__main__":
    main()
