import numpy as np
from scipy.stats import entropy


def extract_features(window):
    feats = []
    feats.extend([
        np.mean(window),
        np.std(window),
        np.min(window),
        np.max(window),
        np.sum(window ** 2) / len(window),  # energy
        entropy(np.abs(window) + 1e-6)
    ])
    return feats


def extract_all_features(acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z):
    features = []
    for i in range(len(acc_x)):
        row = []
        row.extend(extract_features(acc_x[i]))
        row.extend(extract_features(acc_y[i]))
        row.extend(extract_features(acc_z[i]))
        row.extend(extract_features(gyro_x[i]))
        row.extend(extract_features(gyro_y[i]))
        row.extend(extract_features(gyro_z[i]))
        features.append(row)
    return np.array(features)
