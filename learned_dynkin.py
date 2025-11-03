import numpy as np
import math
import random


def learned_Dynkin(tau : float, theta : float, v : list[float], v_hat : list[float]):

    n = len(v)
    candidates = list(range(n)) 
    random.shuffle(candidates)

    i_hat = max(range(n), key=lambda i: v_hat[i]) # find index of max value in v_hat
    print(f"Best predicted candidate is {i_hat} with predicted value {v_hat[i_hat]}")
    print(f"---------------------------------------------")

    mode = "PREDICTION"
    best_so_far = -float("inf")
    hired = None

    # arrival_times = {i: random.random() for i in candidates}   # assign random arrival times
    arrival_times = {i: t for i, t in zip(candidates, [k/(n-1) for k in range(n)])} # assign deterministic arrival times where the i-th candidate arrives at time i/(n-1)
    candidates.sort(key=lambda i: arrival_times[i]) # sort candidates by arrival time
    for i in range(n):
        print(f"Candidate {candidates[i]} arrives at time {arrival_times[candidates[i]]:.3f} with value {v[candidates[i]]} and predicted value {v_hat[candidates[i]]}")

    print(f"Predicted best candidate is {i_hat} with predicted value {v_hat[i_hat]}")
    print(f"---------------------------------------------")

    for i in candidates:
        if (v[i] >= best_so_far): 
                best_so_far = v[i]
        if abs(1 - v_hat[i] / v_hat[i_hat]) > theta:
            print(f"Switching to SECRETARY mode at candidate {i} (predicted value {v_hat[i]}, {abs(1 - v_hat[i] / v_hat[i_hat]):.3f})")
            mode = "SECRETARY"
        if mode == "PREDICTION" and i==i_hat:
            hired = i
            break
        if mode == "SECRETARY" and arrival_times[i] > tau and v[i] >= best_so_far:
            best_so_far = v[i]
            hired = i
            break
    
    print(f"Hired candidate: {hired}, Value: {v[hired] if hired is not None else None}, Mode: {mode}")
    return hired


# Example usage
if __name__ == "__main__":
    tau = 0.313
    theta = 0.646
    #v = [10, 20, 15, 30, 25]
    #v_hat = [12, 18, 14, 28, 22]

    # Τυχαίες τιμές υποψηφίων
    n = int(input("Πόσοι υποψήφιοι; "))
    v = [random.randint(0, 100) for _ in range(n)] 
    v_hat = [v[i] + random.randint(-30, 30) for i in range(n)] # Προβλέψεις με τυχαίο σφάλμα ±30

    print(f"\nΤιμές πραγματικές: {v}")
    print(f"Προβλέψεις: {v_hat}\n")


    learned_Dynkin(tau, theta, v, v_hat)