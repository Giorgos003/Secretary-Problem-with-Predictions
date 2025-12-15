import tkinter as tk
from tkinter import ttk
import random

# ---------------- Algorigthm -------------------

def learned_Dynkin(tau: float, theta: float, v: list[int], v_hat: list[int]):
    n = len(v)
    candidates = list(range(n)) 
    random.shuffle(candidates)

    i_hat = max(range(n), key=lambda i: v_hat[i])
    output = []
    output.append(f"Best predicted candidate is {i_hat} with predicted value {v_hat[i_hat]} and real value {v[i_hat]}")
    output.append("---------------------------------------------")

    mode = "PREDICTION"
    best_so_far = -float("inf")
    hired = None

    arrival_times = {i: random.random() for i in candidates}
    candidates.sort(key=lambda i: arrival_times[i])

    for i in range(n):
        output.append(
            f"Candidate {candidates[i]} arrives at time {arrival_times[candidates[i]]:.3f} "
            f"with value {v[candidates[i]]} and predicted value {v_hat[candidates[i]]}"
        )

    output.append("---------------------------------------------")

    for i in candidates:
        if v[i] >= best_so_far:
            best_so_far = v[i]

        if abs(1 - v_hat[i] / v[i]) > theta:
            output.append(
                f"Switching to SECRETARY mode at candidate {i} "
                f"(predicted value {v_hat[i]}, error={abs(1 - v_hat[i] / v[i]):.3f})"
            )
            mode = "SECRETARY"

        if mode == "PREDICTION" and i == i_hat:
            hired = i
            break

        if mode == "SECRETARY" and arrival_times[i] > tau and v[i] >= best_so_far:
            best_so_far = v[i]
            hired = i
            break

    output.append(f"Hired candidate: {hired}, Value: {v[hired] if hired is not None else None}, Mode: {mode}")
    return "\n".join(output)


# ---------------- Predictions -------------------
def generate_predicted_values(v: list[int], error_rate: float) -> list[int]:
    v_hat = []
    for value in v:
        sigma = error_rate * value
        prediction = value + random.gauss(0, sigma)
        v_hat.append(round(prediction))
    return v_hat



# ---------------- GUI -------------------

def run_algorithm():
    try:
        n = int(entry_n.get())
        tau = float(entry_tau.get())
        theta = float(entry_theta.get())
        error_rate = float(entry_error.get())
    except ValueError:
        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, "Λάθος στις εισόδους.")
        return


    if error_rate < 0:
        error_rate = 0
    if error_rate > 1:
        error_rate = 1

    v = [random.randint(0, 1000) for _ in range(n)]
    v_hat = generate_predicted_values(v, error_rate)

    result = (
        f"Πραγματικές τιμές: {v}\n"
        f"Προβλέψεις: {v_hat}\n\n" +
        learned_Dynkin(tau, theta, v, v_hat)
    )

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, result)


root = tk.Tk()
root.title("Learned Dynkin GUI")

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Πλήθος υποψηφίων (n):").grid(column=0, row=0, sticky="w")
entry_n = ttk.Entry(frm)
entry_n.grid(column=1, row=0)

ttk.Label(frm, text="Cutoff τ:").grid(column=0, row=1, sticky="w")
entry_tau = ttk.Entry(frm)
entry_tau.grid(column=1, row=1)

ttk.Label(frm, text="Ανοχή σφάλματος θ:").grid(column=0, row=2, sticky="w")
entry_theta = ttk.Entry(frm)
entry_theta.grid(column=1, row=2)

ttk.Label(frm, text="Ποσοστό σφάλματος (π.χ. 0.2):").grid(column=0, row=3, sticky="w")
entry_error = ttk.Entry(frm)
entry_error.grid(column=1, row=3)

run_button = ttk.Button(frm, text="Τρέξε", command=run_algorithm)
run_button.grid(column=0, row=4, columnspan=2, pady=10)

result_box = tk.Text(frm, width=80, height=25)
result_box.grid(column=0, row=5, columnspan=2)

root.mainloop()
