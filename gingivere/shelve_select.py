import shelve

def load_patient(patient):
    try:
        s = shelve.open('./data/shelve')
        df = s[patient]
    finally:
        s.close()
    return df

if __name__ == "__main__":
    df = load_patient('Dog_2')
