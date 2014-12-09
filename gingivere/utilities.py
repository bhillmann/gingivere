import shelve
from gingivere import SETTINGS

class Shelve(object):
    def __init__(self):
        self.data_cache = SETTINGS.data_dir

    def load(self, item):
        try:
            s = shelve.open('%s/shelve' % self.data_cache)
            loaded = s[item]
        finally:
            s.close()
        return loaded

    def insert(self, item, name):
        s = shelve.open('%s/shelve' % self.data_cache)
        try:
            s[name] = item
        finally:
            s.close()
        return item
