import random
from Generate_Values.real_values import generate_real_values_uniform, generate_real_values_adversarial, generate_real_values_almost_constant
from Generate_Values.predictions import generate_predicted_values_uniform, generate_predicted_values_adversarial, generate_predicted_values_almost_constant


def learned_Dynkin(tau : float, theta : float, v : list[float], arrival_times : list[float], predictions : list[float]):

    n = len(v)
    candidates = list(range(n)) 
    
    random.shuffle(candidates)
    candidates.sort(key=lambda i: arrival_times[i]) # sort candidates by arrival time
    for i in range(n):
        print(f"Candidate {candidates[i]} arrives at time {arrival_times[candidates[i]]:.3f} with value {v[candidates[i]]} and predicted value {predictions[candidates[i]]}")
    print(f"---------------------------------------------")

    best_predicted_value = max(range(n), key=lambda i: predictions[i]) # find index of max value in predictions
    best_real_value = max(range(n), key=lambda i: v[i]) # find index of max value in real values
    print(f"Best predicted candidate is {best_predicted_value} with predicted value {predictions[best_predicted_value]} and real value {v[best_predicted_value]}")
    print(f"Best real candidate is {best_real_value} with real value {v[best_real_value]} and predicted value {predictions[best_real_value]}")
    print(f"---------------------------------------------")

    mode = "PREDICTION"
    best_so_far = -float("inf")
    hired = None

    for i in candidates:
        if abs(1 - predictions[i] / v[i]) > theta:
            print(f"Switching to SECRETARY mode at candidate {i} (predicted value {predictions[i]}, {abs(1 - predictions[i] / v[i]):.3f})")
            mode = "SECRETARY"
        if mode == "PREDICTION" and i==best_predicted_value:
            hired = i
            break        
        if mode == "SECRETARY" and arrival_times[i] > tau and v[i] >= best_so_far:
            best_so_far = v[i]
            hired = i
            break
        if (v[i] >= best_so_far): 
                best_so_far = v[i]
            
    
    print(f"Hired candidate: {hired}, Value: {v[hired] if hired is not None else None}, Mode: {mode}")
    return hired


if __name__ == "__main__":
    tau = 0.313
    theta = 0.646

    # Τυχαίες τιμές υποψηφίων
    n = int(input("Πόσοι υποψήφιοι; "))

    arrival_times = {i: random.random() for i in range(n)}  

    # Uniformly distributed values and predictions
    print("\n--- Uniformly distributed values and predictions ---")
    v = generate_real_values_uniform(n)
    predictions = generate_predicted_values_uniform(v, error_rate=0.7)

    # Adversarial values and predictions
    # v = generate_real_values_adversarial(n)
    # predictions = generate_predicted_values_adversarial(v, error_rate=0.2)

    # Almost constant values and predictions
    # v = generate_real_values_almost_constant(n, error_rate=0.2, k=math.ceil(n/10))
    # predictions = generate_predicted_values_almost_constant(v)

    print(f"\nΤιμές πραγματικές: {v}")
    print(f"Προβλέψεις: {predictions}\n")


    learned_Dynkin(tau, theta, v, arrival_times, predictions)