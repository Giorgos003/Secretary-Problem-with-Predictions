import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import math
import heapq
from Kleinberg import secretary_kleinberg
from Generate_Values.real_values import generate_real_values_uniform, generate_real_values_adversarial, generate_real_values_almost_constant
from Generate_Values.predictions import generate_predicted_values_uniform, generate_predicted_values_adversarial, generate_predicted_values_almost_constant


# ---------------- Learned Kleinberg Algorithm -------------------

def learned_kleinberg(threshold: int, k: int, predictions: list[float], values: list[float]):
    n = len(predictions)
    predicted_S = heapq.nlargest(k, range(n), key=lambda i: predictions[i])

    log = []
    log.append(f"Predicted top {k} candidates: {predicted_S} \n")
    S = [] 
    
    for i in range(n):
        if math.fabs(1 - predictions[i] / values[i]) > threshold:
            log.append(f"Switching to Kleinberg's algorithm at candidate {i} (predicted value {predictions[i]}, real value {values[i]}, error {math.fabs(1 - predictions[i] / values[i]):.3f})")
            k = k - len(S) - 1  
            S.append(i) 

            remaining_candidates = predictions[i+1:]
            log.append(f"Remaining candidates for Kleinberg's algorithm: {remaining_candidates}, k = {k}")
            hired_candidates = secretary_kleinberg(remaining_candidates, k)
            for hired_candidate in hired_candidates:
                S.append(hired_candidate + i + 1) 
            return S, log
        
        if i in predicted_S:
            S.append(i)
            if len(S) == k:
                return S, log
    return S, log



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

        ttk.Label(frame, text="Number of candidates to hire:").grid(row=1, column=0, sticky="w")
        self.hires_entry = ttk.Entry(frame)
        self.hires_entry.insert(0, "2")
        self.hires_entry.grid(row=1, column=1)

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
            k = int(self.hires_entry.get())
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
            real_values = generate_real_values_almost_constant(n, error_rate=error_rate, k=k)
            predictions = generate_predicted_values_almost_constant(real_values)

        hired, log = learned_kleinberg(theta, k, predictions, real_values)

        log.append(f"Final hired candidates: {hired} with real values {[real_values[i] for i in hired]}")

        self.output.delete(1.0, tk.END)
        for i in range(len(real_values)):
            self.output.insert(tk.END, f"candidate {i}: real value = {real_values[i]}, prediction = {predictions[i]}\n")

        self.output.insert(tk.END, "\n")

        for line in log:
            self.output.insert(tk.END, line + "\n")




# ---------------- MAIN ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

