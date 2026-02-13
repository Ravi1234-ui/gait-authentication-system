# ml_pipeline.py
import numpy as np
import pandas as pd
from pathlib import Path
from collections import Counter
from scipy.signal import butter, filtfilt
from scipy.stats import entropy
import joblib

FS = 50
WINDOW_SIZE = 128
STEP_SIZE = 64
CONF_THRESHOLD = 0.7


def remove_gravity(signal):
    b, a = butter(3, 0.3 / (0.5 * FS), btype="low")
    gravity = filtfilt(b, a, signal)
    return signal - gravity


def sliding_window(signal):
    return np.array([
        signal[i:i + WINDOW_SIZE]
        for i in range(0, len(signal) - WINDOW_SIZE, STEP_SIZE)
    ])


def extract_features(window):
    return [
        np.mean(window),
        np.std(window),
        np.min(window),
        np.max(window),
        np.sum(window ** 2) / len(window),
        entropy(np.abs(window) + 1e-6)
    ]


def extract_all_features(ax, ay, az, gx, gy, gz):
    features = []
    for i in range(len(ax)):
        row = []
        for sig in [ax[i], ay[i], az[i], gx[i], gy[i], gz[i]]:
            row.extend(extract_features(sig))
        features.append(row)
    return np.array(features)


def authenticate(person_dir):
    model = joblib.load("models/gait_model2.pkl")
    label_map = joblib.load("models/label_map_realworld.pkl")
    
    acc = pd.read_csv(person_dir / "acc.csv")
    gyro = pd.read_csv(person_dir / "gyro.csv")

    ax = remove_gravity(acc["x"].values)
    ay = remove_gravity(acc["y"].values)
    az = remove_gravity(acc["z"].values)

    gx, gy, gz = gyro["x"].values, gyro["y"].values, gyro["z"].values

    ax, ay, az = map(sliding_window, [ax, ay, az])
    gx, gy, gz = map(sliding_window, [gx, gy, gz])

    n = min(len(ax), len(gx))
    if n == 0:
        return {"decision": "ACCESS DENIED", "confidence": 0.0}

    X = extract_all_features(
        ax[:n], ay[:n], az[:n],
        gx[:n], gy[:n], gz[:n]
    )

    probs = model.predict_proba(X)
    preds = model.classes_[np.argmax(probs, axis=1)]
    confs = np.max(probs, axis=1)

    valid = [(p, c) for p, c in zip(preds, confs) if c >= CONF_THRESHOLD]

    if not valid:
        return {
            "decision": "ACCESS DENIED",
            "confidence": round(float(np.mean(confs)), 3)
        }

    final_label = Counter([p for p, _ in valid]).most_common(1)[0][0]

    return {
        "decision": "ACCESS GRANTED",
        "person": label_map[final_label],
        "confidence": round(float(np.mean(confs)), 3),
        "threshold": CONF_THRESHOLD
    }
