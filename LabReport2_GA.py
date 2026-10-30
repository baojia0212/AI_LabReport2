import time
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ---- Fixed GA Parameters  ----
POP_SIZE = 300          # 1) population set up
TARGET_ONES = 50        # 2) optimum when number of ones == 50
CHROM_LEN = 80          # 3) length of every individual
MAX_FITNESS = 80        # 4) return value is 80 when ones == 50
N_GENERATIONS = 50      # 5) number of generations


# ---- Fitness Function ----
def fitness_all(pop: np.ndarray) -> np.ndarray:
    """Fitness = MAX_FITNESS - |ones - TARGET_ONES|; equals 80 when ones == 50."""
    ones = pop.sum(axis=1)
    return MAX_FITNESS - np.abs(ones - TARGET_ONES)


# ---- Genetic Algorithm ----
def evolve(rng, crossover_rate, mutation_rate, tournament_k, on_generation=None):
    pop = rng.integers(0, 2, size=(POP_SIZE, CHROM_LEN), dtype=np.int8)
    best_curve, avg_curve = [], []
    best_ind, best_f, first_opt = None, -np.inf, None

    for gen in range(1, N_GENERATIONS + 1):
        fits = fitness_all(pop)
        i = int(np.argmax(fits))
        best_curve.append(float(fits[i]))
        avg_curve.append(float(fits.mean()))

        if fits[i] > best_f:
            best_f, best_ind = float(fits[i]), pop[i].copy()
        if first_opt is None and fits[i] == MAX_FITNESS:
            first_opt = gen
        if on_generation:
            on_generation(gen, best_curve, avg_curve)
        if gen == N_GENERATIONS:
            break

# --- build next generation ---
        n_pairs = (POP_SIZE + 1) // 2
 
        def select(n):
            idx = rng.integers(0, POP_SIZE, size=(n, tournament_k))
            winners = idx[np.arange(n), np.argmax(fits[idx], axis=1)]
            return pop[winners]
 
        p1, p2 = select(n_pairs), select(n_pairs)
 
        # Single-point crossover
        cut = rng.integers(1, CHROM_LEN, size=n_pairs)
        do_x = rng.random(n_pairs) < crossover_rate
        mask = (np.arange(CHROM_LEN)[None, :] < cut[:, None]) | ~do_x[:, None]
 
        c1 = np.where(mask, p1, p2)
        c2 = np.where(mask, p2, p1)
        children = np.vstack([c1, c2])[:POP_SIZE]
 
        # Bit-flip mutation
        flip = rng.random(children.shape) < mutation_rate
        pop = np.where(flip, 1 - children, children).astype(np.int8)
 
    return best_ind, best_f, best_curve, avg_curve, first_opt

# ---- Streamlit UI ----
st.set_page_config(page_title="Bit Pattern GA", page_icon="🧬", layout="wide")
st.title(f"🧬 Genetic Algorithm: Evolve an {CHROM_LEN}-bit Pattern")
st.caption(
    f"Fitness = {MAX_FITNESS} - |ones - {TARGET_ONES}|  →  maximum fitness {MAX_FITNESS} "
    f"when the number of ones equals {TARGET_ONES}."
)

# Original default hyperparameters
DEFAULTS = {
    "crossover_rate": 0.9,
    "mutation_rate": 0.0125,   # 1 / CHROM_LEN
    "tournament_k": 3,
}
for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)


def reset_defaults():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value


with st.sidebar:
    st.header("🔒 Fixed Condition")
    st.markdown(
        f"- Population: **{POP_SIZE}**\n"
        f"- Chromosome length: **{CHROM_LEN}**\n"
        f"- Target ones: **{TARGET_ONES}**\n"
        f"- Max fitness: **{MAX_FITNESS}**\n"
        f"- Generations: **{N_GENERATIONS}**"
    )
    st.header("🎛️ Hyperparameters")
    crossover_rate = st.slider("Crossover rate", 0.0, 1.0, step=0.05, key="crossover_rate")
    mutation_rate = st.slider("Mutation rate (per bit)", 0.0, 0.1, step=0.0025,
                              format="%.4f", key="mutation_rate")
    tournament_k = st.slider("Tournament size (k)", 2, 10, key="tournament_k")
    st.button("Default", on_click=reset_defaults)
    seed = st.number_input("Random seed", min_value=0, value=42, step=1)

run_btn = st.button("Run Genetic Algorithm", type="primary")

if run_btn:
    rng = np.random.default_rng(int(seed))
    chart_slot, status_slot = st.empty(), st.empty()

    def on_gen(gen, best_curve, avg_curve):
        df = pd.DataFrame(
            {"Best": best_curve, "Average": avg_curve, "Max": [MAX_FITNESS] * len(best_curve)},
            index=range(1, len(best_curve) + 1),
        )
        chart_slot.line_chart(df)
        status_slot.markdown(
            f"Generation **{gen}/{N_GENERATIONS}**: best = **{best_curve[-1]:.0f}**, "
            f"average = {avg_curve[-1]:.2f}"
        )
        time.sleep(0.05)

    best_ind, best_f, best_curve, avg_curve, first_opt = evolve(
        rng, crossover_rate, mutation_rate, tournament_k, on_gen
    )
    chart_slot.empty()
    status_slot.empty()
    st.session_state["result"] = dict(
        best_ind=best_ind, best_f=best_f, best_curve=best_curve,
        avg_curve=avg_curve, first_opt=first_opt,
    )

res = st.session_state.get("result")
if res:
    ones = int(res["best_ind"].sum())
    bitstring = "".join(map(str, res["best_ind"].tolist()))

    st.subheader("🏁 Best Individual Found")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Best fitness", f"{res['best_f']:.0f}")
    m2.metric("Ones", ones)
    m3.metric("Zeros", CHROM_LEN - ones)
    m4.metric("Optimum first found at gen", res["first_opt"] if res["first_opt"] else "not reached")
    st.code(bitstring, language="text")

    st.subheader("📈 Convergence")
    fig, ax = plt.subplots(figsize=(8, 4))
    gens = range(1, len(res["best_curve"]) + 1)
    ax.plot(gens, res["best_curve"], linewidth=2, label="Best")
    ax.plot(gens, res["avg_curve"], linewidth=2, linestyle="--", label="Average")
    ax.axhline(MAX_FITNESS, color="green", linestyle=":", label=f"Max = {MAX_FITNESS}")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.set_title("GA Convergence")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    st.pyplot(fig)

    if res["best_f"] == MAX_FITNESS and ones == TARGET_ONES:
        st.success(f"Perfect match achieved: ones = {TARGET_ONES} and fitness = {MAX_FITNESS} ✅")
    else:
        st.info("Near-optimal solution found; try another seed or adjust the hyperparameters.")

    hist_df = pd.DataFrame({"generation": range(1, len(res["best_curve"]) + 1),
                            "best": res["best_curve"], "average": res["avg_curve"]})
    st.download_button("⬇️ Download convergence (CSV)", hist_df.to_csv(index=False),
                       "convergence.csv", "text/csv")