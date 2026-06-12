"""Figures for ch02/series_sum/series_sum.md."""

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
})


# ============================================================
# Figure 1: double_sum_grid.png
# ============================================================
def fig_double_sum_grid():
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    # left: original ordering — m on x-axis, k on y-axis
    ax = axes[0]
    for m in range(1, 10):
        for k in range(m, 11):
            ax.add_patch(mpatches.Rectangle((m - 0.4, k - 0.4), 0.8, 0.8,
                                            fc="#9fc5e8", ec="black", lw=0.6))
    ax.set_xlim(0.3, 9.7); ax.set_ylim(0.3, 10.7)
    ax.set_xticks(range(1, 10)); ax.set_yticks(range(1, 11))
    ax.set_xlabel("m"); ax.set_ylabel("k")
    ax.set_title(r"original: $\sum_{m=1}^{9}\sum_{k=m}^{10}$ — fix m, vary k")
    ax.grid(True, alpha=0.3)

    # right: swapped ordering — k on y-axis, m on x-axis but with reverse
    ax = axes[1]
    for k in range(1, 11):
        for m in range(1, min(k, 9) + 1):
            ax.add_patch(mpatches.Rectangle((m - 0.4, k - 0.4), 0.8, 0.8,
                                            fc="#b6d7a8", ec="black", lw=0.6))
    ax.set_xlim(0.3, 9.7); ax.set_ylim(0.3, 10.7)
    ax.set_xticks(range(1, 10)); ax.set_yticks(range(1, 11))
    ax.set_xlabel("m"); ax.set_ylabel("k")
    ax.set_title(r"swap: for each k, count m ⇒ multiplicity of $k^2$")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT / "double_sum_grid.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    fig_double_sum_grid()
    print(f"figures written to {OUT}")
