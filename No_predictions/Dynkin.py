import numpy as np
import random

def secretary_dynkin(values: list[float], arrival_times: list[float], threshold: float) -> int | None:
    """
    Implements the classical secretary problem algorithm.
    Parameters:
    - values: A list of values of the candidates.
    - arrival_times: A list of arrival times for the candidates, uniformly distributed in [0, 1].
    - threshold: The threshold time which determines the selection phase. Candidates arriving before this time are observed but not selected.
    Returns:
    - The index of the hired candidate, or None if no candidate is hired.
    """

    n = len(values)

    # Sort candidates by their arrival times
    candidates = list(range(n))
    candidates.sort(key=lambda i: arrival_times[i])

    # print the arrival times and values of the candidates
    print(f"Candidates sorted by arrival time:")
    for i in candidates:
        print(f"Candidate {i} arrives at time {arrival_times[i]} with value {values[i]}")

    # Find the best candidate based on the values so we can compare it with the hired candidate later
    best_candidate = max(range(n), key=lambda i: values[i])
    print(f"Best candidate is {best_candidate} with value {values[best_candidate]} and arrival time {arrival_times[best_candidate]}")
    print(f"---------------------------------------------")

    # Initialize variables to keep track of the best candidate seen so far and the hired candidate
    hired = None
    best_so_far = -float("inf") 

    # Iterate through the candidates in order of arrival time
    for candidate in candidates:
        if arrival_times[candidate] <= threshold:
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
    # Get the number of candidates from the user
    n = int(input("Number of candidates: "))
    
    # We create the values of the candidates using the exponential distribution.
    values = generate_real_values_uniform(n)

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