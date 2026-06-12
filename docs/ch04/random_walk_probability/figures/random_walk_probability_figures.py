"""Figures for ch04/random_walk_probability/random_walk_probability.md."""

# ============================================================
# Imports & style
# ============================================================
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 140,
    "axes.grid": True,
    "grid.alpha": 0.25,
})


# ============================================================
# Figure 1: walk_setup.png
# ============================================================
def fig_walk_setup():
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.set_xlim(-0.5, 4.0); ax.set_ylim(-1.5, 1.5)
    ax.axis("off")
    # four points
    xs = [0, 1, 2, 3]
    for i, x in enumerate(xs):
        ax.scatter([x], [0], s=200, color="black", zorder=3)
        ax.text(x, -0.5, f"point {i+1}", ha="center", fontsize=10)
    ax.plot([0, 3], [0, 0], "k-", lw=1.5, zorder=1)

    # start marker
    ax.scatter([0], [0], s=400, color="red", zorder=4)
    ax.text(0, 0.4, "start", ha="center", color="red", fontsize=11, weight="bold")
    ax.text(3, 0.4, "goal (right end)", ha="center", color="green", fontsize=10, weight="bold")

    # transition arrow
    ax.annotate("", xy=(0.85, 0.15), xytext=(0.15, 0.15),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="blue"))
    ax.text(0.5, 0.4, "head (prob p)", ha="center", color="blue", fontsize=9)

    # stay arrow
    ax.annotate("", xy=(0.15, -0.3), xytext=(0.05, -0.5),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="orange",
                                connectionstyle="arc3,rad=0.5"))
    ax.text(0.0, -1.0, "tail (prob 1-p): stay", ha="left", color="orange", fontsize=9)

    ax.set_title("random walk model — 4 points, coin-toss step")

    fig.savefig(OUT / "walk_setup.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Figure 2: f_eq_g.png — f(p) and g(p) curves
# ============================================================
def fig_f_eq_g():
    fig, ax = plt.subplots(figsize=(8, 5))
    p = np.linspace(0.01, 1, 200)
    f = p**2 * (3*p**2 - 8*p + 6)
    g1 = p * (2 - p)
    g2 = p**2 * (3 - 2*p)
    g = (4/5) * g1 + (1/5) * g2
    ax.plot(p, f, "b-", lw=2, label=r"$f(p) = p^2(3p^2 - 8p + 6)$")
    ax.plot(p, g, "r-", lw=2, label=r"$g(p) = \frac{p}{5}(-2p^2 - p + 8)$")
    # mark intersection at p = 8/15
    p_star = 8/15
    f_star = p_star**2 * (3*p_star**2 - 8*p_star + 6)
    ax.scatter([p_star], [f_star], color="green", s=80, zorder=4)
    ax.axvline(p_star, color="green", ls=":", lw=1.0)
    ax.text(p_star + 0.02, f_star, fr"$p = 8/15 \approx {p_star:.3f}$",
            fontsize=11, color="green", va="center")
    # intersection at p = 1
    ax.scatter([1], [1], color="green", s=80, zorder=4)
    ax.set_xlabel("p (probability of head)")
    ax.set_ylabel("probability of reaching goal")
    ax.set_title(r"$f(p) = g(p)$ — solutions at $p = 8/15$ and $p = 1$")
    ax.legend(fontsize=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.05)

    fig.tight_layout()
    fig.savefig(OUT / "f_eq_g.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    fig_walk_setup()
    fig_f_eq_g()
    print(f"figures written to {OUT}")
