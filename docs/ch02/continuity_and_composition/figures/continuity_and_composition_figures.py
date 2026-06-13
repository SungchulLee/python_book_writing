"""Figures for continuity_and_composition.md.

Generates PNGs in this directory:

- ``example1_continuity.png``     : the three conditions for continuity of
  a function at a point — defined, limit exists, limit equals value.
- ``example2_branches.png``       : a cubic with positive leading coefficient
  has three monotone branches; a one-sided inverse traces one branch.
- ``exercise1_setup.png``         : f(x) = (x+2)(x-2)(x-3), zeros at -2, 2,
  3 and value f(1) = 6.
- ``exercise1_g.png``             : the function g traces the left branch of
  f from t = 0 up to t = 6, then jumps at t = 6.
- ``exercise2_constraint.png``    : the inequality n - 1 < m ≤ n that the
  local minimum value m must satisfy for h continuous, k not continuous.
- ``exercise2_solution.png``      : f(x) = x³ - 3x² + 6 with h(2) = 1 + √3
  and tangent line of slope 1/6.

Run with ``python continuity_and_composition_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# ===
# Figure 1 — Continuity at a point: three conditions
# ===


def make_continuity(out_path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))

    # Each plot shows a different failure mode + the continuous case
    # (a) not defined
    xs = np.linspace(-1, 3, 200)
    ys = xs**2 - 2 * xs + 1
    axes[0].plot(xs[xs != 1], ys[xs != 1], color="tab:blue", linewidth=2)
    axes[0].plot(1, 0, "o", markerfacecolor="white", markeredgecolor="tab:red", markersize=10)
    axes[0].set_title("(a) Not defined at $x = 1$", fontsize=11)
    axes[0].annotate(r"$f(1)$ undefined", (1, 0), xytext=(15, 5),
                     textcoords="offset points", fontsize=10, color="tab:red")

    # (b) limit doesn't exist (jump)
    xs1 = np.linspace(-1, 1, 100)
    xs2 = np.linspace(1, 3, 100)
    axes[1].plot(xs1, xs1, color="tab:blue", linewidth=2)
    axes[1].plot(xs2, xs2 - 1, color="tab:blue", linewidth=2)
    axes[1].plot(1, 1, "o", markerfacecolor="tab:blue", markeredgecolor="tab:blue", markersize=8)
    axes[1].plot(1, 0, "o", markerfacecolor="white", markeredgecolor="tab:red", markersize=10)
    axes[1].set_title("(b) Limit does not exist", fontsize=11)
    axes[1].annotate("jump at $x = 1$", (1, 0.5), xytext=(10, 0),
                     textcoords="offset points", fontsize=10, color="tab:red")

    # (c) limit ≠ value
    xs_c = np.linspace(-1, 3, 200)
    ys_c = xs_c
    axes[2].plot(xs_c[xs_c != 1], ys_c[xs_c != 1], color="tab:blue", linewidth=2)
    axes[2].plot(1, 1, "o", markerfacecolor="white", markeredgecolor="tab:blue", markersize=8)
    axes[2].plot(1, 2.5, "o", markerfacecolor="tab:red", markeredgecolor="tab:red", markersize=8)
    axes[2].set_title(r"(c) $\lim f \neq f(1)$", fontsize=11)
    axes[2].annotate("limit $= 1$\nvalue $= 2.5$", (1, 1.7), xytext=(8, 0),
                     textcoords="offset points", fontsize=10, color="tab:red")

    for ax in axes:
        ax.axhline(0, color="black", linewidth=0.5)
        ax.axvline(1, color="gray", linewidth=0.5, linestyle="--")
        ax.set_xlim(-1.2, 3.2)
        ax.set_ylim(-1.2, 3.2)

    fig.suptitle(
        r"Continuity at $x = 1$ fails in three ways",
        fontsize=12,
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 2 — A cubic has three monotone branches
# ===


def make_branches(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    xs = np.linspace(-3, 5, 600)
    ys = xs**3 - 3 * xs**2 - 4 * xs + 12  # f(x) = (x+2)(x-2)(x-3)

    # Critical points (numerically)
    # f'(x) = 3x² - 6x - 4 = 0 ⟹ x = 1 ± √(7/3)
    x_max = 1 - np.sqrt(7 / 3)
    x_min = 1 + np.sqrt(7 / 3)

    # Color three branches
    left_mask = xs <= x_max
    mid_mask = (xs >= x_max) & (xs <= x_min)
    right_mask = xs >= x_min

    ax.plot(xs[left_mask], ys[left_mask], color="tab:red", linewidth=2.2, label="left branch (increasing)")
    ax.plot(xs[mid_mask], ys[mid_mask], color="tab:green", linewidth=2.2, label="middle branch (decreasing)")
    ax.plot(xs[right_mask], ys[right_mask], color="tab:purple", linewidth=2.2, label="right branch (increasing)")

    # Mark critical points
    ax.plot(x_max, x_max**3 - 3 * x_max**2 - 4 * x_max + 12, "o", color="black", markersize=7)
    ax.plot(x_min, x_min**3 - 3 * x_min**2 - 4 * x_min + 12, "o", color="black", markersize=7)

    # Mark zeros
    for z in [-2, 2, 3]:
        ax.plot(z, 0, "x", color="tab:blue", markersize=10)
    ax.annotate(r"$f(-2) = 0$", (-2, 0), xytext=(-25, -18), textcoords="offset points", fontsize=10)
    ax.annotate(r"$f(2) = 0$", (2, 0), xytext=(-15, 12), textcoords="offset points", fontsize=10)
    ax.annotate(r"$f(3) = 0$", (3, 0), xytext=(2, -18), textcoords="offset points", fontsize=10)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-3.2, 5.2)
    ax.set_ylim(-7, 18)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$f(x)$", fontsize=11)
    ax.set_title(r"$f(x) = (x+2)(x-2)(x-3)$:  three monotone branches", fontsize=12)
    ax.legend(loc="upper left", fontsize=10)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 3 — Exercise 1 setup: f(x) = (x+2)(x-2)(x-3) with f(1) = 6
# ===


def make_setup(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5.5))

    xs = np.linspace(-3, 5, 600)
    ys = (xs + 2) * (xs - 2) * (xs - 3)
    ax.plot(xs, ys, color="tab:blue", linewidth=2.2)

    # Horizontal line y = 6
    ax.axhline(6, color="tab:red", linewidth=1.4, linestyle="--")
    ax.annotate(r"$y = 6$", (-2.8, 6.3), fontsize=11, color="tab:red")

    # Three solutions of f(x) = 6
    roots = [1 - np.sqrt(7), 1.0, 1 + np.sqrt(7)]
    for i, r in enumerate(roots):
        ax.plot(r, 6, "o", color="tab:red", markersize=8)
        labels = [r"$1 - \sqrt{7}$", r"$g(6) = 1$", r"$1 + \sqrt{7}$"]
        ax.annotate(labels[i], (r, 6), xytext=(8, 8 if i != 1 else -16),
                    textcoords="offset points", fontsize=10, color="tab:red")

    # Mark zeros
    for z in [-2, 2, 3]:
        ax.plot(z, 0, "x", color="black", markersize=9)

    ax.annotate(r"$f(-2) = 0$", (-2, 0), xytext=(8, -18), textcoords="offset points", fontsize=10)
    ax.annotate(r"$f(2) = 0$", (2, 0), xytext=(-15, 12), textcoords="offset points", fontsize=10)
    ax.annotate(r"$f(3) = 0$", (3, 0), xytext=(8, -18), textcoords="offset points", fontsize=10)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-3.2, 5.2)
    ax.set_ylim(-7, 18)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$f(x)$", fontsize=11)
    ax.set_title(r"$f(x) = (x+2)(x-2)(x-3)$:  solutions of $f(x) = 6$", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 4 — Exercise 1: g traces left branch then jumps at t = 6
# ===


def make_g_trajectory(out_path: Path) -> None:
    fig, (ax_f, ax_g) = plt.subplots(1, 2, figsize=(13, 5))

    # Left panel: y = f(x) with traced branch
    xs = np.linspace(-3, 5, 600)
    ys = (xs + 2) * (xs - 2) * (xs - 3)
    ax_f.plot(xs, ys, color="tab:blue", linewidth=1.5)

    x_max = 1 - np.sqrt(7 / 3)
    left_mask = xs <= x_max
    ax_f.plot(xs[left_mask], ys[left_mask], color="tab:red", linewidth=3, alpha=0.8,
              label=r"$g(t)$ for $t < 6$")

    # Right branch for t > 6
    x_min = 1 + np.sqrt(7 / 3)
    right_mask = xs >= x_min
    ax_f.plot(xs[right_mask], ys[right_mask], color="tab:purple", linewidth=3, alpha=0.8,
              label=r"$g(t)$ for $t > 6$")

    # Point g(0) = -2
    ax_f.plot(-2, 0, "o", color="tab:red", markersize=9)
    ax_f.annotate(r"$(-2, 0)$:  $g(0) = -2$", (-2, 0), xytext=(8, -18),
                  textcoords="offset points", fontsize=10, color="tab:red")

    # Jump
    ax_f.plot(1 - np.sqrt(7), 6, "o", color="tab:red", markersize=9)
    ax_f.plot(1, 6, "o", color="black", markersize=9)
    ax_f.plot(1 + np.sqrt(7), 6, "o", color="tab:purple", markersize=9)
    ax_f.annotate(r"$g(6) = 1$", (1, 6), xytext=(8, 8), textcoords="offset points", fontsize=10)

    ax_f.axhline(0, color="black", linewidth=0.5)
    ax_f.axvline(0, color="black", linewidth=0.5)
    ax_f.set_xlim(-3.2, 5.2)
    ax_f.set_ylim(-7, 18)
    ax_f.set_xlabel(r"$x$", fontsize=11)
    ax_f.set_ylabel(r"$f(x)$", fontsize=11)
    ax_f.set_title(r"Tracing $g$ along $y = f(x)$", fontsize=11)
    ax_f.legend(loc="upper left", fontsize=10)

    # Right panel: g(t) vs t (jump at t = 6)
    ts1 = np.linspace(-7, 6, 200)
    # On left branch, x is between -∞ and x_max. Map x to f(x) = t.
    # We want g(t) = x such that x ≤ x_max and f(x) = t.
    # Since g is on the left branch, parametrize by x and plot (f(x), x).
    xs_left = np.linspace(-4, x_max - 0.01, 200)
    ts_left = (xs_left + 2) * (xs_left - 2) * (xs_left - 3)
    mask_left = ts_left <= 6
    ax_g.plot(ts_left[mask_left], xs_left[mask_left], color="tab:red", linewidth=2.2)

    # Right branch
    xs_right = np.linspace(x_min + 0.01, 5, 200)
    ts_right = (xs_right + 2) * (xs_right - 2) * (xs_right - 3)
    mask_right = ts_right >= 6
    ax_g.plot(ts_right[mask_right], xs_right[mask_right], color="tab:purple", linewidth=2.2)

    # Mark g(6) = 1 with filled circle
    ax_g.plot(6, 1, "o", color="black", markersize=10)
    # Open circles at limits
    ax_g.plot(6, 1 - np.sqrt(7), "o", markerfacecolor="white", markeredgecolor="tab:red", markersize=10)
    ax_g.plot(6, 1 + np.sqrt(7), "o", markerfacecolor="white", markeredgecolor="tab:purple", markersize=10)

    ax_g.annotate(r"$g(6) = 1$", (6, 1), xytext=(10, 0), textcoords="offset points", fontsize=11)
    ax_g.annotate(r"$\lim_{t \to 6^-} g(t) = 1 - \sqrt{7}$", (6, 1 - np.sqrt(7)),
                  xytext=(10, 0), textcoords="offset points", fontsize=10, color="tab:red")
    ax_g.annotate(r"$\lim_{t \to 6^+} g(t) = 1 + \sqrt{7}$", (6, 1 + np.sqrt(7)),
                  xytext=(10, 0), textcoords="offset points", fontsize=10, color="tab:purple")

    ax_g.axhline(0, color="black", linewidth=0.5)
    ax_g.axvline(6, color="gray", linewidth=0.7, linestyle=":")
    ax_g.set_xlim(-8, 18)
    ax_g.set_ylim(-4, 5)
    ax_g.set_xlabel(r"$t$", fontsize=11)
    ax_g.set_ylabel(r"$g(t)$", fontsize=11)
    ax_g.set_title(r"$g(t)$ has a jump discontinuity at $t = 6$", fontsize=11)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 5 — n - 1 < m ≤ n constraint
# ===


def make_constraint(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))

    # f(x) = x³ - 3x² + c, local min m = c - 4 at x = 2
    cs = np.linspace(5, 8, 200)
    ms = cs - 4  # local min value

    ax.plot(cs, ms, color="tab:blue", linewidth=2.2, label=r"$m = c - 4$  (local min value)")

    # Show region n - 1 < m ≤ n for n = 2
    n = 2
    ax.axhline(n, color="tab:green", linewidth=1.4, linestyle="--", label=rf"$m = n = {n}$")
    ax.axhline(n - 1, color="tab:red", linewidth=1.4, linestyle="--", label=rf"$m = n - 1 = {n-1}$")
    ax.fill_between(cs, n - 1, n, color="tab:green", alpha=0.1, label=r"admissible $m$")

    # Mark solution c = 6, m = 2
    ax.plot(6, 2, "o", color="black", markersize=10)
    ax.annotate(r"$c = 6, m = 2$", (6, 2), xytext=(10, -15), textcoords="offset points", fontsize=11)

    ax.set_xlim(5, 8)
    ax.set_ylim(0, 5)
    ax.set_xlabel(r"$c$  (constant in $f(x) = x^3 - 3x^2 + c$)", fontsize=11)
    ax.set_ylabel(r"local min value $m$", fontsize=11)
    ax.set_title(r"Admissible range: $n - 1 < m \leq n$  forces $n + 3 < c \leq n + 4$", fontsize=11)
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 6 — Exercise 2 solution: f, h(2), tangent line of slope 1/6
# ===


def make_solution(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5.5))

    xs = np.linspace(-1.5, 4, 600)
    ys = xs**3 - 3 * xs**2 + 6  # n = 2, c = 6
    ax.plot(xs, ys, color="tab:blue", linewidth=2.2)

    # Local max at x = 0 (value 6), local min at x = 2 (value 2)
    ax.plot(0, 6, "o", color="tab:orange", markersize=8)
    ax.annotate(r"local max $(0, 6)$", (0, 6), xytext=(-50, 12), textcoords="offset points",
                fontsize=10, color="tab:orange")
    ax.plot(2, 2, "o", color="tab:orange", markersize=8)
    ax.annotate(r"local min $(2, 2)$", (2, 2), xytext=(8, -18), textcoords="offset points",
                fontsize=10, color="tab:orange")

    # h(2) = 1 + √3, f(h(2)) = 4 = 2 + n
    h2 = 1 + np.sqrt(3)
    ax.plot(h2, 4, "o", color="tab:red", markersize=10)
    ax.annotate(rf"$h(2) = 1 + \sqrt{{3}}$,  $f(h(2)) = 4$", (h2, 4),
                xytext=(10, 10), textcoords="offset points", fontsize=11, color="tab:red")

    # Tangent line at h(2) — slope f'(h(2)) = 6
    slope_f = 3 * h2**2 - 6 * h2
    tx = np.linspace(h2 - 1, h2 + 1, 30)
    ty = 4 + slope_f * (tx - h2)
    ax.plot(tx, ty, color="tab:red", linewidth=1.5, linestyle="--",
            label=rf"$f'(h(2)) = 6$, so $h'(2) = 1/6$")

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-1.5, 4)
    ax.set_ylim(-5, 12)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$f(x)$", fontsize=11)
    ax.set_title(r"$f(x) = x^3 - 3x^2 + 6$  (where $n = 2$, $c = 6$):  $h'(2) = 1/6$", fontsize=11)
    ax.legend(loc="upper left", fontsize=10)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Entry point
# ===

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    make_continuity(out_dir / "example1_continuity.png")
    make_branches(out_dir / "example2_branches.png")
    make_setup(out_dir / "exercise1_setup.png")
    make_g_trajectory(out_dir / "exercise1_g.png")
    make_constraint(out_dir / "exercise2_constraint.png")
    make_solution(out_dir / "exercise2_solution.png")
    print(f"Wrote figures to {out_dir}")
