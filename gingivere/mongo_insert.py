from pymongo import MongoClient
import load_data
import copy
import json

def insert_patient(name):
    name_to_post_id = {}
    client = MongoClient()
    db = client['gingivere']
    posts = db[name]
    count_i = 0
    count_p = 0

    for data in load_data.walk_training_mats(name):
        post_item = copy.deepcopy(data)
        del post_item['data']
        for i, item in enumerate(data['data']):
            post_item['data'] = item.tolist()
            if 'interictal' in data['file']:
                post_item['int_id'] = count_i
                count_i += 1
            elif 'preictal' in data['file']:
                post_item['int_id'] = count_p
                count_p += 1
            post_id = posts.insert(post_item)
            name = "%02d_%s" % (i, data['file'])
            name_to_post_id[name] = str(post_id)
            print("Just posted: " + name)
            del post_item['_id']

    with open("posts.json", "w") as f:
        json.dump(str(name_to_post_id), f)
        f.close()

if __name__ == "__main__":
    insert_patient('Dog_2')
