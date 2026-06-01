import numpy as np
import random

def secretary_dynkin(values: list[float], arrival_times: list[float], threshold: float) -> int | None:
    n = len(values)

    # Sort candidates by their arrival times
    candidates = list(range(n))
    candidates.sort(key=lambda i: arrival_times[i])

    for i in candidates:
        print(f"Candidate {i} arrives at time {arrival_times[i]} with value {values[i]}")


    best_candidate = max(range(n), key=lambda i: values[i])
    print(f"Best candidate is {best_candidate} with value {values[best_candidate]} and arrival time {arrival_times[best_candidate]}")
    print(f"---------------------------------------------")

    best_so_far = -float("inf") 

    for candidate in candidates:
        if arrival_times[candidate] < threshold:
            if values[candidate] > best_so_far:
                best_so_far = values[candidate]
        else:
            if values[candidate] > best_so_far:
                hired = candidate
                print(f"Hired candidate: {hired}, Value: {values[hired]}, Arrival time: {arrival_times[hired]}")
                return hired
        
    
    print("Dynkin: No candidate hired.")
    return None




def generate_real_values_uniform(n: int) -> list[float]:
    values = []
    for i in range(n):
        value = np.random.exponential(scale=1)
        values.append(value)
    return values



if __name__ == "__main__":
    n = int(input("Number of candidates: "))
    
    # We create the values of the candidates using the exponential distribution.
    values = generate_real_values_uniform(n)


    # For simplicity, we will just ask the user to input the values of the candidates and their arrival times.
    # values = []
    # for i in range(n):
    #     value = float(input(f"Value of candidate {i}: "))
    #     values.append(value)
    # print(f"Candidate values: {values}\n")

    # Generate random arrival times for each candidate from a uniform distribution between 0 and 1.
    arrival_times = []
    for i in range(n):
        time = random.random()
        arrival_times.append(time)

    # Ask the user to input the threshold time for the selection phase.
    threshold_index = float(input(f"Enter the threshold time: "))
    print(f"Threshold time: {threshold_index}\n")

    # Run the Dynkin's algorithm for the classical secretary problem without predictions.
    secretary_dynkin(values, arrival_times, threshold_index)