from pymongo import MongoClient
import random
import shelve_api
import collections

INTERICTAL_QUERY = {'state':  'interictal'}
PREICTAL_QUERY = {'state': 'preictal'}

def get_all_preictals(collection):
    return collection.find(PREICTAL_QUERY)

def get_all_interictals(collection):
    return collection.find(INTERICTAL_QUERY)

def find_random_docs(posts, query, num):
    n = posts.find(query).count()
    rs = [randint(0,n-1) for i in range(num)]
    query['int_id'] = {'$in' : rs}
    rand_eles = posts.find(query)
    return rand_eles

def load_random_training_set(db, patient, num=500):
    convert = {'interictal': 0, 'preictal': 1}
    data_dict = collections.defaultdict(list)
    for state in ['preictal', 'interictal']:
        for result in get_rand_docs(db, patient, state, num):
            print(state)
            for key in ['data', '_id', 'state']:
                if (key == 'state'):
                    data_dict[key].append(convert[result[key]])
                else:
                    data_dict[key].append(result[key])
    return data_dict

def get_rand_docs(db, patient, state, num=500):
    #TODO change later to patient
    collection = db['posts']
    df = shelve_api.load(patient)
    selection = df[df['state'] == state]
    l_id = list(selection['_id'])
    random.shuffle(l_id)
    l_id = l_id[:num]
    query = {'state': state, '_id': {'$in': l_id}}
    return collection.find(query)

if __name__ == "__main__":
    client = MongoClient()
    db = client['gingivere']
    collection = db.posts
    data_dict = load_random_training_set(db, 'Dog_2')
