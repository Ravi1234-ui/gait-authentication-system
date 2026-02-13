import numpy as np
import joblib


class GaitIdentifier:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def predict(self, X, threshold=0.7):
        probs = self.model.predict_proba(X)
        preds = self.model.classes_[np.argmax(probs, axis=1)]
        confs = np.max(probs, axis=1)

        results = []
        for p, c in zip(preds, confs):
            if c >= threshold:
                results.append((int(p), float(c), "ACCESS GRANTED"))
            else:
                results.append((None, float(c), "ACCESS DENIED"))
        return results
