"""Figures for ch04/repetition_counting/repetition_counting.md.

Visualizations of stars-and-bars for repetition combinations and the
symmetry x -> 9-x for digit-sum problems.
"""

# ============================================================
# Imports & global style
# ============================================================
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 140,
})


# ============================================================
# Figure 1: stars_and_bars.png
# ============================================================
def fig_stars_and_bars():
    fig, axes = plt.subplots(2, 1, figsize=(11, 5.5))

    # Top: one example for n=4, r=5, arrangement *** | * | | *
    ax = axes[0]
    ax.set_xlim(0, 12); ax.set_ylim(-0.5, 1.5)
    ax.axis("off")
    # ★★★ | ★ | | ★
    seq = ["S", "S", "S", "B", "S", "B", "B", "S"]
    x = 1.0
    for tok in seq:
        if tok == "S":
            ax.text(x, 0.5, r"$\bigstar$", fontsize=22, ha="center", va="center", color="#d62728")
        else:
            ax.plot([x, x], [0, 1], "k-", lw=3)
        x += 1.0
    ax.text(6, 1.4, r"$n = 4$ groups, $r = 5$ items: pick $n-1 = 3$ bar positions among $n + r - 1 = 8$ slots",
            ha="center", fontsize=10)
    ax.text(6, -0.3, r"each pattern corresponds to a solution of $x_1 + x_2 + x_3 + x_4 = 5$, $x_i \geq 0$",
            ha="center", fontsize=10, color="gray")

    # Bottom: count as binomial
    ax = axes[1]
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.axis("off")
    formula = (
        r"$_n\mathrm{H}_r \;=\; \binom{n + r - 1}{r} \;=\; \binom{n + r - 1}{n - 1}$"
    )
    ax.text(5, 4.5, formula, ha="center", fontsize=18)
    ax.text(5, 2.5,
            r"$_4\mathrm{H}_5 = \binom{8}{5} = \binom{8}{3} = 56$",
            ha="center", fontsize=15, color="#2ca02c")
    ax.text(5, 1.0,
            "number of nonneg-integer solutions of $x_1+x_2+x_3+x_4=5$",
            ha="center", fontsize=10, color="gray")

    fig.tight_layout()
    fig.savefig(OUT / "stars_and_bars.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Figure 2: digit_sum_transform.png
# ============================================================
def fig_digit_sum_transform():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # Left: original problem — sum = 38 with five digits in [0,9]
    ax = axes[0]
    # sample digits totaling 38: 9,9,9,9,2
    digits = [9, 9, 9, 9, 2]
    for i, d in enumerate(digits):
        rect = mpatches.Rectangle((i, 0), 0.9, d / 9, color="#1f77b4", alpha=0.6)
        ax.add_patch(rect)
        ax.text(i + 0.45, d/9 + 0.05, str(d), ha="center", fontsize=12)
    ax.text(2.45, 1.4, "sum = 38", ha="center", fontsize=12, color="red")
    ax.set_xlim(-0.3, 5.3); ax.set_ylim(0, 1.7)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(r"original: $\alpha + \beta + \gamma + \delta + \epsilon = 38$")

    # Right: transformed
    ax = axes[1]
    digits1 = [9 - d for d in digits]
    for i, d in enumerate(digits1):
        rect = mpatches.Rectangle((i, 0), 0.9, d / 9 if d > 0 else 0.03, color="#2ca02c", alpha=0.6)
        ax.add_patch(rect)
        ax.text(i + 0.45, (d/9 if d > 0 else 0.03) + 0.05, str(d), ha="center", fontsize=12)
    ax.text(2.45, 1.4, "sum = 7", ha="center", fontsize=12, color="red")
    ax.set_xlim(-0.3, 5.3); ax.set_ylim(0, 1.7)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(r"after $x \to 9 - x$: sum becomes $7$")

    fig.tight_layout()
    fig.savefig(OUT / "digit_sum_transform.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    fig_stars_and_bars()
    fig_digit_sum_transform()
    print(f"figures written to {OUT}")
