from pymongo import MongoClient
import load_data
import copy
import json

def main():
    name_to_post_id = {}
    client = MongoClient()
    db = client['gingivere']
    posts = db.posts

    for data in load_data.walk_training_mats("Dog_2"):
        post_item = copy.deepcopy(data)
        del post_item['data']
        for i, item in enumerate(data['data']):
            post_item['data'] = item.tolist()
            post_id = posts.insert(post_item)
            name = "%02d_%s" % (i, data['file'])
            name_to_post_id[name] = post_id
            print("Just posted: " + name)
            del post_item['_id']

    with open("posts.json") as f:
        json.dump(name_to_post_id, f)
        f.close()

if __name__ == "__main__":
    main()
