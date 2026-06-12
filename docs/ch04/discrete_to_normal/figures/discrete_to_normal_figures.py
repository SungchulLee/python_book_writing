"""Figures for discrete_to_normal.md.

Generates PNGs in this directory:

- ``example1_conditional.png``    : tree diagram of conditional probability
  with two stages and three outcomes.
- ``example2_binomial_normal.png``: a Bin(m, p) distribution overlaid with
  its normal approximation for m = 288, p = 7/12.
- ``exercise1_trajectory.png``    : two example trajectories of the score
  sequence X_n showing how X grows then resets to 0.
- ``exercise1_X2_distribution.png``: bar chart of P(X_2 = k) for k = 0, 1, 2.
- ``exercise2_X3_zero.png``       : how P(X_3 = 0) decomposes by the previous
  state X_2 (law of total probability).
- ``exercise3_binom_variance.png``: V(Y) and V(2Y+3) as a function of m for
  Y ~ Bin(m, 7/12), showing V(2Y+3) = 280 at m = 288.
- ``exercise4_normal_tail.png``   : normal distribution N(333, 280) with
  shaded right tail P(Z ≥ 0) = 0.5, corresponding to a = 333.

Run with ``python discrete_to_normal_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from scipy.stats import binom, norm


# ===
# Figure 1 — Conditional probability tree
# ===


def make_conditional(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.5))

    # Stage 0 (root)
    ax.plot(0, 0, "o", color="black", markersize=10)
    ax.annotate(r"$X_0 = 0$", (0, 0), xytext=(-30, -8), textcoords="offset points", fontsize=13)

    # Stage 1 — two children
    ax.plot(2, 1.5, "o", color="tab:blue", markersize=10)
    ax.annotate(r"$X_1 = 1$  ($A_1$)", (2, 1.5), xytext=(10, 0),
                textcoords="offset points", fontsize=11, color="tab:blue")
    ax.plot(2, -1.5, "o", color="tab:red", markersize=10)
    ax.annotate(r"$X_1 = 0$  ($B_1$)", (2, -1.5), xytext=(10, 0),
                textcoords="offset points", fontsize=11, color="tab:red")

    ax.plot([0, 2], [0, 1.5], color="tab:blue", linewidth=1.5)
    ax.plot([0, 2], [0, -1.5], color="tab:red", linewidth=1.5)
    ax.annotate(r"$P(A_1) = 1/2$", (0.9, 1.0), fontsize=10, color="tab:blue")
    ax.annotate(r"$P(B_1) = 1/2$", (0.9, -1.0), fontsize=10, color="tab:red")

    # Stage 2 — four children (from each Stage 1 node)
    # From X_1 = 1:
    ax.plot(4.5, 2.3, "o", color="tab:blue", markersize=10)
    ax.annotate(r"$X_2 = 2$", (4.5, 2.3), xytext=(10, 0),
                textcoords="offset points", fontsize=11, color="tab:blue")
    ax.plot(4.5, 0.7, "o", color="tab:red", markersize=10)
    ax.annotate(r"$X_2 = 0$", (4.5, 0.7), xytext=(10, 0),
                textcoords="offset points", fontsize=11, color="tab:red")
    ax.plot([2, 4.5], [1.5, 2.3], color="tab:blue", linewidth=1.2)
    ax.plot([2, 4.5], [1.5, 0.7], color="tab:red", linewidth=1.2)
    ax.annotate(r"$1/3$", (3, 2.1), fontsize=10, color="tab:blue")
    ax.annotate(r"$2/3$", (3, 0.85), fontsize=10, color="tab:red")

    # From X_1 = 0:
    ax.plot(4.5, -0.7, "o", color="tab:blue", markersize=10)
    ax.annotate(r"$X_2 = 1$", (4.5, -0.7), xytext=(10, 0),
                textcoords="offset points", fontsize=11, color="tab:blue")
    ax.plot(4.5, -2.3, "o", color="tab:red", markersize=10)
    ax.annotate(r"$X_2 = 0$", (4.5, -2.3), xytext=(10, 0),
                textcoords="offset points", fontsize=11, color="tab:red")
    ax.plot([2, 4.5], [-1.5, -0.7], color="tab:blue", linewidth=1.2)
    ax.plot([2, 4.5], [-1.5, -2.3], color="tab:red", linewidth=1.2)
    ax.annotate(r"$1/2$", (3, -0.85), fontsize=10, color="tab:blue")
    ax.annotate(r"$1/2$", (3, -2.1), fontsize=10, color="tab:red")

    ax.set_xlim(-1.5, 7.5)
    ax.set_ylim(-3.2, 3.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(r"Conditional probability tree for the score sequence $X_n$", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 2 — Binomial + Normal approximation
# ===


def make_binomial_normal(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))

    m, p = 288, 7 / 12
    ks = np.arange(140, 200)
    pmf = binom.pmf(ks, m, p)

    ax.bar(ks, pmf, color="tab:blue", alpha=0.6, label=rf"Bin($m={m}$, $p=7/12$)")

    # Normal approximation
    mu = m * p  # 168
    sigma2 = m * p * (1 - p)  # 70
    sigma = np.sqrt(sigma2)
    xs = np.linspace(140, 200, 300)
    pdf = norm.pdf(xs, mu, sigma)
    ax.plot(xs, pdf, color="tab:red", linewidth=2.5, label=rf"$N(\mu={mu:.0f},\,\sigma^2={sigma2:.0f})$")

    ax.set_xlabel(r"$Y$  (number of successes)", fontsize=11)
    ax.set_ylabel("Probability", fontsize=11)
    ax.set_title(rf"Bin($m={m},\,p=7/12$) and its normal approximation", fontsize=12)
    ax.legend(loc="upper right", fontsize=11)
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 3 — Two sample trajectories of X_n
# ===


def make_trajectory(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))

    # Simulate two trajectories
    np.random.seed(42)
    n_steps = 20

    def _sim():
        X = [0]
        for _ in range(n_steps):
            x = X[-1]
            p_A = 1 / (x + 2)
            if np.random.rand() < p_A:
                X.append(x + 1)
            else:
                X.append(0)
        return X

    traj1 = _sim()
    traj2 = _sim()

    ax.plot(range(len(traj1)), traj1, "-o", color="tab:blue", linewidth=1.8,
            markersize=7, label="trajectory 1")
    ax.plot(range(len(traj2)), traj2, "-s", color="tab:red", linewidth=1.8,
            markersize=7, label="trajectory 2")

    ax.set_xlabel(r"$n$  (step)", fontsize=11)
    ax.set_ylabel(r"$X_n$  (score)", fontsize=11)
    ax.set_title(r"Two example trajectories of $X_n$ — grows by $+1$ or resets to $0$", fontsize=12)
    ax.legend(loc="upper right", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 4 — Distribution of X_2
# ===


def make_X2_distribution(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))

    ks = [0, 1, 2]
    probs = [7 / 12, 1 / 4, 1 / 6]
    colors = ["tab:red", "tab:blue", "tab:green"]

    bars = ax.bar(ks, probs, color=colors, width=0.6)

    for k, p, c in zip(ks, probs, colors):
        ax.annotate(rf"$\frac{{{['7','3','2'][k]}}}{{12}}$" if False
                    else rf"${['7/12','1/4','1/6'][k]}$",
                    (k, p), xytext=(0, 8), textcoords="offset points",
                    fontsize=14, color=c, ha="center", weight="bold")

    # Sum check
    ax.annotate(r"sum $= \frac{7}{12} + \frac{3}{12} + \frac{2}{12} = 1$",
                (1, 0.5), fontsize=11, ha="center", style="italic")

    ax.set_xticks(ks)
    ax.set_xlabel(r"$X_2$", fontsize=12)
    ax.set_ylabel(r"$P(X_2 = k)$", fontsize=12)
    ax.set_ylim(0, 0.7)
    ax.set_title(r"Distribution of $X_2$:  $P(X_2 = 0, 1, 2) = (7/12,\;1/4,\;1/6)$", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 5 — Decomposition of P(X_3 = 0)
# ===


def make_X3_zero(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))

    # Each P(X_2 = k) goes to P(X_3 = 0) with probability (k+1)/(k+2)
    ks = [0, 1, 2]
    pX2 = [7 / 12, 1 / 4, 1 / 6]
    cond = [1 / 2, 2 / 3, 3 / 4]
    contrib = [a * b for a, b in zip(pX2, cond)]

    width = 0.35
    x = np.arange(len(ks))

    ax.bar(x - width / 2, pX2, width, color="lightblue", label=r"$P(X_2 = k)$")
    ax.bar(x + width / 2, contrib, width, color="tab:red", alpha=0.7,
           label=r"$P(X_2 = k) \cdot P(B_3 \mid X_2 = k)$")

    for i, (k, c) in enumerate(zip(ks, contrib)):
        ax.annotate(rf"${['7/24','1/6','1/8'][i]}$", (i + width / 2, c),
                    xytext=(0, 5), textcoords="offset points",
                    fontsize=11, color="tab:red", ha="center")

    ax.set_xticks(x)
    ax.set_xticklabels(ks)
    ax.set_xlabel(r"$k = X_2$", fontsize=11)
    ax.set_ylabel("Probability", fontsize=11)
    ax.set_title(r"$P(X_3 = 0) = \sum_k P(X_2 = k)\,P(B_3 \mid X_2 = k) = 7/12$", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 6 — V(2Y+3) as function of m
# ===


def make_binom_variance(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    p = 7 / 12
    ms = np.arange(1, 400)
    V_Y = ms * p * (1 - p)
    V_2Y3 = 4 * V_Y

    ax.plot(ms, V_Y, color="tab:blue", linewidth=2, label=r"$V(Y) = m \cdot \frac{7}{12} \cdot \frac{5}{12}$")
    ax.plot(ms, V_2Y3, color="tab:red", linewidth=2, label=r"$V(2Y + 3) = 4\,V(Y) = \frac{35 m}{36}$")

    # Mark m = 288 where V(2Y+3) = 280
    ax.axhline(280, color="gray", linewidth=0.7, linestyle="--")
    ax.axvline(288, color="gray", linewidth=0.7, linestyle="--")
    ax.plot(288, 280, "o", color="tab:red", markersize=10)
    ax.annotate(r"$m = 288,\;V(2Y + 3) = 280$", (288, 280),
                xytext=(15, -30), textcoords="offset points", fontsize=11, color="tab:red",
                arrowprops=dict(arrowstyle="->", color="tab:red"))

    ax.set_xlabel(r"$m$", fontsize=11)
    ax.set_ylabel("Variance", fontsize=11)
    ax.set_title(r"Variance of $Y \sim \text{Bin}(m, 7/12)$ and of $2Y + 3$", fontsize=12)
    ax.legend(loc="upper left", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 7 — Normal tail at 0.5
# ===


def make_normal_tail(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    mu = 333
    sigma = np.sqrt(280)
    xs = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 400)
    pdf = norm.pdf(xs, mu, sigma)

    ax.plot(xs, pdf, color="tab:blue", linewidth=2.2)
    # Shade right half (≥ μ)
    mask = xs >= mu
    ax.fill_between(xs[mask], pdf[mask], alpha=0.35, color="tab:red",
                    label=r"$P(2Y - 3 \geq a) = 0.5$")

    # Mark a = 333
    ax.axvline(333, color="tab:red", linewidth=1.5, linestyle="--")
    ax.annotate(r"$a = 333$ (= $\mu$)", (333, 0.005),
                xytext=(15, 30), textcoords="offset points", fontsize=12, color="tab:red",
                arrowprops=dict(arrowstyle="->", color="tab:red"))

    ax.set_xlabel(r"$2Y - 3$", fontsize=11)
    ax.set_ylabel("Density", fontsize=11)
    ax.set_title(r"$2Y - 3 \approx N(333,\,280)$:  $P(2Y - 3 \geq a) = 0.5 \Rightarrow a = 333$", fontsize=11)
    ax.legend(loc="upper right", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Entry point
# ===

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    make_conditional(out_dir / "example1_conditional.png")
    make_binomial_normal(out_dir / "example2_binomial_normal.png")
    make_trajectory(out_dir / "exercise1_trajectory.png")
    make_X2_distribution(out_dir / "exercise1_X2_distribution.png")
    make_X3_zero(out_dir / "exercise2_X3_zero.png")
    make_binom_variance(out_dir / "exercise3_binom_variance.png")
    make_normal_tail(out_dir / "exercise4_normal_tail.png")
    print(f"Wrote figures to {out_dir}")
