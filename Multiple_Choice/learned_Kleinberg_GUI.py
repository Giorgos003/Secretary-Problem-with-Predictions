import tkinter as tk
from tkinter import messagebox
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

def run_algorithm():
    try:
        n = int(entry_n.get())
        k = int(entry_k.get())
        threshold = float(entry_threshold.get())
        error_rate = float(entry_error.get())

        values = [random.randint(0, 1000) for _ in range(n)]
        predictions = generate_predicted_values(values, error_rate)

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
