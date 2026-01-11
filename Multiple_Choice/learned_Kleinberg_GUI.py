import tkinter as tk
from tkinter import messagebox
import math
import random
import numpy 
import heapq
from Kleinberg import secretary_kleinberg


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
        predictions[i] = predictions[i] + random.uniform(0, 0.01)

    return predictions




# ---------------- Learned Kleinberg Algorithm -------------------

def learned_kleinberg(threshold: int, k: int, predictions: list[float], values: list[float]) -> list[float]:
    n = len(predictions)
    predicted_S = heapq.nlargest(k, range(n), key=lambda i: predictions[i]) # Indices of top-k predicted candidates
    S = []  # Final selected candidates

    for i in range(n):
        if math.fabs(1 - predictions[i] / values[i]) > threshold:
            print(f"Switching to Kleinberg's algorithm at candidate {i} (predicted value {predictions[i]}, real value {values[i]}, error {math.fabs(1 - predictions[i] / values[i]):.3f})")
            k = k - len(S) - 1  # We substract the already selected candidates and the current one that we select
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



# ---------------- GUI Application -------------------
def run_algorithm():
    try:
        n = int(entry_n.get())
        k = int(entry_k.get())
        threshold = float(entry_threshold.get())
        error_rate = float(entry_error.get())

        # values = generate_real_values_uniform(n)
        # predictions = generate_predicted_values_uniform(values, error_rate)

        values = generate_real_values_adversarial(n)
        predictions = generate_predicted_values_adversarial(values, error_rate)

        # values = generate_real_values_almost_constant(n, error_rate, k)
        # predictions = generate_predicted_values_almost_constant(values)

        for i in range(n):
            print(f"Candidate {i}: Real Value = {values[i]}, Predicted Value = {predictions[i]}")

        hired = learned_kleinberg(threshold, k, predictions, values)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Candidate values:\n{values}\n\n")
        output_text.insert(tk.END, f"Predicted values:\n{predictions}\n\n")
        output_text.insert(
            tk.END,
            f"Hired candidates (indices): {hired}\n"
            f"Hired values: {[values[i] for i in hired]}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))





# --- GUI setup ---
root = tk.Tk()
root.title("Secretary Problem with Predictions")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Number of candidates (n):").grid(row=0, column=0, sticky="w")
entry_n = tk.Entry(frame)
entry_n.grid(row=0, column=1)

tk.Label(frame, text="Number of hires (k):").grid(row=1, column=0, sticky="w")
entry_k = tk.Entry(frame)
entry_k.grid(row=1, column=1)

tk.Label(frame, text="Prediction threshold:").grid(row=2, column=0, sticky="w")
entry_threshold = tk.Entry(frame)
entry_threshold.grid(row=2, column=1)

tk.Label(frame, text="Prediction error rate:").grid(row=3, column=0, sticky="w")
entry_error = tk.Entry(frame)
entry_error.grid(row=3, column=1)

tk.Button(frame, text="Run Algorithm", command=run_algorithm).grid(
    row=4, column=0, columnspan=2, pady=10
)

output_text = tk.Text(root, height=15, width=70)
output_text.pack(padx=10, pady=10)

root.mainloop()
