"""Figures for ch02/sequence_limit/sequence_limit.md.

Generates PNGs for the sequence-limit topic: parabola/line area,
conjugate pair (2+√3)^n, and the (β−α) → 1/6 formula visual.
"""

# ============================================================
# Imports & global style
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
# Figure 1: area_difference.png — the 1/6 formula visual
# ============================================================
def fig_area_difference():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    x = np.linspace(-1.5, 3.5, 400)

    # left: y = x^2 and y = x + 1
    ax = axes[0]
    a_val, k_val = 1.0, 1.0
    ax.plot(x, x**2, "b-", lw=2, label=r"$y = x^2$")
    ax.plot(x, a_val * x + k_val, "r-", lw=2, label=r"$y = ax + k$")
    alpha = (a_val - np.sqrt(a_val**2 + 4*k_val)) / 2
    beta  = (a_val + np.sqrt(a_val**2 + 4*k_val)) / 2
    xf = np.linspace(alpha, beta, 200)
    ax.fill_between(xf, xf**2, a_val*xf + k_val, color="orange", alpha=0.35)
    ax.axvline(alpha, color="gray", ls=":", lw=0.8)
    ax.axvline(beta,  color="gray", ls=":", lw=0.8)
    ax.text(alpha, -0.5, r"$\alpha$", ha="center", fontsize=12)
    ax.text(beta,  -0.5, r"$\beta$",  ha="center", fontsize=12)
    ax.set_title(r"Area $= \frac{1}{6}(\beta - \alpha)^3$")
    ax.set_xlim(-1.5, 3); ax.set_ylim(-1, 7)
    ax.legend(loc="upper left", fontsize=9)

    # right: same area as a function of (β - α)
    ax = axes[1]
    d = np.linspace(0, 4, 200)
    ax.plot(d, d**3 / 6, "g-", lw=2)
    ax.set_xlabel(r"$\beta - \alpha$")
    ax.set_ylabel("enclosed area")
    ax.set_title("area grows like cube of root-difference")

    fig.tight_layout()
    fig.savefig(OUT / "area_difference.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Figure 2: parabola_line_area.png
# ============================================================
def fig_parabola_line_area():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    x = np.linspace(-2.5, 2.5, 400)

    # left: parabola with several lines y = a_n x + 1 for varying n
    ax = axes[0]
    ax.plot(x, x**2, "b-", lw=2, label=r"$y = x^2$")
    colors = ["#d62728", "#ff7f0e", "#2ca02c", "#9467bd"]
    for n, c in zip([11, 14, 20, 30], colors):
        # a_n^2 + 4 = n^(2/3)
        if n**(2/3) - 4 > 0:
            a_n = np.sqrt(n**(2/3) - 4)
            ax.plot(x, a_n*x + 1, "-", color=c, lw=1.4, label=fr"$n={n}$, $a_n={a_n:.2f}$")
    ax.set_xlim(-2.5, 2.5); ax.set_ylim(-1, 6)
    ax.set_title(r"$y = x^2$ and $y = a_n x + 1$")
    ax.legend(fontsize=8, loc="upper left")

    # right: a_n^2 / n^(2/3) -> 1
    ax = axes[1]
    n_vals = np.arange(11, 200)
    ratio = 1 - 4 / (n_vals**(2/3))
    ax.plot(n_vals, ratio, "ro-", ms=3, lw=1.0)
    ax.axhline(1, color="k", ls="--", lw=0.8)
    ax.set_xlabel("n")
    ax.set_ylabel(r"$a_n^2 \,/\, \sqrt[3]{n^2}$")
    ax.set_title(r"$a_n^2 / \sqrt[3]{n^2} \to 1$")
    ax.set_ylim(0, 1.05)

    fig.tight_layout()
    fig.savefig(OUT / "parabola_line_area.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Figure 3: conjugate_pair.png — (2+sqrt(3))^n vs (2-sqrt(3))^n
# ============================================================
def fig_conjugate_pair():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    n_vals = np.arange(1, 16)
    p = (2 + np.sqrt(3)) ** n_vals
    m = (2 - np.sqrt(3)) ** n_vals
    a = (p + m) / 2
    b = (p - m) / (2 * np.sqrt(3))

    ax = axes[0]
    ax.semilogy(n_vals, a, "bo-", ms=5, label=r"$a_n$")
    ax.semilogy(n_vals, b, "rs-", ms=5, label=r"$b_n$")
    ax.semilogy(n_vals, p, "g^--", ms=4, alpha=0.5, label=r"$(2+\sqrt{3})^n$")
    ax.set_xlabel("n"); ax.set_ylabel("value (log)")
    ax.set_title(r"$a_n, b_n$ grow like $(2+\sqrt{3})^n$")
    ax.legend(fontsize=9)

    ax = axes[1]
    ax.plot(n_vals, a / b, "bo-", ms=5, label=r"$a_n / b_n$")
    ax.axhline(np.sqrt(3), color="r", ls="--", lw=1.0, label=r"$\sqrt{3}$")
    ax.set_xlabel("n"); ax.set_ylabel(r"$a_n / b_n$")
    ax.set_title(r"$a_n/b_n \to \sqrt{3}$")
    ax.legend(fontsize=9)
    ax.set_ylim(1.5, 2.2)

    fig.tight_layout()
    fig.savefig(OUT / "conjugate_pair.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    fig_area_difference()
    fig_parabola_line_area()
    fig_conjugate_pair()
    print(f"figures written to {OUT}")
