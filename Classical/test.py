import random
from learned_dynkin import generate_real_values_uniform, generate_predicted_values_uniform, generate_real_values_adversarial, generate_predicted_values_adversarial, generate_real_values_almost_constant, generate_predicted_values_almost_constant
import plotly.graph_objects as go

def learned_Dynkin(tau : float, theta : float, real_values : list[float], predictions : list[float]):

    n = len(real_values)
    candidates = list(range(n))
    
    random.shuffle(candidates)
    arrival_times = {i: random.random() for i in candidates}
    candidates.sort(key=lambda i: arrival_times[i])

    best_predicted_candidate = max(range(n), key=lambda i: predictions[i]) # best candidate according to predictions

    mode = "PREDICTION"
    best_so_far = -float("inf")
    hired = None

    for i in candidates:
        if abs(1 - predictions[i] / real_values[i]) > theta:
            mode = "SECRETARY"
        if mode == "PREDICTION" and i==best_predicted_candidate:
            hired = i
            break        
        if mode == "SECRETARY" and arrival_times[i] > tau and real_values[i] > best_so_far:
            best_so_far = real_values[i]
            hired = i
            break   
        if (real_values[i] > best_so_far): 
                best_so_far = real_values[i]
    
    return hired


def experiment(n: int, tau: float, theta: float, error_rate: float, runs: int = 1000) -> float:
    competitive_ratio = 0.0
    success = 0

    for _ in range(runs):
        real_values = generate_real_values_adversarial(n)
        predictions = generate_predicted_values_adversarial(real_values, error_rate=error_rate)

        best_real_candidate = max(range(n), key=lambda i: real_values[i]) # best candidate according to real values

        hired = learned_Dynkin(tau, theta, real_values, predictions)

        if hired is not None:
            competitive_ratio += real_values[hired] / real_values[best_real_candidate]
            if hired == best_real_candidate:
                success += 1

    return competitive_ratio / runs, success / runs

if __name__ == "__main__":
    n = int(input("Πόσοι υποψήφιοι; "))

    thresholds = [0.3, 0.5, 0.7]
    tau = 0.313
    error_rates = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    runs = 10000

    fig = go.Figure()

    for theta in thresholds:
        print(f"\n--- Threshold: {theta} ---")

        x_error_rates = []
        y_competitive_ratios = []
        for error_rate in error_rates:
            print(f"\n--- Error rate: {error_rate} ---")
            competitive_ratio, success_rate = experiment(n, tau, theta, error_rate, runs)
            print(f"competitive ratio: {competitive_ratio:.3f} ---- success rate: {success_rate:.3f}")
        
            x_error_rates.append(error_rate)
            y_competitive_ratios.append(competitive_ratio)

        # Γραμμή Competitive Ratio για το συγκεκριμένο theta
        fig.add_trace(go.Scatter(
            x=x_error_rates, 
            y=y_competitive_ratios,
            mode='lines+markers',
            name=f'Comp. Ratio (θ={theta})',
            hovertemplate=f'<b>θ={theta}</b><br>Error: %{{x}}<br>Ratio: %{{y:.3f}}<extra></extra>'
        ))

    # Ρυθμίσεις εμφάνισης 
    fig.update_layout(
        title=f"Σύγκριση Στρατηγικών για το Πρόβλημα του Γραμματέα (n={n}, τ={tau})",
        xaxis_title="Error Rate (Ρυθμός Σφάλματος)",
        yaxis_title="Τιμή / Ποσοστό Επιτυχίας",
        template="plotly_white",
        hovermode="closest" 
    )

    fig.show()