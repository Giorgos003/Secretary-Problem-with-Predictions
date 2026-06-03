import numpy as np
import random
import math
import plotly.graph_objects as go

# This function implements the classical Dynkin's algorithm for the Secretary problem but with a small change.
# If the algorithm fails to hire the best canditate, it returns None instead of the hired candidate index. This allows us to easily calculate the success rate of the algorithm in our experiments.
def secretary_dynkin(values: list[float], arrival_times: list[float], threshold: float) -> int | None:
    n = len(values)

    # Sort candidates by their arrival times
    candidates = list(range(n))
    candidates.sort(key=lambda i: arrival_times[i])

    # for i in candidates:
    #     print(f"Candidate {i} arrives at time {arrival_times[i]} with value {values[i]}")

    best_so_far = -float("inf") 

    best_candidate = max(range(n), key=lambda i: values[i])

    for candidate in candidates:
        if arrival_times[candidate] < threshold:
            if values[candidate] > best_so_far:
                best_so_far = values[candidate]
        else:
            if values[candidate] > best_so_far:
                hired = candidate
                if hired == best_candidate:
                    # print(f"Hired the best candidate: {hired}, Value: {values[hired]}, Arrival time: {arrival_times[hired]}")
                    return hired
                else:
                    return None
        
    return None




def generate_real_values_uniform(n: int) -> list[float]:
    values = []
    for i in range(n):
        value = np.random.exponential(scale=1)
        values.append(value)
    return values



def experiment(threshold, runs=1000):
    success = 0

    for _ in range(runs):
        if secretary_dynkin(generate_real_values_uniform(n), [random.random() for _ in range(n)], threshold) is not None:
            success += 1

    print(f"Threshold: {threshold:.2f}, Successes: {success}")
    return success / runs

if __name__ == "__main__":
    n = int(input("Number of candidates: "))

    thresholds = [0.1, 0.2, 0.3, 0.368, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    runs = 10000

    x_thresholds = []
    y_success_rates = []

    for t in thresholds:
        success_rate = experiment(t, runs)

        print(f"t={t:.3f} → success={success_rate:.3f}")
        x_thresholds.append(t)
        y_success_rates.append(success_rate)

    fig = go.Figure()

    # Προσθήκη της καμπύλης για το success rate
    fig.add_trace(go.Scatter(
        x=x_thresholds,
        y=y_success_rates,
        mode='lines+markers',
        name='Πειραματική Επιτυχία',
        line=dict(color='blue', width=3),
        marker=dict(size=8)
    ))

    # Προσθήκη της κάθετης κόκκινης γραμμής στο 1/e 
    fig.add_vline(
        x=0.368, 
        line_dash="dash", 
        line_color="red", 
        annotation_text="Θεωρητικό Βέλτιστο (1/e)",
        annotation_position="top left"
    )

    # Ρυθμίσεις εμφάνισης
    fig.update_layout(
        title=f"Κλασικό Πρόβλημα του Γραμματέα (n={n}, runs={runs})",
        xaxis_title="Κατώφλι τ",
        yaxis_title="Ποσοστό Επιτυχίας (Success Rate)",
        template="plotly_white",
        hovermode="x"
    )

    fig.show()