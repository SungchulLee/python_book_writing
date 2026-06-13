"""Figures for piecewise_curve_analysis.md.

Generates PNGs in this directory:

- ``example1_arc_length_trick.png`` : the integrand √(1 + (y')²) being a
  perfect square for y = x²/4 - (1/2) ln(x/2).
- ``example2_area_bisect.png``      : a line bisecting a planar region's
  area visualised.
- ``exercise_C_curve.png``          : the full closed curve C made of 8
  pieces, with each piece colored differently.
- ``exercise1_lengths.png``         : the eight piece lengths labeled.
- ``exercise2_area.png``            : the enclosed region with its area
  shaded.
- ``exercise3_bisect_line.png``     : line y = -10(x - k) splitting the
  enclosed area in half.
- ``exercise4_g_count.png``         : the count g(a) of intersections of
  y = a x with C, as a function of a.
- ``exercise5_l_count.png``         : the count f(t) of intersections of
  line ℓ_t (slope 4/3, x-intercept t) with C — discontinuity structure.

Run with ``python piecewise_curve_analysis_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def _C2(x):
    return x**2 / 4 - 0.5 * np.log(x / 2)


def _C7(x):
    return x**2 / 4 - 0.5 * np.log(-x / 2)


def _draw_C(ax):
    """Draw the full closed curve C made of 8 pieces."""
    # Each piece a different color for clarity
    colors = {
        1: "tab:blue", 2: "tab:orange", 3: "tab:green", 4: "tab:red",
        5: "tab:purple", 6: "tab:brown", 7: "tab:pink", 8: "tab:cyan",
    }
    # C_1: y = -x + 3 on [0, 2]
    xs = np.linspace(0, 2, 50)
    ax.plot(xs, -xs + 3, color=colors[1], linewidth=2.5)
    # C_2: y = x²/4 - (1/2) ln(x/2) on [2, 4]
    xs = np.linspace(2, 4, 100)
    ax.plot(xs, _C2(xs), color=colors[2], linewidth=2.5)
    # C_3: linear on [2, 4]
    xs = np.linspace(2, 4, 50)
    ax.plot(xs, (16 - np.log(2)) / 4 * (xs - 2) - 4, color=colors[3], linewidth=2.5)
    # C_4: y = -x - 2 on [-2/3, 2]
    xs = np.linspace(-2 / 3, 2, 50)
    ax.plot(xs, -xs - 2, color=colors[4], linewidth=2.5)
    # C_5: y = 2x on [-2, -2/3]
    xs = np.linspace(-2, -2 / 3, 50)
    ax.plot(xs, 2 * xs, color=colors[5], linewidth=2.5)
    # C_6: linear on [-4, -2]
    xs = np.linspace(-4, -2, 50)
    ax.plot(xs, (np.log(2) - 16) / 4 * (xs + 2) - 4, color=colors[6], linewidth=2.5)
    # C_7: y = x²/4 - (1/2) ln(-x/2) on [-4, -2]
    xs = np.linspace(-4, -2, 100)
    ax.plot(xs, _C7(xs), color=colors[7], linewidth=2.5)
    # C_8: y = x + 3 on [-2, 0]
    xs = np.linspace(-2, 0, 50)
    ax.plot(xs, xs + 3, color=colors[8], linewidth=2.5)
    return colors


# ===
# Figure 1 — Arc length trick: perfect square integrand
# ===


def make_arclength_trick(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    xs = np.linspace(2, 4, 200)
    dydx = xs / 2 - 1 / (2 * xs)
    integrand = np.sqrt(1 + dydx**2)
    perfect_sq = xs / 2 + 1 / (2 * xs)

    ax.plot(xs, integrand, color="tab:blue", linewidth=2.5,
            label=r"$\sqrt{1 + (y')^2}$  (actual integrand)")
    ax.plot(xs, perfect_sq, color="tab:red", linewidth=1.5, linestyle="--",
            label=r"$\frac{x}{2} + \frac{1}{2x}$  (perfect-square form)")

    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel("Value", fontsize=11)
    ax.set_title(r"For $y = \frac{x^2}{4} - \frac{1}{2}\ln\frac{x}{2}$:  $1 + (y')^2$ is a perfect square", fontsize=11)
    ax.legend(loc="upper left", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 2 — A line bisecting area of a region
# ===


def make_area_bisect(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 6))

    # A simple region: triangle with vertices (0, 0), (4, 0), (2, 3)
    tri_x = [0, 4, 2, 0]
    tri_y = [0, 0, 3, 0]
    ax.fill(tri_x, tri_y, color="tab:blue", alpha=0.2)

    # A vertical line bisecting it (median from (2, 3) to (2, 0) divides triangle into two equal halves)
    ax.plot([2, 2], [0, 3], color="tab:red", linewidth=2.5, linestyle="--",
            label="bisecting line")

    # Annotations
    ax.annotate("region of area $A$", (1, 0.5), fontsize=11)
    ax.annotate(r"area $= A/2$", (0.6, 1.5), fontsize=10, color="tab:blue")
    ax.annotate(r"area $= A/2$", (2.6, 1.5), fontsize=10, color="tab:blue")

    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 3.5)
    ax.set_aspect("equal")
    ax.set_title("A line bisects the area of a planar region in half", fontsize=11)
    ax.legend(loc="upper right", fontsize=11)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 3 — The full closed curve C
# ===


def make_C_curve(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 8))

    colors = _draw_C(ax)

    # Label each piece
    labels = {
        1: ((1, 2.2), r"$C_1$"),
        2: ((3, 2.5), r"$C_2$"),
        3: ((3.3, -0.5), r"$C_3$"),
        4: ((1.0, -3.4), r"$C_4$"),
        5: ((-1.5, -2.6), r"$C_5$"),
        6: ((-3.3, -0.5), r"$C_6$"),
        7: ((-3, 2.5), r"$C_7$"),
        8: ((-1, 2.2), r"$C_8$"),
    }
    for k, ((xpos, ypos), text) in labels.items():
        ax.annotate(text, (xpos, ypos), fontsize=14, color=colors[k], weight="bold")

    # Key vertices
    vertices = [
        ((0, 3), "(0, 3)"),
        ((2, 1), "(2, 1)"),
        ((4, 4 - np.log(2) / 2), r"$(4,\,4 - \frac{\ln 2}{2})$"),
        ((2, -4), "(2, -4)"),
        ((-2 / 3, -4 / 3), r"$(-\frac{2}{3}, -\frac{4}{3})$"),
        ((-2, -4), "(-2, -4)"),
        ((-4, 4 - np.log(2) / 2), r"$(-4,\,4 - \frac{\ln 2}{2})$"),
        ((-2, 1), "(-2, 1)"),
    ]
    for (x, y), label in vertices:
        ax.plot(x, y, "o", color="black", markersize=6)

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 4)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"Closed curve $C = C_1 \cup C_2 \cup \cdots \cup C_8$", fontsize=12)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 4 — Piece lengths
# ===


def make_lengths(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))

    # Computed lengths
    L_1 = 2 * np.sqrt(2)
    L_2 = 3 + 0.5 * np.log(2)
    L_3 = 0.5 * np.sqrt(16 + (16 - np.log(2)) ** 2)
    L_4 = (8 / 3) * np.sqrt(2)
    L_5 = (4 / 3) * np.sqrt(5)
    L_6 = L_3
    L_7 = L_2
    L_8 = L_1

    lengths = [L_1, L_2, L_3, L_4, L_5, L_6, L_7, L_8]
    labels = [r"$C_1$", r"$C_2$", r"$C_3$", r"$C_4$", r"$C_5$",
              r"$C_6$", r"$C_7$", r"$C_8$"]
    colors_list = ["tab:blue", "tab:orange", "tab:green", "tab:red",
                   "tab:purple", "tab:brown", "tab:pink", "tab:cyan"]

    bars = ax.bar(range(8), lengths, color=colors_list, alpha=0.7)
    for i, (l, lbl) in enumerate(zip(lengths, labels)):
        ax.annotate(f"{l:.3f}", (i, l), xytext=(0, 5), textcoords="offset points",
                    fontsize=10, ha="center")

    ax.set_xticks(range(8))
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_ylabel("Length", fontsize=11)
    ax.set_title(rf"Lengths of the 8 pieces;  total $= {sum(lengths):.3f}$", fontsize=12)
    ax.grid(alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 5 — Enclosed area
# ===


def make_area(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 8))

    _draw_C(ax)

    # Shade the enclosed region using a polygon approximation by sampling C boundary
    xs1 = np.linspace(0, 2, 30)
    ys1 = -xs1 + 3
    xs2 = np.linspace(2, 4, 50)
    ys2 = _C2(xs2)
    xs3 = np.linspace(4, 2, 30)
    ys3 = (16 - np.log(2)) / 4 * (xs3 - 2) - 4
    xs4 = np.linspace(2, -2 / 3, 30)
    ys4 = -xs4 - 2
    xs5 = np.linspace(-2 / 3, -2, 30)
    ys5 = 2 * xs5
    xs6 = np.linspace(-2, -4, 30)
    ys6 = (np.log(2) - 16) / 4 * (xs6 + 2) - 4
    xs7 = np.linspace(-4, -2, 50)
    ys7 = _C7(xs7)
    xs8 = np.linspace(-2, 0, 30)
    ys8 = xs8 + 3

    px = np.concatenate([xs1, xs2, xs3, xs4, xs5, xs6, xs7, xs8])
    py = np.concatenate([ys1, ys2, ys3, ys4, ys5, ys6, ys7, ys8])
    ax.fill(px, py, color="tab:blue", alpha=0.15)

    # Annotate
    ax.annotate(r"area $= 30 - 3 \ln 2$", (0, -1), fontsize=14, ha="center",
                color="tab:blue", weight="bold")

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 4)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title("Area enclosed by the curve $C$", fontsize=12)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 6 — Bisecting line y = -10(x - k)
# ===


def make_bisect_line(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 8))

    _draw_C(ax)

    # The line y = -10(x - k) for k = (√2739 - 49)/20
    k = (np.sqrt(2739) - 49) / 20
    xs_line = np.linspace(-5, 5, 100)
    ys_line = -10 * (xs_line - k)
    mask = (ys_line >= -5) & (ys_line <= 5)
    ax.plot(xs_line[mask], ys_line[mask], color="tab:red", linewidth=2.5,
            label=rf"$y = -10(x - k)$  with $k = \frac{{\sqrt{{2739}} - 49}}{{20}}$")

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 4)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title("Line bisecting the area enclosed by $C$", fontsize=12)
    ax.legend(loc="upper right", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 7 — g(a) count
# ===


def make_g_count(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))

    # g(a): number of intersections of y = ax with C for a in [-1, 1]
    a1 = 1 - np.log(2) / 8  # slope from origin to (4, 4 - ln 2 / 2)
    a_half = 0.5

    # Piecewise constant g(a)
    a_grid = np.linspace(-1.05, 1.05, 1000)
    g = np.zeros_like(a_grid)
    for i, a in enumerate(a_grid):
        if abs(a) > 1 or abs(a) > a1:
            g[i] = 2 if abs(a) <= 1 else 0
        elif abs(a) == a1:
            g[i] = 3
        elif a_half < abs(a) < a1:
            g[i] = 4
        elif abs(a) == a_half:
            g[i] = 3
        else:
            g[i] = 2

    # Use exact discontinuity values
    # For plot, use thin step
    a_vals = np.array([-1.05, -a1 - 1e-6, -a1 + 1e-6, -a_half - 1e-6, -a_half + 1e-6,
                       a_half - 1e-6, a_half + 1e-6, a1 - 1e-6, a1 + 1e-6, 1.05])
    g_vals = np.array([2, 2, 4, 4, 2, 2, 4, 4, 2, 2])

    ax.step(a_vals, g_vals, where="post", color="tab:blue", linewidth=2.2)

    # Mark discontinuities
    for a_d, label in [(-a1, r"$-a_1$"), (-a_half, r"$-\frac{1}{2}$"),
                       (a_half, r"$\frac{1}{2}$"), (a1, r"$a_1 = 1 - \frac{\ln 2}{8}$")]:
        ax.axvline(a_d, color="tab:red", linewidth=0.8, linestyle=":")
        ax.annotate(label, (a_d, 4.5), fontsize=11, ha="center", color="tab:red")

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(0, 5)
    ax.set_xlabel(r"$a$", fontsize=11)
    ax.set_ylabel(r"$g(a)$  (intersections of $y = ax$ with $C$)", fontsize=11)
    ax.set_title(r"$g(a)$ has 4 discontinuities — at $a = \pm a_1$ and $a = \pm \frac{1}{2}$", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 8 — f(t) discontinuities for line ℓ_t
# ===


def make_l_count(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))

    # Discontinuity points of f(t)
    t1 = 1 / 3
    t2 = 1
    t4 = 1 + 3 * np.log(2) / 8
    t5 = (21 + 6 * np.log(1.5)) / 16
    t6 = 5

    # f(t) values from the table in the answer key
    t_breaks = [0, t1 - 0.001, t1, t1 + 0.001, t2 - 0.001, t2, t2 + 0.001,
                5 / 4 - 0.001, 5 / 4, 5 / 4 + 0.001, t4 - 0.001, t4, t4 + 0.001,
                t5 - 0.001, t5, t5 + 0.001, t6 - 0.001, t6, t6 + 0.001, 5.5]
    f_vals = [2, 2, 3, 4, 4, 3, 2, 2, 2, 2, 2, 3, 4, 4, 3, 2, 2, 1, 0, 0]

    ax.plot(t_breaks, f_vals, color="tab:blue", linewidth=2)

    # Discontinuity markers
    for td, label in [(t1, r"$\frac{1}{3}$"), (t2, r"$1$"),
                      (t4, r"$1 + \frac{3\ln 2}{8}$"),
                      (t5, r"$\frac{21 + 6\ln\frac{3}{2}}{16}$"),
                      (t6, r"$5$")]:
        ax.axvline(td, color="tab:red", linewidth=0.8, linestyle=":")
        ax.annotate(label, (td, 4.5), fontsize=10, ha="center", color="tab:red")

    ax.set_xlim(0, 5.5)
    ax.set_ylim(-0.5, 5)
    ax.set_xlabel(r"$t$  ($x$-intercept of line $\ell_t$, slope $4/3$)", fontsize=11)
    ax.set_ylabel(r"$f(t)$", fontsize=11)
    ax.set_title(r"$f(t)$ — count of intersections of $\ell_t$ with $C$. 5 discontinuities.", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Entry point
# ===

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    make_arclength_trick(out_dir / "example1_arc_length_trick.png")
    make_area_bisect(out_dir / "example2_area_bisect.png")
    make_C_curve(out_dir / "exercise_C_curve.png")
    make_lengths(out_dir / "exercise1_lengths.png")
    make_area(out_dir / "exercise2_area.png")
    make_bisect_line(out_dir / "exercise3_bisect_line.png")
    make_g_count(out_dir / "exercise4_g_count.png")
    make_l_count(out_dir / "exercise5_l_count.png")
    print(f"Wrote figures to {out_dir}")
