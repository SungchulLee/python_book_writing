"""Figures for absolute_value_integral.md.

Generates PNGs in this directory:

- ``example1_graph_shape.png``    : graph of f(x) = 2x/(1+x²) with sign of
  f', showing monotone branches on (-∞, -1], [-1, 1], [1, ∞).
- ``example1_one_to_one.png``     : same graph with three example intervals
  where f is one-to-one (subsets of the three monotone branches).
- ``example2_absolute.png``       : the area ∫₀² |t - 1| dt as two triangles.
- ``exercise1_admissible.png``    : admissible (b, a, c) region for the
  one-to-one condition (visualized).
- ``exercise2_cases.png``         : three cases of the integrand |f(t) - x|
  on [0, 1] for x < 0, 0 ≤ x < 1, x ≥ 1.
- ``exercise3_Ax_graph.png``      : graph of A(x) on [-0.5, 2] with the
  local minimum at x = 4/5 and A(k) = ln 2 at k = 2 ln 2.

Run with ``python absolute_value_integral_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def _f(x):
    return 2 * x / (1 + x**2)


# ===
# Figure 1 — Graph of f and its monotone branches
# ===


def make_graph_shape(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    xs = np.linspace(-5, 5, 600)
    ys = _f(xs)

    # Shade three monotone branches with different colors
    left = xs <= -1
    middle = (xs >= -1) & (xs <= 1)
    right = xs >= 1

    ax.plot(xs[left], ys[left], color="tab:red", linewidth=2.2, label=r"decreasing on $(-\infty, -1]$")
    ax.plot(xs[middle], ys[middle], color="tab:green", linewidth=2.2, label=r"increasing on $[-1, 1]$")
    ax.plot(xs[right], ys[right], color="tab:red", linewidth=2.2, label=r"decreasing on $[1, \infty)$")

    # Mark critical points (1, 1) and (-1, -1)
    ax.plot(1, 1, "o", color="black", markersize=7)
    ax.annotate(r"$(1,\,1)$", (1, 1), xytext=(8, 5), textcoords="offset points", fontsize=11)
    ax.plot(-1, -1, "o", color="black", markersize=7)
    ax.annotate(r"$(-1,\,-1)$", (-1, -1), xytext=(-50, -15), textcoords="offset points", fontsize=11)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.axhline(1, color="gray", linewidth=0.5, linestyle=":")
    ax.axhline(-1, color="gray", linewidth=0.5, linestyle=":")
    ax.axvline(1, color="gray", linewidth=0.5, linestyle=":")
    ax.axvline(-1, color="gray", linewidth=0.5, linestyle=":")

    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(-1.4, 1.4)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"$f(x) = \frac{2x}{1 + x^2}$:  monotone on three branches", fontsize=12)
    ax.legend(loc="lower right", fontsize=10)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 2 — One-to-one intervals (subsets of monotone branches)
# ===


def make_one_to_one(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    xs = np.linspace(-5, 5, 600)
    ys = _f(xs)

    ax.plot(xs, ys, color="tab:blue", linewidth=2)

    # Three example intervals (subsets of monotone branches)
    intervals = [
        (-4, -1.5, "tab:red"),
        (-0.8, 0.8, "tab:green"),
        (1.5, 4, "tab:red"),
    ]
    for b, c, color in intervals:
        ts = np.linspace(b, c, 100)
        ax.plot(ts, _f(ts), color=color, linewidth=3.5, alpha=0.8)
        ax.plot(b, _f(b), "o", color=color, markersize=7)
        ax.plot(c, _f(c), "o", color=color, markersize=7)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.axvline(-1, color="gray", linewidth=0.5, linestyle=":")
    ax.axvline(1, color="gray", linewidth=0.5, linestyle=":")
    ax.annotate(r"$x = -1$", (-1, 1.25), fontsize=10, color="gray", ha="center")
    ax.annotate(r"$x = 1$", (1, 1.25), fontsize=10, color="gray", ha="center")

    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(-1.4, 1.4)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"$f$ is one-to-one on any subset of a single monotone branch", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 3 — ∫₀² |t - 1| dt as two triangles
# ===


def make_absolute_example(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))

    ts = np.linspace(0, 2, 200)
    ys = np.abs(ts - 1)
    ax.plot(ts, ys, color="tab:blue", linewidth=2.2)

    # Two shaded triangles
    ax.fill_between(ts[ts <= 1], ys[ts <= 1], alpha=0.3, color="tab:red", label=r"$\int_0^1 (1-t)\,dt = \frac{1}{2}$")
    ax.fill_between(ts[ts >= 1], ys[ts >= 1], alpha=0.3, color="tab:green", label=r"$\int_1^2 (t-1)\,dt = \frac{1}{2}$")

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.axvline(1, color="gray", linewidth=0.5, linestyle="--")

    ax.annotate(r"$y = |t - 1|$", (1.5, 0.7), fontsize=12, color="tab:blue")
    ax.annotate(r"$t = 1$", (1.02, 0.5), fontsize=10, color="gray")

    ax.set_xlim(-0.15, 2.15)
    ax.set_ylim(-0.1, 1.25)
    ax.set_xlabel(r"$t$", fontsize=11)
    ax.set_title(r"$\int_0^2 |t - 1|\,dt = 1$  by splitting at $t = 1$", fontsize=12)
    ax.legend(fontsize=10, loc="upper right")

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 4 — Admissible (a) region for one-to-one condition
# ===


def make_admissible(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    xs = np.linspace(-3, 3, 600)
    ys = _f(xs)

    ax.plot(xs, ys, color="tab:blue", linewidth=2)

    # Highlight the middle monotone branch on [-1, 1]
    ms = np.linspace(-1, 1, 200)
    ax.plot(ms, _f(ms), color="tab:green", linewidth=3.5, alpha=0.8)
    ax.fill_betweenx([-1.3, 1.3], -1, 1, color="tab:green", alpha=0.08)
    ax.annotate(
        r"$[b, c] \subset [-1, 1]$:  $a \in (-1, 1)$",
        (0, 1.05),
        fontsize=12,
        ha="center",
        color="tab:green",
    )

    # Show a < -1 not possible (b<a<c with negative b means b<-1 then c > -1; but [b,c] crosses -1)
    ax.axvline(-1, color="black", linewidth=0.6, linestyle="--")
    ax.axvline(1, color="black", linewidth=0.6, linestyle="--")
    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)

    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-1.3, 1.3)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(
        r"Range of $a$ such that $\exists$ negative $b$, positive $c$ with $f$ one-to-one on $[b, c]$",
        fontsize=11,
    )

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 5 — Three cases of |f(t) - x| on [0, 1]
# ===


def make_cases(out_path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))

    ts = np.linspace(0, 1, 200)
    f_vals = _f(ts)

    cases = [
        (-0.5, r"$x = -0.5$  ($x < 0$): $|f - x| = f - x$"),
        (0.5, r"$x = 0.5$  ($0 \leq x < 1$): split at $g(x)$"),
        (1.5, r"$x = 1.5$  ($x \geq 1$): $|f - x| = x - f$"),
    ]
    for ax, (x_val, title) in zip(axes, cases):
        absdiff = np.abs(f_vals - x_val)
        ax.plot(ts, absdiff, color="tab:blue", linewidth=2)
        ax.fill_between(ts, absdiff, alpha=0.25, color="tab:blue")

        # Reference: f and y = x
        ax.plot(ts, f_vals, color="tab:gray", linewidth=1, linestyle=":")
        ax.axhline(x_val, color="tab:red", linewidth=1, linestyle="--")

        # If 0 ≤ x < 1, mark g(x) where f(g(x)) = x
        if 0 <= x_val < 1:
            # f(t) = x ⇒ 2t/(1+t²) = x ⇒ x t² - 2t + x = 0 ⇒ t = (1 - √(1-x²))/x
            g_x = (1 - np.sqrt(1 - x_val**2)) / x_val
            ax.axvline(g_x, color="tab:purple", linewidth=1, linestyle="--")
            ax.annotate(rf"$g(x) \approx {g_x:.2f}$", (g_x, 0.4), fontsize=10, color="tab:purple",
                        rotation=90, va="bottom", ha="right")

        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.1, 1.7)
        ax.set_xlabel(r"$t$", fontsize=10)
        ax.set_title(title, fontsize=10)

    fig.suptitle(r"$|f(t) - x|$  on $[0, 1]$:  three regimes", fontsize=12)
    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 6 — A(x) graph
# ===


def _A(x):
    """Compute A(x) = ∫₀¹ |f(t) - x| dt analytically."""
    if x < 0:
        return np.log(2) - x
    if x >= 1:
        return x - np.log(2)
    # 0 ≤ x < 1: split at g(x)
    if x == 0:
        return np.log(2)
    g_x = (1 - np.sqrt(1 - x**2)) / x
    int_low = x * g_x - np.log(1 + g_x**2)
    int_high = (np.log(2) - np.log(1 + g_x**2)) - x * (1 - g_x)
    return int_low + int_high


def make_Ax_graph(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    xs = np.linspace(-0.6, 2.2, 400)
    As = np.array([_A(x) for x in xs])
    ax.plot(xs, As, color="tab:blue", linewidth=2.2)

    # Local minimum at x = c = 4/5
    c = 0.8
    Ac = _A(c)
    ax.plot(c, Ac, "o", color="tab:red", markersize=9)
    ax.annotate(
        r"local min at  $x = c = \frac{4}{5}$",
        (c, Ac),
        xytext=(20, -25),
        textcoords="offset points",
        fontsize=11,
        color="tab:red",
        arrowprops=dict(arrowstyle="->", color="tab:red"),
    )

    # A(k) = ln 2 at k = 2 ln 2
    k = 2 * np.log(2)
    ax.plot(k, np.log(2), "o", color="tab:green", markersize=9)
    ax.annotate(
        r"$A(k) = \ln 2$  at  $k = 2\ln 2$",
        (k, np.log(2)),
        xytext=(15, 15),
        textcoords="offset points",
        fontsize=11,
        color="tab:green",
        arrowprops=dict(arrowstyle="->", color="tab:green"),
    )

    # Reference line y = ln 2
    ax.axhline(np.log(2), color="gray", linewidth=0.7, linestyle=":")
    ax.annotate(r"$y = \ln 2$", (-0.55, np.log(2) + 0.04), fontsize=10, color="gray")

    # Also mark A(0) = ln 2
    ax.plot(0, np.log(2), "o", color="black", markersize=6)
    ax.annotate(r"$A(0) = \ln 2$", (0, np.log(2)), xytext=(8, -18),
                textcoords="offset points", fontsize=10)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-0.6, 2.2)
    ax.set_ylim(-0.05, 1.7)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$A(x)$", fontsize=11)
    ax.set_title(r"$A(x) = \int_0^1 |f(t) - x|\,dt$:  V-shape with vertex at $c$", fontsize=12)
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Entry point
# ===

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    make_graph_shape(out_dir / "example1_graph_shape.png")
    make_one_to_one(out_dir / "example1_one_to_one.png")
    make_absolute_example(out_dir / "example2_absolute.png")
    make_admissible(out_dir / "exercise1_admissible.png")
    make_cases(out_dir / "exercise2_cases.png")
    make_Ax_graph(out_dir / "exercise3_Ax_graph.png")
    print(f"Wrote figures to {out_dir}")
