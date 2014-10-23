from pymongo import MongoClient
import random
import shelve_select
import collections

INTERICTAL_QUERY = {'state':  'interictal}'
PREICTAL_QUERY = {'state' = 'preictal'}

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

def template_dict(dict, result):
    convert = {'interictal': 0, 'preictal': 1}
    for string in ['data', '_id', 'state']:
        if string == 'state':
            dict[string].append(convert[string])
        else:
            dict[string].append(result[string])
    return dict

def load_random_training_set(db, patient, num=500):
    d = collections.defaultdict()
    for state in ('preictal', 'interictal'):
        for result in get_rand_docs(db, patient, state, num):
            d = template_dict(d, result)
    return d

def get_rand_docs(db, patient, state, num=500):
    #TODO change later to patient
    collection = db['posts']
    df = shelve_select.load_patient(patient)
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
