import random
import numpy 


#---------------- Real Values -------------------

def generate_real_values_uniform(n: int) -> list[float]:
    values = []
    for i in range(n):
        value = numpy.random.exponential(scale=1)
        values.append(value)
    return values

def generate_real_values_adversarial(n: int) -> list[float]:
    values = []
    for i in range(n):
        value = numpy.random.exponential(scale=1)
        values.append(value)
    return values

def generate_real_values_almost_constant(n: int, error_rate: float, k: int) -> list[float]:
    values = [1.0] * n  # All values are 1
    indices = random.sample(range(n), k)  # Randomly select k different indices to have higher values

    for i in indices:
        values[i] = 1 / (1 - error_rate)  # Set higher value based on error rate

    for i in range(n):
        values[i] = values[i] + random.uniform(0, 0.01)
    
    return values