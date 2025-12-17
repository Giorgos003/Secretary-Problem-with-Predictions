import math
import random
import numpy 
import heapq
from Kleinberg import secretary_kleinberg


# ---------------- Predictions -------------------
def generate_predicted_values(v: list[int], error_rate: float) -> list[int]:
    predictions = []
    for value in v:
        sigma = error_rate * value
        prediction = value + random.gauss(0, sigma)
        predictions.append(round(prediction))
    return predictions

# ---------------- Learned Kleinberg Algorithm -------------------
def learned_kleinberg(threshold: int, k: int, predictions: list[int], values: list[int]) -> list[int]:
    n = len(predictions)
    predicted_S = heapq.nlargest(k, range(n), key=lambda i: predictions[i]) # Indices of top-k predicted candidates
    S = []  # Final selected candidates

    for i in range(n):
        if math.fabs(1 - predictions[i] / values[i]) > threshold:
            print(f"Switching to Kleinberg's algorithm at candidate {i} (predicted value {predictions[i]}, real value {values[i]}, error {math.fabs(1 - predictions[i] / values[i]):.3f})")
            k = k - len(S) - 1  # We substract the already selected candidates and the current one that
            S.append(i) # Add the current candidate
            # Switch to Kleinberg's algorithm for the remaining candidates
            remaining_candidates = values[i+1:]
            print(f"Remaining candidates for Kleinberg's algorithm: {remaining_candidates}", "k = ", k)
            hired_candidates = secretary_kleinberg(remaining_candidates, k)
            for hired_candidate in hired_candidates:
                S.append(hired_candidate + i + 1)  # Adjust index
            return S
            # return predicted_S + [i] +  secretary_kleinberg(values[i+1:], k)
        
        if i in predicted_S:
            S.append(i)
            if len(S) == k:
                return S
    return S


if __name__ == "__main__":
    n = int(input("Number of candidates: "))
    k = int(input("Number of hires (k): "))
    threshold = float(input("Prediction error threshold (e.g., 0.2 for 20%): "))
    error_rate = float(input("Prediction error rate (e.g., 0.3 for 30%): "))

    values = [random.randint(0, 1000) for _ in range(n)] 
    predictions = generate_predicted_values(values, error_rate)

    print(f"\nCandidate values: {values}")
    print(f"Predicted values: {predictions}\n")

    hired_candidates = learned_kleinberg(threshold, k, predictions, values)
    print(f"Hired candidates: {hired_candidates}, Values: {[values[i] for i in hired_candidates]}")