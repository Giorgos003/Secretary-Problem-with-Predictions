import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
from learned_dynkin import generate_real_values_uniform, generate_predicted_values_uniform, generate_real_values_adversarial, generate_predicted_values_adversarial, generate_real_values_almost_constant, generate_predicted_values_almost_constant



def learned_Dynkin(tau : float, theta : float, real_values : list[float], predictions : list[float]):

    n = len(real_values)
    candidates = list(range(n))
    
    random.shuffle(candidates)
    arrival_times = {i: random.random() for i in candidates}
    candidates.sort(key=lambda i: arrival_times[i])

    log = []
    for i in range(n):
        log.append(f"Candidate {candidates[i]} arrives at time {arrival_times[candidates[i]]:.6f} with value {real_values[candidates[i]]} and predicted value {predictions[candidates[i]]}")
    log.append("---------------------------------------------")

    best_predicted_value = max(range(n), key=lambda i: predictions[i])
    best_real_value = max(range(n), key=lambda i: real_values[i])
    log.append(f"Best predicted candidate is {best_predicted_value} with predicted value {predictions[best_predicted_value]} and real value {real_values[best_predicted_value]} and arrived at time {arrival_times[best_predicted_value]:.6f}")
    log.append(f"Best real candidate is {best_real_value} with real value {real_values[best_real_value]} and predicted value {predictions[best_real_value]} and arrived at time {arrival_times[best_real_value]:.6f}")
    log.append("---------------------------------------------")

    mode = "PREDICTION"
    best_so_far = -float("inf")
    hired = None

    for i in candidates:
        if abs(1 - predictions[i] / real_values[i]) > theta:
            log.append(f"Switching to SECRETARY mode at candidate {i} (predicted value {predictions[i]}, {abs(1 - predictions[i] / real_values[i]):.3f} > {theta}) and arrived at time {arrival_times[i]:.6f} where τ={tau}")
            mode = "SECRETARY"
        if mode == "PREDICTION" and i==best_predicted_value:
            hired = i
            break        
        if mode == "SECRETARY" and arrival_times[i] > tau and real_values[i] > best_so_far:
            best_so_far = real_values[i]
            hired = i
            break   
        if (real_values[i] > best_so_far): 
                best_so_far = real_values[i]
    
    log.append(f"Hired candidate: {hired}, Value: {real_values[hired] if hired is not None else None}, Mode: {mode}")
    return hired, log




# ---------------- UI ----------------

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Learned Dynkin Simulator")
        self.root.geometry("800x600")

        frame = ttk.Frame(root, padding=10)
        frame.pack(fill="x")

        ttk.Label(frame, text="Number of candidates:").grid(row=0, column=0, sticky="w")
        self.n_entry = ttk.Entry(frame)
        self.n_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Tau:").grid(row=1, column=0, sticky="w")
        self.tau_entry = ttk.Entry(frame)
        self.tau_entry.insert(0, "0.313")
        self.tau_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Theta:").grid(row=2, column=0, sticky="w")
        self.theta_entry = ttk.Entry(frame)
        self.theta_entry.insert(0, "0.646")
        self.theta_entry.grid(row=2, column=1)

        ttk.Label(frame, text="Error rate:").grid(row=3, column=0, sticky="w")
        self.error_rate_entry = ttk.Entry(frame)
        self.error_rate_entry.insert(0, "0.7")
        self.error_rate_entry.grid(row=3, column=1)

        distr_label = tk.Label(frame, text="Distribution Mode")
        distr_label.grid(row=4, column=0, sticky="w", padx=15, pady=10)

        self.distr_var = tk.StringVar(value="Uniform")

        distr_dropdown = ttk.Combobox(
            frame,
            textvariable=self.distr_var,
            values=["Uniform", "Adversarial", "Almost Constant"],
            state="readonly",
        )
        distr_dropdown.grid(row=4, column=1, sticky="w", padx=15, pady=10)

        run_btn = ttk.Button(frame, text="Run Simulation", command=self.run)
        run_btn.grid(row=5, column=0, columnspan=2, pady=10)

        frame_output = ttk.Frame(root)
        frame_output.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(frame_output)
        scrollbar.pack(side="right", fill="y")

        self.output = tk.Text(frame_output, wrap="word", yscrollcommand=scrollbar.set)
        self.output.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.output.yview)

    def run(self):
        try:
            n = int(self.n_entry.get())
            tau = float(self.tau_entry.get())
            theta = float(self.theta_entry.get())
            error_rate = float(self.error_rate_entry.get())
            distribution_mode = self.distr_var.get()
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
            return

        if distribution_mode == "Uniform":
            # Uniformly distributed values and predictions
            print("\n--- Uniformly distributed values and predictions ---")
            real_values = generate_real_values_uniform(n)
            predictions = generate_predicted_values_uniform(real_values, error_rate=error_rate)
        elif distribution_mode == "Adversarial":
            # Adversarially distributed values and predictions
            print("\n--- Adversarially distributed values and predictions ---")
            real_values = generate_real_values_adversarial(n)
            predictions = generate_predicted_values_adversarial(real_values, error_rate=error_rate)
        elif distribution_mode == "Almost Constant":
            # Almost constant values and predictions
            print("\n--- Almost constant values and predictions ---")
            real_values = generate_real_values_almost_constant(n, error_rate=error_rate, k=1) # r takes the k value, where is one for classical secretary problem
            predictions = generate_predicted_values_almost_constant(real_values)

        hired, log = learned_Dynkin(tau, theta, real_values, predictions)

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"Real values: {real_values}\n")
        self.output.insert(tk.END, f"Predictions: {predictions}\n\n")

        for line in log:
            self.output.insert(tk.END, line + "\n")

# ---------------- MAIN ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

