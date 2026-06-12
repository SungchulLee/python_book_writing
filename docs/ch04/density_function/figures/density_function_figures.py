"""Figures for ch04/density_function/density_function.md."""

# ============================================================
# Imports & style
# ============================================================
import matplotlib.pyplot as plt
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
# Figure 1: density_area.png
# ============================================================
def fig_density_area():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # left: f(x) = 3/4 x(2-x) shaded over [0,1]
    ax = axes[0]
    x = np.linspace(0, 2, 200)
    f = 0.75 * x * (2 - x)
    ax.plot(x, f, "b-", lw=2)
    xfill = np.linspace(0, 1, 100)
    ax.fill_between(xfill, 0.75 * xfill * (2 - xfill), alpha=0.4, color="orange",
                    label=r"$P(0 \leq X \leq 1) = 0.5$")
    ax.set_xlabel("x"); ax.set_ylabel(r"$f(x)$")
    ax.set_title(r"$f(x) = \frac{3}{4} x(2 - x)$ — area = probability")
    ax.legend(fontsize=10)
    ax.set_xlim(-0.1, 2.1); ax.set_ylim(0, 1)

    # right: full area = 1
    ax = axes[1]
    ax.plot(x, f, "b-", lw=2)
    ax.fill_between(x, f, alpha=0.4, color="lightblue",
                    label=r"total area $= \int_0^2 f \, dx = 1$")
    ax.set_xlabel("x"); ax.set_ylabel(r"$f(x)$")
    ax.set_title("normalization condition")
    ax.legend(fontsize=10)
    ax.set_xlim(-0.1, 2.1); ax.set_ylim(0, 1)

    fig.tight_layout()
    fig.savefig(OUT / "density_area.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Figure 2: piecewise_density.png
# ============================================================
def fig_piecewise_density():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    for ax, b, title in [(axes[0], 0.5, "b = 0.5"),
                         (axes[1], 5.0, "b = 5")]:
        a = 2 / (2*b + 3)
        x1 = np.linspace(0, 1, 100)
        x2 = np.linspace(1, 2, 100)
        f1 = a * (b * x1 + 1)
        f2 = -a * (b + 1) * (x2 - 2)
        ax.plot(x1, f1, "b-", lw=2)
        ax.plot(x2, f2, "g-", lw=2)
        ax.fill_between(x1, f1, alpha=0.3, color="b")
        ax.fill_between(x2, f2, alpha=0.3, color="g")
        ax.scatter([1], [a*(b+1)], color="red", s=40, zorder=3)
        ax.set_xlabel("x"); ax.set_ylabel(r"$f(x)$")
        ax.set_title(f"piecewise density ({title}), a = {a:.3f}")
        ax.set_xlim(-0.1, 2.1)

    fig.tight_layout()
    fig.savefig(OUT / "piecewise_density.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    fig_density_area()
    fig_piecewise_density()
    print(f"figures written to {OUT}")
