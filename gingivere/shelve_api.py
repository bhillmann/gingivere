import shelve

def load(item):
    try:
        s = shelve.open('./data/shelve')
        loaded = s[item]
    finally:
        s.close()
    return loaded

def insert(item, name):
    s = shelve.open('./data/shelve')
    try:
        s[name] = item
    finally:
        s.close()
    return item

if __name__ == "__main__":
    df = load('Dog_2')
