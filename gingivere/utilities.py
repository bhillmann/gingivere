import shelve

class Shelve(object):
    def __init__(self, settings):
        self.data_cache = settings.data_cache

    def load_shelve(self, item):
        try:
            s = shelve.open('%s/shelve' % self.data_cache)
            loaded = s[item]
        finally:
            s.close()
        return loaded

    def insert_shelve(self, item, name):
        s = shelve.open('%s/shelve' % self.data_cache)
        try:
            s[name] = item
        finally:
            s.close()
        return item
