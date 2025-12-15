import numpy as np
import math
import random

def secretary_dynkin(values: list[int]) -> int | None:
    n = len(values)

    for i in range(n):
        print(f"Candidate {i} arrives with value {values[i]}")

    best_so_far = -float("inf") 
    threshold_index = math.floor(n / math.e)
    print(f"Observation phase ends at candidate index: {threshold_index - 1}")

    # Observation phase for the first n/e candidates
    for i in range(threshold_index):
        if values[i] > best_so_far:
            best_so_far = values[i]
    
    # Selection phase for the remaining candidates
    for i in range(threshold_index, n):
        if values[i] > best_so_far:
            hired = i
            print(f"Hired candidate: {hired}, Value: {values[hired]}")
            return hired
    
    print("No candidate hired.")
    return None



if __name__ == "__main__":
    n = int(input("Number of candidates: "))
    values = [random.randint(0, 100) for _ in range(n)] 
    # candidates = list(range(n)) # Create a list of candidate indices
    # random.shuffle(candidates)
    # values = []
    # for i in range(n):
    #     values[i] = starting_values[candidates[i]]

    print(f"Candidate values: {values}\n")
    secretary_dynkin(values)