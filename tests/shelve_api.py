import shelve

def load_shelve(item):
    try:
        s = shelve.open('./data/shelve')
        loaded = s[item]
    finally:
        s.close()
    return loaded

def insert_shelve(item, name):
    s = shelve.open('./data/shelve')
    try:
        s[name] = item
    finally:
        s.close()
    return item

def main():
    df = load('Dog_2')

if __name__ == "__main__":
    main()
