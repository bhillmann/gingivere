import shelve
from gingivere import SETTINGS

def load_shelve(item):
    try:
        s = shelve.open(SETTINGS.cache_dir + '/shelve')
        loaded = s[item]
    finally:
        s.close()
    return loaded

def insert_shelve(item, name):
    s = shelve.open(SETTINGS.cache_dir + '/shelve')
    try:
        s[name] = item
    finally:
        s.close()
    return item