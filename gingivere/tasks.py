
def build_feature_vectors():
    features = []
    targets = []
    for i, path in enumerate(paths):
        for row in features[i]:
            features.append(row)
        targets = len(features[i])

def build_target_vector():
    pass

def load_data_for_cv(data):
    features, paths = data
    X = build_feature_vectors(features)
    y = build_target_vector(features, path)
    return X, y