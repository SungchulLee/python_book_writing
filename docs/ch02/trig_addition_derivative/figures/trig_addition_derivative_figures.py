"""Figures for ch02/trig_addition_derivative/trig_addition_derivative.md."""

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
# Figure 1: derivation_flow.png — unit circle + two methods
# ============================================================
def fig_derivation_flow():
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    # Left: unit circle with P, Q
    ax = axes[0]
    theta = np.linspace(0, 2*np.pi, 400)
    ax.plot(np.cos(theta), np.sin(theta), "k-", lw=1.0)
    alpha, beta = np.deg2rad(70), np.deg2rad(20)
    P = (np.cos(alpha), np.sin(alpha))
    Q = (np.cos(beta), np.sin(beta))
    ax.plot([0, P[0]], [0, P[1]], "b-", lw=1.5)
    ax.plot([0, Q[0]], [0, Q[1]], "g-", lw=1.5)
    ax.plot([P[0], Q[0]], [P[1], Q[1]], "r-", lw=2.0, label="PQ")
    ax.scatter([0, P[0], Q[0]], [0, P[1], Q[1]], color=["k", "b", "g"], s=50, zorder=3)
    ax.text(P[0] + 0.05, P[1] + 0.05, r"$\mathrm{P}(\cos\alpha, \sin\alpha)$", fontsize=10, color="b")
    ax.text(Q[0] + 0.05, Q[1] - 0.05, r"$\mathrm{Q}(\cos\beta, \sin\beta)$", fontsize=10, color="g")
    ax.text(-0.1, -0.1, r"O", fontsize=12)
    ax.text(0.18, 0.1, r"$\alpha - \beta$", fontsize=11, color="red")
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.set_title(r"distance $\overline{\mathrm{PQ}}$ computed two ways")
    ax.legend(fontsize=9)

    # Right: the two formulas
    ax = axes[1]
    ax.axis("off")
    ax.text(0.5, 0.85, "Method A — coord distance:", ha="center", fontsize=12, color="b")
    ax.text(0.5, 0.72, r"$\overline{\mathrm{PQ}}^2 = 2 - 2(\cos\alpha\cos\beta + \sin\alpha\sin\beta)$",
            ha="center", fontsize=12)
    ax.text(0.5, 0.55, "Method B — law of cosines:", ha="center", fontsize=12, color="g")
    ax.text(0.5, 0.42, r"$\overline{\mathrm{PQ}}^2 = 2 - 2\cos(\alpha - \beta)$",
            ha="center", fontsize=12)
    ax.text(0.5, 0.22, "Equate ⇒", ha="center", fontsize=13, color="red")
    ax.text(0.5, 0.08, r"$\cos(\alpha - \beta) = \cos\alpha\cos\beta + \sin\alpha\sin\beta$",
            ha="center", fontsize=14, color="red")

    fig.tight_layout()
    fig.savefig(OUT / "derivation_flow.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Figure 2: cos_derivative.png
# ============================================================
def fig_cos_derivative():
    fig, ax = plt.subplots(figsize=(10, 4.5))
    x = np.linspace(-2*np.pi, 2*np.pi, 500)
    ax.plot(x, np.cos(x), "b-", lw=2, label=r"$\cos x$")
    ax.plot(x, -np.sin(x), "r-", lw=2, label=r"$-\sin x = (\cos x)'$")
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title(r"derivative: $(\cos x)' = -\sin x$")
    ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
    ax.set_xticklabels([r"$-2\pi$", r"$-\pi$", "0", r"$\pi$", r"$2\pi$"])
    ax.legend(fontsize=11)

    fig.tight_layout()
    fig.savefig(OUT / "cos_derivative.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    fig_derivation_flow()
    fig_cos_derivative()
    print(f"figures written to {OUT}")
