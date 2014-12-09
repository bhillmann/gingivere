# import mongo_select

# def shelve_data(patient, name):
#     client = MongoClient()
#     db = client['gingivere']
#     collection = db.posts
#     data_dict = mongo_select.load_random_training_set(db, patient)
#     shelve_api.insert(data_dict, name)
from tests import shelve_api


def load_shelve(name):
    return shelve_api.load(name)

if __name__ == "__main__":
    shelve_data('Dog_2', 'test')
