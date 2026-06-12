"""Figures for ch01/integral_equation/integral_equation.md."""

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
# Figure 1: two_tools.png — flow diagram
# ============================================================
def fig_two_tools():
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    ax.axis("off")

    # boxes
    def box(x, y, w, h, text, color="#cfe2f3"):
        ax.add_patch(plt.Rectangle((x, y), w, h, fc=color, ec="black", lw=1.2))
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=11)

    box(0.3, 3.5, 3.0, 1.4, "integral equation\n$f(x) + \\int_0^x f = g(x)$", "#fff2cc")
    box(4.5, 4.5, 3.0, 1.0, "step 1: differentiate\n$f'(x) + f(x) = g'(x)$", "#cfe2f3")
    box(4.5, 2.5, 3.0, 1.0, "step 2: set $x = 0$\n$f(0)$ extracted", "#cfe2f3")
    box(8.5, 3.5, 3.2, 1.4, "ODE + initial value\n$\\Rightarrow$ unique $f(x)$", "#d9ead3")

    # arrows
    ax.annotate("", xy=(4.5, 5.0), xytext=(3.3, 4.5),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="black"))
    ax.annotate("", xy=(4.5, 3.0), xytext=(3.3, 3.8),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="black"))
    ax.annotate("", xy=(8.5, 4.5), xytext=(7.5, 5.0),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="black"))
    ax.annotate("", xy=(8.5, 4.0), xytext=(7.5, 3.0),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="black"))

    ax.text(6, 0.8, "core idea: convert integral-equation to differential-equation",
            ha="center", fontsize=11, style="italic", color="gray")

    fig.savefig(OUT / "two_tools.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Figure 2: exponential_force.png
# ============================================================
def fig_exponential_force():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # left: f(x) = e^(x/2)
    ax = axes[0]
    x = np.linspace(-1, 4, 400)
    ax.plot(x, np.exp(x/2), "b-", lw=2, label=r"$f(x) = e^{x/2}$")
    ax.plot(x, 0.5 * np.exp(x/2), "r--", lw=1.5, label=r"$f'(x) = \frac{1}{2}e^{x/2}$")
    ax.axhline(0, color="k", lw=0.5)
    ax.scatter([0], [1], color="green", s=50, zorder=3)
    ax.text(0.1, 1.1, "$f(0)=1$", fontsize=10, color="green")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title(r"$f = 2 f'$ with $f(0)=1$")
    ax.legend(fontsize=9)

    # right: comparison of inequalities forced to equality
    ax = axes[1]
    x = np.linspace(0, 3, 200)
    f = np.exp(x/2)
    fp = 0.5 * np.exp(x/2)
    ax.plot(x, f**2, "b-", lw=2, label=r"$\{f(x)\}^2$")
    ax.plot(x, np.cumsum(f**2) * (x[1]-x[0]) + 1, "r--", lw=1.5,
            label=r"$\int_0^x \{f\}^2\, dt + 1$")
    ax.plot(x, np.cumsum(2*f*fp) * (x[1]-x[0]) + 1, "g:", lw=2,
            label=r"$\int_0^x 2 f f'\, dt + 1$")
    ax.set_xlabel("x"); ax.set_ylabel("value")
    ax.set_title("two-sided inequality forces equality")
    ax.legend(fontsize=9, loc="upper left")

    fig.tight_layout()
    fig.savefig(OUT / "exponential_force.png", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    fig_two_tools()
    fig_exponential_force()
    print(f"figures written to {OUT}")
