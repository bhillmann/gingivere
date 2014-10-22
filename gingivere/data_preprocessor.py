import shelve
import load_data

for data in load_data.walk_training_mats("Dog_2"):
    for i, item in enumerate(data['data']):
        s = shelve.open('./data/dog_2/dog_2', writeback=True)
        try:
            s["%02d_%s" % (i, data['file'])] = item
        finally:
            s.close()
