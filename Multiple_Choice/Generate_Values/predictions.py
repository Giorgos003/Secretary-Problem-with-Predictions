import random
import numpy 
import heapq

# ---------------- Predictions -------------------

def generate_predicted_values_uniform(v: list[float], error_rate: float) -> list[float]:
    predictions = []
    for value in v:
        prediction = value * (numpy.random.uniform(1 - error_rate, 1 + error_rate))
        predictions.append(prediction)
    return predictions

def generate_predicted_values_adversarial(v: list[float], error_rate: float) -> list[float]:
    predictions = []
    top_half = set(heapq.nlargest(len(v)//2, range(len(v)), key=lambda i: v[i]))  # Indices of top half candidates
    for i in range(len(v)):
        if i in top_half:
            prediction = v[i] * (1 - error_rate)
        else:
            prediction = v[i] * (1 + error_rate)
        predictions.append(prediction)
    return predictions

def generate_predicted_values_almost_constant(v: list[float]) -> list[float]:
    predictions = [1 for _ in v]

    for i in range(len(predictions)):
        predictions[i] = predictions[i] + predictions[i] * random.uniform(0, 0.01)

    return predictions