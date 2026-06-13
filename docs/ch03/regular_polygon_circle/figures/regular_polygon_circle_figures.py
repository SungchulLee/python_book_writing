"""Figures for regular_polygon_circle.md.

Generates PNGs in this directory:

- ``example1_polygon.png``         : a regular n-gon inscribed in the unit
  circle with vertices labeled for n = 8.
- ``example2_perpendicular.png``   : perpendicular foot from origin onto a
  chord of the unit circle lies on a smaller circle (Thales).
- ``exercise1_n8_circle.png``      : n = 8 case — the three perpendicular
  feet H_1, H_2, H_3 from origin onto L_1, L_2, L_3 lie on a circle of
  diameter OP_1.
- ``exercise2_geometric_sum.png``  : the geometric series ∑ S_k for the
  scaled circles in the n = 10 case.
- ``exercise3_quadrilateral.png``  : the quadrilateral P_2 A B P_3 for
  n = 12 formed by intersections of ℓ_1, ℓ_2, ℓ_3.
- ``exercise4_lines_m.png``        : the family of lines m_j for n = 16,
  with intersections m_8 ∩ m_j summed.
- ``exercise5_T_n_limit.png``      : the area T_n = ∑ s_i and its limit as
  n → ∞.

Run with ``python regular_polygon_circle_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Circle


# ===
# Helpers
# ===


def _polygon_vertices(n):
    """Vertices of a regular n-gon inscribed in the unit circle with P_1 = (0, 1)."""
    angles = np.pi / 2 - 2 * np.pi * np.arange(n) / n
    return np.column_stack([np.cos(angles), np.sin(angles)])


def _perp_foot(line_a, line_b, origin=(0, 0)):
    """Perpendicular foot from `origin` onto the line through `line_a` and `line_b`."""
    a = np.asarray(line_a, dtype=float)
    b = np.asarray(line_b, dtype=float)
    o = np.asarray(origin, dtype=float)
    d = b - a
    t = np.dot(o - a, d) / np.dot(d, d)
    return a + t * d


# ===
# Figure 1 — Regular n-gon inscribed in unit circle
# ===


def make_polygon(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 7))

    # Unit circle
    theta = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), color="tab:gray", linewidth=1.2)

    n = 8
    V = _polygon_vertices(n)
    poly = Polygon(V, fill=False, edgecolor="tab:blue", linewidth=2.2)
    ax.add_patch(poly)

    for i, (x, y) in enumerate(V):
        ax.plot(x, y, "o", color="tab:red", markersize=7)
        ax.annotate(rf"$P_{{{i+1}}}$", (x, y),
                    xytext=(8, 8) if y >= 0 else (8, -16),
                    textcoords="offset points", fontsize=11)

    ax.plot(0, 0, "x", color="black", markersize=10)
    ax.annotate("O", (0, 0), xytext=(8, -15), textcoords="offset points", fontsize=11)

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(rf"Regular {n}-gon inscribed in unit circle, $P_1 = (0, 1)$", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 2 — Perpendicular foot from origin onto a chord (Thales)
# ===


def make_perpendicular(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 7))

    # Unit circle
    theta = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), color="tab:gray", linewidth=1.2,
            label="unit circle (radius 1)")

    # A point on circle and a chord through it
    P1 = np.array([0, 1])
    P_other = np.array([np.cos(-0.3 * np.pi), np.sin(-0.3 * np.pi)])

    # Draw chord
    ax.plot([P1[0], P_other[0]], [P1[1], P_other[1]], color="tab:blue", linewidth=2,
            label="chord through $P_1$")

    # Perpendicular foot from origin
    H = _perp_foot(P1, P_other)
    ax.plot([0, H[0]], [0, H[1]], color="tab:red", linewidth=1.8, linestyle="--",
            label="perpendicular from O")
    ax.plot(H[0], H[1], "o", color="tab:red", markersize=10)
    ax.annotate("H", H, xytext=(10, 5), textcoords="offset points", fontsize=12)

    # Smaller circle: diameter OP_1
    mid = P1 / 2
    small_circle = Circle(mid, 0.5, fill=False, color="tab:green", linewidth=2,
                          linestyle=":", label="circle with diameter $OP_1$")
    ax.add_patch(small_circle)

    # Mark P_1, O
    ax.plot(*P1, "o", color="black", markersize=8)
    ax.annotate(r"$P_1 = (0, 1)$", P1, xytext=(10, 0), textcoords="offset points", fontsize=11)
    ax.plot(0, 0, "x", color="black", markersize=10)
    ax.annotate("O", (0, 0), xytext=(-20, -5), textcoords="offset points", fontsize=11)

    # Right angle marker at H
    ax.annotate("⌐", H, xytext=(-5, 5), textcoords="offset points",
                fontsize=10, rotation=np.degrees(np.arctan2(H[1], H[0])))

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"Thales:  $\angle OHP_1 = 90°$ ⟹ $H$ lies on circle with diameter $OP_1$", fontsize=11)
    ax.legend(loc="lower left", fontsize=9)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 3 — n = 8: three perpendicular feet on a single small circle
# ===


def make_n8_circle(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 7))

    n = 8
    V = _polygon_vertices(n)

    # Unit circle
    theta = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), color="tab:gray", linewidth=1.0)

    P1 = V[0]

    # Three lines L_1, L_2, L_3 through P_1 to P_2, P_3, P_4
    for i, (label, idx, color) in enumerate(
        [(r"$L_1$", 1, "tab:blue"), (r"$L_2$", 2, "tab:green"), (r"$L_3$", 3, "tab:purple")]
    ):
        P_other = V[idx]
        # Extend line beyond endpoints
        d = P_other - P1
        ext_a = P1 - 0.3 * d
        ext_b = P_other + 0.3 * d
        ax.plot([ext_a[0], ext_b[0]], [ext_a[1], ext_b[1]], color=color, linewidth=1.5)
        ax.annotate(label, ext_b, xytext=(5, 5), textcoords="offset points",
                    fontsize=11, color=color)

        # Perpendicular foot
        H = _perp_foot(P1, P_other)
        ax.plot([0, H[0]], [0, H[1]], color=color, linewidth=1, linestyle=":")
        ax.plot(H[0], H[1], "o", color=color, markersize=10)
        ax.annotate(rf"$H_{{{i+1}}}$", H, xytext=(8, 5), textcoords="offset points",
                    fontsize=12, color=color)

    # Small circle: diameter OP_1
    small_circle = Circle(P1 / 2, 0.5, fill=False, color="tab:red", linewidth=2.5,
                          linestyle="--")
    ax.add_patch(small_circle)
    ax.annotate(r"$x^2 + (y - 1/2)^2 = 1/4$",
                (0.55, 0.55), fontsize=11, color="tab:red")

    # Vertices
    for i, v in enumerate(V):
        if i < 4:
            ax.plot(*v, "o", color="black", markersize=6)
            ax.annotate(rf"$P_{{{i+1}}}$", v, xytext=(8, 5), textcoords="offset points", fontsize=10)
        else:
            ax.plot(*v, "o", color="lightgray", markersize=4)

    ax.plot(0, 0, "x", color="black", markersize=10)
    ax.annotate("O", (0, 0), xytext=(8, -15), textcoords="offset points", fontsize=11)

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.set_title(r"$n = 8$:  $H_1, H_2, H_3$ all lie on circle with diameter $OP_1$", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 4 — Geometric sum ∑ S_k
# ===


def make_geometric_sum(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    K = 8
    ks = np.arange(1, K + 1)
    S = (9 / 4) * (4 / 81) ** ks * np.pi

    # Partial sums
    partial = np.cumsum(S)
    total = (1 / 9) * np.pi / (1 - 4 / 81)  # = 9π/77

    ax.bar(ks, S, color="tab:blue", alpha=0.6, label=r"$S_k$ (individual term)")
    ax.plot(ks, partial, "o-", color="tab:red", linewidth=2, markersize=8,
            label=r"partial sum $\sum_{j=1}^k S_j$")
    ax.axhline(total, color="tab:green", linewidth=1.8, linestyle="--",
               label=rf"$\sum_{{k=1}}^\infty S_k = \frac{{9}}{{77}}\pi \approx {total:.4f}$")

    ax.set_xlabel(r"$k$", fontsize=11)
    ax.set_ylabel("Area", fontsize=11)
    ax.set_title(r"Geometric series:  $S_k = \frac{9}{4}\left(\frac{4}{81}\right)^k \pi$", fontsize=12)
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 5 — n = 12 quadrilateral P_2 A B P_3
# ===


def make_quadrilateral(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 7))

    n = 12
    V = _polygon_vertices(n)

    # Unit circle
    theta = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), color="tab:gray", linewidth=1.0)

    # Three lines ℓ_1 (P_1, P_4), ℓ_2 (P_2, P_5), ℓ_3 (P_3, P_6)
    lines = [
        (V[0], V[3], "tab:blue", r"$\ell_1$"),
        (V[1], V[4], "tab:green", r"$\ell_2$"),
        (V[2], V[5], "tab:purple", r"$\ell_3$"),
    ]

    def _intersection(p1, p2, p3, p4):
        x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(d) < 1e-12:
            return None
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
        return np.array([x1 + t * (x2 - x1), y1 + t * (y2 - y1)])

    A = _intersection(*lines[0][:2], *lines[1][:2])
    B = _intersection(*lines[0][:2], *lines[2][:2])

    for p_a, p_b, color, label in lines:
        d = p_b - p_a
        ext_a = p_a - 0.3 * d
        ext_b = p_b + 0.3 * d
        ax.plot([ext_a[0], ext_b[0]], [ext_a[1], ext_b[1]], color=color, linewidth=1.5,
                label=label)

    # Mark A, B
    ax.plot(*A, "o", color="tab:red", markersize=10)
    ax.annotate("A", A, xytext=(8, 8), textcoords="offset points", fontsize=14, color="tab:red")
    ax.plot(*B, "o", color="tab:red", markersize=10)
    ax.annotate("B", B, xytext=(8, -16), textcoords="offset points", fontsize=14, color="tab:red")

    # Quadrilateral P_2 A B P_3
    quad = Polygon([V[1], A, B, V[2]], fill=True, facecolor="tab:orange", alpha=0.3,
                   edgecolor="tab:red", linewidth=2)
    ax.add_patch(quad)

    for i, v in enumerate(V):
        ax.plot(*v, "o", color="black", markersize=5)
        if i < 6:
            ax.annotate(rf"$P_{{{i+1}}}$", v, xytext=(8, 5), textcoords="offset points", fontsize=10)

    ax.plot(0, 0, "x", color="black", markersize=10)

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.set_title(r"$n = 12$:  quadrilateral $P_2 A B P_3$ formed by $\ell_1, \ell_2, \ell_3$", fontsize=11)
    ax.legend(loc="lower left", fontsize=10)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 6 — Lines m_j and intersections
# ===


def make_lines_m(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 7))

    n = 16
    # m_j: line through (j/n, 0) and (0, (n-j)/n)
    for j in range(1, n):
        a = np.array([j / n, 0])
        b = np.array([0, (n - j) / n])
        if j == n // 2:
            color = "tab:red"
            lw = 2.5
            label = rf"$m_{{{j}}}$  (the special line)"
        else:
            color = "tab:blue"
            lw = 0.9
            label = None
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, linewidth=lw,
                label=label if j in [n // 2, 1] else None)
        if j == 1:
            ax.plot([a[0], b[0]], [a[1], b[1]], color=color, linewidth=lw,
                    label=r"$m_j$, $j \neq n/2$")

    ax.set_xlim(-0.05, 1.1)
    ax.set_ylim(-0.05, 1.1)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(rf"$n = {n}$:  family of lines $m_j$  ($j = 1, \ldots, {n-1}$)", fontsize=11)
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 7 — T_n → 1/6
# ===


def make_T_n_limit(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    ns = np.arange(3, 50)
    # T_n = sum_{i=1}^{n-1} s_i where s_i = ((n-i+1)(n-i)) / (2 n^3)
    # plus s_1 = (n-1)/(2n^2)
    # Actually from the solution: T_n = (n-1)/(2n^2) + n(n-1)(n-2)/(6n^3)
    T = (ns - 1) / (2 * ns**2) + ns * (ns - 1) * (ns - 2) / (6 * ns**3)

    ax.plot(ns, T, "o-", color="tab:blue", linewidth=2, markersize=6,
            label=r"$T_n = \sum_{i=1}^{n-1} s_i$")
    ax.axhline(1 / 6, color="tab:red", linewidth=1.8, linestyle="--",
               label=r"$\lim_{n \to \infty} T_n = \frac{1}{6}$")

    ax.set_xlabel(r"$n$", fontsize=11)
    ax.set_ylabel(r"$T_n$", fontsize=11)
    ax.set_title(r"$T_n$ converges to $\frac{1}{6}$ as $n \to \infty$", fontsize=12)
    ax.legend(loc="lower right", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Entry point
# ===

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    make_polygon(out_dir / "example1_polygon.png")
    make_perpendicular(out_dir / "example2_perpendicular.png")
    make_n8_circle(out_dir / "exercise1_n8_circle.png")
    make_geometric_sum(out_dir / "exercise2_geometric_sum.png")
    make_quadrilateral(out_dir / "exercise3_quadrilateral.png")
    make_lines_m(out_dir / "exercise4_lines_m.png")
    make_T_n_limit(out_dir / "exercise5_T_n_limit.png")
    print(f"Wrote figures to {out_dir}")
