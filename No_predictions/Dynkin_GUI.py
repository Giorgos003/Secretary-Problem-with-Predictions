import tkinter as tk
from tkinter import ttk
import numpy as np
import random


def generate_real_values_uniform(n):
    """
    Generates a list of n real values from an exponential distribution.
    Parameters:
    - n: The number of values to generate.
    Returns:
    - A list of n real values.
    """
    return list(np.random.exponential(scale=1, size=n))



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

    candidates = list(range(n))
    candidates.sort(key=lambda i: arrival_times[i])

    output = []

    for i in candidates:
        output.append(
            f"Candidate {i} arrives at time {arrival_times[i]:.3f} "
            f"with value {values[i]:.3f}"
        )

    best_candidate = max(range(n), key=lambda i: values[i])

    output.append("")
    output.append(
        f"Best candidate: {best_candidate} "
        f"(value={values[best_candidate]:.3f}, "
        f"time={arrival_times[best_candidate]:.3f})"
    )
    output.append("-" * 50)

    best_so_far = -float("inf")

    for candidate in candidates:
        if arrival_times[candidate] <= threshold:
            best_so_far = max(best_so_far, values[candidate])
        else:
            if values[candidate] > best_so_far:
                output.append(
                    f"Hired candidate: {candidate} "
                    f"(value={values[candidate]:.3f}, "
                    f"time={arrival_times[candidate]:.3f})"
                )
                return "\n".join(output)

    output.append("No candidate hired.")
    return "\n".join(output)



def run_simulation():
    try:
        n = int(n_entry.get())  # number of candidates
        threshold = float(threshold_entry.get())    # threshold for the observation phase

        # If the user selects manual input, we will get the values from the entry field. Otherwise, we will generate random values.
        if input_mode.get() == "manual":
            values = [float(x.strip()) for x in values_entry.get().split(",")]

            if len(values) != n:
                raise ValueError(f"You entered {len(values)} values but n = {n}")
            
            arrival_times = {i: i / n for i in range(n)}    # uniform arrival times for manual input
        else:
            values = generate_real_values_uniform(n)
            arrival_times = {i: random.random() for i in range(n)}  # uniformly random arrival times between [0, 1] for random input


        result = secretary_dynkin(values, arrival_times, threshold)

        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)

    except ValueError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Please enter valid numbers.")


# ---------------- UI ----------------

root = tk.Tk()
root.title("Dynkin Secretary Problem")
root.geometry("800x600")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="x")

ttk.Label(frame, text="Number of Candidates:").grid(row=0, column=0, sticky="w")
n_entry = ttk.Entry(frame)
n_entry.insert(0, "20")
n_entry.grid(row=0, column=1)

ttk.Label(frame, text="Threshold (0-1):").grid(row=1, column=0, sticky="w")
threshold_entry = ttk.Entry(frame)
threshold_entry.insert(0, "0.37")
threshold_entry.grid(row=1, column=1)

run_button = ttk.Button(frame, text="Run Simulation", command=run_simulation)
run_button.grid(row=2, column=0, columnspan=2, pady=10)

input_mode = tk.StringVar(value="random")

ttk.Radiobutton(
    frame,
    text="Random Values",
    variable=input_mode,
    value="random"
).grid(row=3, column=0, sticky="w")

ttk.Radiobutton(
    frame,
    text="Manual Values",
    variable=input_mode,
    value="manual"
).grid(row=3, column=1, sticky="w")

ttk.Label(frame, text="Manual Values (comma separated):").grid(
    row=4, column=0, sticky="w"
)
values_entry = ttk.Entry(frame, width=50)
values_entry.grid(row=4, column=1)

output_text = tk.Text(root, wrap="word")
output_text.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()