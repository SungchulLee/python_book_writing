"""Figures for integration_by_substitution.md.

Generates PNGs in this directory:

- ``example1_substitution.png``  : area under 2x·e^(x²) on [0,1] vs area under
  e^u on [0,1] — both equal e - 1.
- ``example2_inverse.png``       : g(u) = u³ on u ≥ 0 and its inverse
  h(x) = ∛x as reflections across y = x.
- ``exercise2_extremum.png``     : f(x) = ∫₀ˣ (t-a) eᵗ dt for a = 1, showing
  the local minimum at x = a.
- ``exercise2_signs.png``        : sign analysis of f'(x) = (x-a) e^x.
- ``exercise4_inverse.png``      : g(x) = 1 + x - e^x on x ≥ 0 (decreasing
  from 0 to m = 3 - e²) and its inverse h.
- ``exercise5_setup.png``        : equilateral triangle T with centroid at
  (x, k(x)), top vertex 2 above, and the small similar piece above the
  x-axis (shaded).
- ``exercise5_cases.png``        : triangle T for x = -1, 0, 1 — showing
  how the cut-off piece is largest at x = 0.
- ``exercise5_k_plot.png``       : k(x) = -2 + √(2 + x - e^x) on [-1, 1]
  with maximum at (0, -1).

Run with ``python substitution_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon


# ===
# Figure 1 — Example 1: substitution u = x² preserves area
# ===


def make_example1(out_path: Path) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))

    # Left: y = 2x e^(x²) on [0, 1]
    xs = np.linspace(0, 1, 200)
    ys = 2 * xs * np.exp(xs**2)
    ax1.fill_between(xs, ys, alpha=0.3, color="tab:blue")
    ax1.plot(xs, ys, color="tab:blue", linewidth=2)
    ax1.axhline(0, color="black", linewidth=0.6)
    ax1.axvline(0, color="black", linewidth=0.6)
    ax1.set_xlim(-0.08, 1.18)
    ax1.set_ylim(-0.4, 6.2)
    ax1.set_title(r"$\int_0^1 2x\,e^{x^2}\,dx$", fontsize=12)
    ax1.set_xlabel(r"$x$", fontsize=11)
    ax1.annotate(
        r"$y = 2x\,e^{x^2}$",
        (0.65, 4.0),
        fontsize=12,
        color="tab:blue",
    )
    ax1.annotate(r"area $= e - 1$", (0.18, 1.0), fontsize=11)

    # Right: y = e^u on [0, 1]
    us = np.linspace(0, 1, 200)
    vs = np.exp(us)
    ax2.fill_between(us, vs, alpha=0.3, color="tab:green")
    ax2.plot(us, vs, color="tab:green", linewidth=2)
    ax2.axhline(0, color="black", linewidth=0.6)
    ax2.axvline(0, color="black", linewidth=0.6)
    ax2.set_xlim(-0.08, 1.18)
    ax2.set_ylim(-0.2, 3.1)
    ax2.set_title(r"$\int_0^1 e^u\,du$", fontsize=12)
    ax2.set_xlabel(r"$u$", fontsize=11)
    ax2.annotate(
        r"$y = e^u$",
        (0.65, 2.05),
        fontsize=12,
        color="tab:green",
    )
    ax2.annotate(r"area $= e - 1$", (0.15, 0.55), fontsize=11)

    # Arrow between
    fig.suptitle(r"$u = x^2$: same area, two coordinates", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 2 — Example 2: g(u) = u³ and inverse h(x) = ∛x
# ===


def make_example2(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))

    # y = x reference line
    t = np.linspace(-0.3, 3.6, 100)
    ax.plot(t, t, color="gray", linestyle="--", linewidth=0.9)
    ax.annotate(r"$y = x$", (3.0, 3.15), fontsize=10, color="gray")

    # g(u) = u³ on u ∈ [0, 1.5]
    us = np.linspace(0, 1.55, 100)
    ax.plot(us, us**3, color="tab:blue", linewidth=2.2)
    ax.annotate(
        r"$g(u) = u^3$",
        (1.45, 3.0),
        fontsize=12,
        color="tab:blue",
    )

    # h(x) = ∛x on x ∈ [0, 3.4]
    xs = np.linspace(0, 3.4, 100)
    ax.plot(xs, xs ** (1 / 3), color="tab:red", linewidth=2.2)
    ax.annotate(
        r"$h(x) = \sqrt[3]{x}$",
        (2.7, 1.65),
        fontsize=12,
        color="tab:red",
    )

    # Sample point pair
    a = 1.2
    ax.plot(a, a**3, "o", color="tab:blue", markersize=7)
    ax.annotate(
        r"$(u,\,g(u))$",
        (a, a**3),
        xytext=(8, -2),
        textcoords="offset points",
        fontsize=11,
        color="tab:blue",
    )
    ax.plot(a**3, a, "o", color="tab:red", markersize=7)
    ax.annotate(
        r"$(g(u),\,u)$",
        (a**3, a),
        xytext=(8, -2),
        textcoords="offset points",
        fontsize=11,
        color="tab:red",
    )
    ax.plot([a, a**3], [a**3, a], color="gray", linestyle=":", linewidth=1.0)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-0.3, 3.7)
    ax.set_ylim(-0.3, 3.7)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$u$", fontsize=11)
    ax.set_title(r"Inverse functions: reflection across $y = x$", fontsize=11)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 3 — Exercise 2: f(x) for a = 1 with extremum at x = a
# ===


def make_exercise2(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))

    a = 1.0
    xs = np.linspace(-0.5, 2.5, 300)
    ys = (xs - a - 1) * np.exp(xs) + a + 1

    ax.plot(xs, ys, color="tab:blue", linewidth=2.2)
    ax.annotate(
        r"$f(x) = \int_0^x (t-a)\,e^t\,dt$",
        (1.55, -0.8),
        fontsize=12,
        color="tab:blue",
    )

    fmin = 1 + a - np.exp(a)
    ax.plot(a, fmin, "o", color="tab:red", markersize=8)
    ax.annotate(
        r"local min: $f(a) = 1 + a - e^a$",
        (a, fmin),
        xytext=(15, -20),
        textcoords="offset points",
        fontsize=11,
        color="tab:red",
        arrowprops=dict(arrowstyle="->", color="tab:red"),
    )

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.axvline(a, color="gray", linestyle="--", linewidth=0.8)
    ax.annotate(r"$x = a$", (a + 0.04, 1.3), fontsize=11, color="gray")

    ax.set_xlim(-0.6, 2.6)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_title(rf"Local minimum at $x = a$ (illustrated with $a = {a:.0f}$)", fontsize=11)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 4 — Exercise 2 supplement: sign of f'(x) = (x - a) e^x
# ===


def make_exercise2_signs(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 2.6))

    a = 1.0
    xs = np.linspace(-0.5, 2.5, 300)
    deriv = (xs - a) * np.exp(xs)

    # Shade f' < 0 (left of a) and f' > 0 (right of a)
    ax.fill_between(xs, deriv, 0, where=(deriv < 0), color="tab:red", alpha=0.25)
    ax.fill_between(xs, deriv, 0, where=(deriv > 0), color="tab:green", alpha=0.25)
    ax.plot(xs, deriv, color="black", linewidth=1.8)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(a, color="gray", linestyle="--", linewidth=0.8)

    ax.annotate(r"$f'(x) < 0$", (0.0, -1.0), fontsize=11, color="tab:red")
    ax.annotate(r"$f'(x) > 0$", (1.55, 1.5), fontsize=11, color="tab:green")
    ax.annotate(
        r"$f'(a) = 0$",
        (a, 0),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=10,
    )

    ax.set_xlim(-0.6, 2.6)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_title(r"Sign of $f'(x) = (x - a)\,e^x$ — sign change at $x = a$", fontsize=11)
    ax.set_yticks([])

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 5 — Exercise 4: g and h
# ===


def make_exercise4(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 6.5))

    # y = x reference
    t = np.linspace(-5, 3, 100)
    ax.plot(t, t, color="gray", linestyle="--", linewidth=0.8)
    ax.annotate(r"$y = x$", (2.4, 2.55), fontsize=10, color="gray")

    # g(x) = 1 + x - e^x on x ∈ [0, 2.5]
    xs = np.linspace(0, 2.5, 200)
    gs = 1 + xs - np.exp(xs)
    ax.plot(xs, gs, color="tab:blue", linewidth=2.2)
    ax.annotate(r"$g(x) = 1 + x - e^x$", (1.45, -1.4), fontsize=12, color="tab:blue")

    # h: inverse, plotted as (g(x), x)
    ax.plot(gs, xs, color="tab:red", linewidth=2.2)
    ax.annotate(r"$h(x)$  (inverse of $g$)", (-3.2, 1.85), fontsize=12, color="tab:red")

    # Key points
    m = 3 - np.exp(2)
    ax.plot(0, 0, "ko", markersize=6)
    ax.annotate(r"$(0,\,0)$", (0, 0), xytext=(6, 8), textcoords="offset points", fontsize=10)

    ax.plot(2, m, "o", color="tab:blue", markersize=7)
    ax.annotate(
        rf"$(2,\,m)$,  $m = 3 - e^2 \approx {m:.2f}$",
        (2, m),
        xytext=(8, 4),
        textcoords="offset points",
        fontsize=10,
        color="tab:blue",
    )

    ax.plot(m, 2, "o", color="tab:red", markersize=7)
    ax.annotate(
        r"$(m,\,2)$",
        (m, 2),
        xytext=(-30, 6),
        textcoords="offset points",
        fontsize=10,
        color="tab:red",
    )

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-5.2, 3.0)
    ax.set_ylim(-5.2, 3.0)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"$g$ on $x \geq 0$ and its inverse $h$ (reflection across $y = x$)", fontsize=11)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Helpers for the equilateral triangle figures
# ===


def _k(x: float) -> float:
    return -2.0 + np.sqrt(2.0 + x - np.exp(x))


def _triangle_vertices(x0: float, k0: float):
    """Vertices of T: side 2√3, centroid (x0, k0), one side parallel to x-axis."""
    top = (x0, k0 + 2.0)
    bl = (x0 - np.sqrt(3.0), k0 - 1.0)
    br = (x0 + np.sqrt(3.0), k0 - 1.0)
    return top, bl, br


def _cut_above_x_axis(top, bl, br):
    """Triangle formed by intersecting T with y ≥ 0, assuming top vertex above x-axis."""
    if top[1] <= 0:
        return None
    h = top[1]  # height of cut piece equals the y-coordinate of top vertex
    # similar triangle with height h: linear interpolation along the two top edges
    s = h / 3.0
    p_left = (top[0] - s * np.sqrt(3.0), 0.0)
    p_right = (top[0] + s * np.sqrt(3.0), 0.0)
    return top, p_left, p_right


# ===
# Figure 6 — Exercise 5 setup: single triangle with centroid, top vertex, cut piece
# ===


def make_exercise5_setup(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 6.5))

    x0 = -0.4
    k0 = _k(x0)
    top, bl, br = _triangle_vertices(x0, k0)

    # Full triangle T (outline)
    tri = Polygon([top, bl, br], fill=False, edgecolor="black", linewidth=1.6)
    ax.add_patch(tri)

    # Cut piece above x-axis (shaded)
    cut = _cut_above_x_axis(top, bl, br)
    if cut is not None:
        cut_poly = Polygon(
            list(cut),
            fill=True,
            facecolor="tab:blue",
            edgecolor="tab:blue",
            alpha=0.35,
            linewidth=1.5,
        )
        ax.add_patch(cut_poly)

    # x-axis
    ax.axhline(0, color="black", linewidth=1.0)

    # Centroid + top vertex
    ax.plot(x0, k0, "ko", markersize=6)
    ax.annotate(
        r"centroid $(x,\,k(x))$",
        (x0, k0),
        xytext=(10, -4),
        textcoords="offset points",
        fontsize=11,
    )
    ax.plot(*top, "ko", markersize=6)
    ax.annotate(
        r"top vertex $(x,\,k(x) + 2)$",
        top,
        xytext=(10, 6),
        textcoords="offset points",
        fontsize=11,
    )

    # Distance arrow centroid → top vertex
    ax.annotate(
        "",
        xy=top,
        xytext=(x0, k0),
        arrowprops=dict(arrowstyle="<->", color="gray", linewidth=1.2),
    )
    ax.annotate(r"$2$", (x0 - 0.12, (k0 + top[1]) / 2), fontsize=12, color="gray", ha="right")

    # Side label
    mid_base = ((bl[0] + br[0]) / 2, bl[1] - 0.18)
    ax.annotate(r"side $= 2\sqrt{3}$", mid_base, fontsize=10, ha="center", color="black")

    # Cut piece label
    if cut is not None:
        cx = (cut[0][0] + cut[1][0] + cut[2][0]) / 3
        cy = (cut[0][1] + cut[1][1] + cut[2][1]) / 3
        ax.annotate(
            r"$A(x)$",
            (cx, cy),
            fontsize=12,
            color="tab:blue",
            ha="center",
        )

    # x-axis label
    ax.annotate(r"$x$-axis", (3.2, 0.18), fontsize=11)

    ax.set_xlim(-3.0, 3.5)
    ax.set_ylim(-3.5, 1.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(
        rf"Triangle $T$ with centroid at $(x,\,k(x))$  (here $x = {x0}$)",
        fontsize=11,
    )
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 7 — Exercise 5: triangle T for x = -1, 0, 1 (cut piece largest at x = 0)
# ===


def make_exercise5_cases(out_path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.8))

    for ax, x0 in zip(axes, (-1.0, 0.0, 1.0)):
        k0 = _k(x0)
        top, bl, br = _triangle_vertices(x0, k0)

        tri = Polygon([top, bl, br], fill=False, edgecolor="black", linewidth=1.4)
        ax.add_patch(tri)

        cut = _cut_above_x_axis(top, bl, br)
        if cut is not None:
            cut_poly = Polygon(
                list(cut),
                fill=True,
                facecolor="tab:blue",
                edgecolor="tab:blue",
                alpha=0.35,
                linewidth=1.3,
            )
            ax.add_patch(cut_poly)

        ax.axhline(0, color="black", linewidth=0.8)
        ax.plot(x0, k0, "ko", markersize=4)
        ax.plot(*top, "ko", markersize=4)

        ax.set_xlim(x0 - 2.3, x0 + 2.3)
        ax.set_ylim(-3.6, 1.6)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(
            rf"$x = {int(x0)}$,  top at height $k(x)+2 = {top[1]:.3f}$",
            fontsize=11,
        )
        for s in ("top", "right", "left", "bottom"):
            ax.spines[s].set_visible(False)

    fig.suptitle(
        r"Cut piece above the $x$-axis is largest at $x = 0$  ($k(0) + 2 = 1$)",
        fontsize=12,
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 8 — Exercise 5: k(x) graph
# ===


def make_exercise5_k_plot(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    xs = np.linspace(-1, 1, 300)
    ks = -2 + np.sqrt(2 + xs - np.exp(xs))

    ax.plot(xs, ks, color="tab:blue", linewidth=2.2)
    ax.fill_between(xs, ks, -1.55, color="tab:blue", alpha=0.08)

    # Max
    ax.plot(0, -1, "o", color="tab:red", markersize=9)
    ax.annotate(
        r"maximum: $(0,\,-1)$",
        (0, -1),
        xytext=(20, -8),
        textcoords="offset points",
        fontsize=12,
        color="tab:red",
        arrowprops=dict(arrowstyle="->", color="tab:red"),
    )

    # Endpoint values
    k_left = -2 + np.sqrt(2 - 1 - np.exp(-1))
    k_right = -2 + np.sqrt(3 - np.exp(1))
    ax.plot(-1, k_left, "ko", markersize=5)
    ax.annotate(
        rf"$k(-1) \approx {k_left:.3f}$",
        (-1, k_left),
        xytext=(8, -4),
        textcoords="offset points",
        fontsize=10,
    )
    ax.plot(1, k_right, "ko", markersize=5)
    ax.annotate(
        rf"$k(1) \approx {k_right:.3f}$",
        (1, k_right),
        xytext=(-95, -4),
        textcoords="offset points",
        fontsize=10,
    )

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="gray", linewidth=0.6, linestyle="--")
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.6, -0.6)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$k(x)$", fontsize=11)
    ax.set_title(r"$k(x) = -2 + \sqrt{2 + x - e^x}$  on  $[-1,\,1]$", fontsize=12)
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Entry point
# ===

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    make_example1(out_dir / "example1_substitution.png")
    make_example2(out_dir / "example2_inverse.png")
    make_exercise2(out_dir / "exercise2_extremum.png")
    make_exercise2_signs(out_dir / "exercise2_signs.png")
    make_exercise4(out_dir / "exercise4_inverse.png")
    make_exercise5_setup(out_dir / "exercise5_setup.png")
    make_exercise5_cases(out_dir / "exercise5_cases.png")
    make_exercise5_k_plot(out_dir / "exercise5_k_plot.png")
    print(f"Wrote figures to {out_dir}")
