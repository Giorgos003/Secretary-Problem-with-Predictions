import math
import random
import heapq
from Kleinberg import secretary_kleinberg
from Generate_Values.real_values import generate_real_values_uniform, generate_real_values_adversarial, generate_real_values_almost_constant
from Generate_Values.predictions import generate_predicted_values_uniform, generate_predicted_values_adversarial, generate_predicted_values_almost_constant


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
                S.append(hired_candidate + i + 1)  # Here, we adjust the indices came from secretary_kleinberg() properly
            return S
        
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

    # Uniformly distributed values and predictions
    print("\n--- Uniformly distributed values and predictions ---")
    values = generate_real_values_uniform(n)
    predictions = generate_predicted_values_uniform(values, error_rate)

    # Adversarial values and predictions
    # print("\n--- Adversarial values and predictions ---")
    # values = generate_real_values_adversarial(n)
    # predictions = generate_predicted_values_adversarial(values, error_rate)

    # Almost constant values and predictions
    # print("\n--- Almost constant values and predictions ---")
    # values = generate_real_values_almost_constant(n, error_rate, r=math.ceil(n/10))
    # predictions = generate_predicted_values_almost_constant(values)



    print(f"\nCandidate values: {values}")
    print(f"Predicted values: {predictions}\n")

    hired_candidates = learned_kleinberg(threshold, k, predictions, values)
    print(f"Hired candidates: {hired_candidates}, Values: {[values[i] for i in hired_candidates]}")