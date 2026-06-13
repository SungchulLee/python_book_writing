"""Figures for vector_lattice_inner_product.md.

Generates PNGs in this directory:

- ``example1_hex_lattice.png``     : honeycomb lattice with side length 1
  used as the underlying graphene structure.
- ``example2_dot_product_sign.png``: geometric meaning of the dot product
  sign — acute, right, obtuse angle.
- ``exercise1_twelve_vectors.png`` : the 12 basis vectors at the origin —
  6 A-type (length √3) and 6 B-type (length 3).
- ``exercise2_F1_and_choice.png``  : F₁ = (-√3/2, -5/2) and the six basis
  vectors with positive dot product; the one with smallest positive dot
  product highlighted.
- ``exercise2_dot_table.png``      : bar chart of u · F₁ over the 12 basis
  vectors, with positive ones colored differently.
- ``exercise3_F2_and_reverse.png`` : F₂ = 3F₁ + (√3·k, 0) for k = 2 and the
  reversal of motion direction at this k.

Run with ``python vector_lattice_inner_product_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.patches import FancyArrowPatch


# ===
# Hexagonal lattice utilities
# ===


def _hex_centers(radius_rings: int):
    """Centers of hexagons in a graphene-like honeycomb lattice."""
    centers = []
    # hex grid with hex side = 1, distance between adjacent hex centers = √3
    for i in range(-radius_rings, radius_rings + 1):
        for j in range(-radius_rings, radius_rings + 1):
            cx = np.sqrt(3) * (i + 0.5 * j)
            cy = 1.5 * j
            if cx**2 + cy**2 < (radius_rings * 1.6) ** 2:
                centers.append((cx, cy))
    return centers


def _draw_hex(ax, cx, cy, edge_color="lightgray", linewidth=0.7):
    """Draw a regular hexagon of side 1 at center (cx, cy)."""
    angles = np.linspace(0, 2 * np.pi, 7) + np.pi / 6
    xs = cx + np.cos(angles)
    ys = cy + np.sin(angles)
    ax.plot(xs, ys, color=edge_color, linewidth=linewidth)


def _draw_lattice(ax, radius_rings=3):
    for cx, cy in _hex_centers(radius_rings):
        _draw_hex(ax, cx, cy)


# ===
# Figure 1 — Hexagonal lattice
# ===


def make_hex_lattice(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 7))

    _draw_lattice(ax, radius_rings=3)

    # Mark origin
    ax.plot(0, 0, "o", color="tab:red", markersize=9)
    ax.annotate(r"$(0, 0)$", (0, 0), xytext=(8, 8), textcoords="offset points", fontsize=11)

    # Indicate "side length = 1"
    ax.annotate("", xy=(-np.sqrt(3) / 2 + np.cos(np.pi / 6),
                        -1.5 + np.sin(np.pi / 6)),
                xytext=(-np.sqrt(3) / 2 + np.cos(np.pi / 2),
                        -1.5 + np.sin(np.pi / 2)),
                arrowprops=dict(arrowstyle="<->", color="black"))
    ax.annotate("side = 1", (-2.7, -1.0), fontsize=10)

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"Honeycomb lattice — hexagons of side 1", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 2 — Dot product sign (geometric meaning)
# ===


def make_dot_product_sign(out_path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))

    cases = [
        (60, "Acute angle:  $\\vec{u}\\cdot\\vec{v} > 0$", "tab:green"),
        (90, "Right angle:  $\\vec{u}\\cdot\\vec{v} = 0$", "tab:orange"),
        (135, "Obtuse angle:  $\\vec{u}\\cdot\\vec{v} < 0$", "tab:red"),
    ]

    for ax, (deg, title, col) in zip(axes, cases):
        rad = np.radians(deg)
        u = np.array([2.5, 0])
        v = 2.0 * np.array([np.cos(rad), np.sin(rad)])

        # Vectors
        ax.add_patch(FancyArrowPatch((0, 0), u, color="tab:blue",
                                     arrowstyle="-|>", mutation_scale=15, linewidth=2.2))
        ax.add_patch(FancyArrowPatch((0, 0), v, color="tab:red",
                                     arrowstyle="-|>", mutation_scale=15, linewidth=2.2))

        ax.annotate(r"$\vec{u}$", u, xytext=(8, -8), textcoords="offset points",
                    fontsize=13, color="tab:blue")
        ax.annotate(r"$\vec{v}$", v, xytext=(8, 5), textcoords="offset points",
                    fontsize=13, color="tab:red")

        # Angle arc
        thetas = np.linspace(0, rad, 30)
        arc_r = 0.5
        ax.plot(arc_r * np.cos(thetas), arc_r * np.sin(thetas), color="gray", linewidth=1.5)
        ax.annotate(rf"${deg}^\circ$", (arc_r * 0.7 * np.cos(rad / 2), arc_r * 0.7 * np.sin(rad / 2)),
                    fontsize=10, ha="center", va="center")

        ax.axhline(0, color="black", linewidth=0.5)
        ax.axvline(0, color="black", linewidth=0.5)
        ax.set_xlim(-2.5, 3)
        ax.set_ylim(-1, 2.5)
        ax.set_aspect("equal")
        ax.set_title(title, fontsize=11, color=col)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# The 12 basis vectors
# ===


def _basis_vectors():
    """Return (A_vectors, B_vectors) at the origin (12 total)."""
    # A type: length √3, at angles 0, 60, 120, 180, 240, 300 degrees (offset 30°)
    # Actually from the problem's example diagram, A type vectors point along
    # directions like (√3, 0), (√3/2, 3/2), (-√3/2, 3/2), (-√3, 0), (-√3/2, -3/2), (√3/2, -3/2)
    A = [
        (np.sqrt(3), 0),
        (np.sqrt(3) / 2, 1.5),
        (-np.sqrt(3) / 2, 1.5),
        (-np.sqrt(3), 0),
        (-np.sqrt(3) / 2, -1.5),
        (np.sqrt(3) / 2, -1.5),
    ]
    # B type: length 3, at angles offset 30° from A: 30, 90, 150, 210, 270, 330
    B = [
        (3 * np.sqrt(3) / 2, 1.5),
        (0, 3),
        (-3 * np.sqrt(3) / 2, 1.5),
        (-3 * np.sqrt(3) / 2, -1.5),
        (0, -3),
        (3 * np.sqrt(3) / 2, -1.5),
    ]
    return A, B


# ===
# Figure 3 — Twelve basis vectors at origin
# ===


def make_twelve_vectors(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 8))

    _draw_lattice(ax, radius_rings=3)

    A, B = _basis_vectors()

    for v in A:
        ax.add_patch(FancyArrowPatch((0, 0), v, color="tab:red",
                                     arrowstyle="-|>", mutation_scale=12, linewidth=2.0))
    for v in B:
        ax.add_patch(FancyArrowPatch((0, 0), v, color="tab:blue",
                                     arrowstyle="-|>", mutation_scale=12, linewidth=2.0))

    ax.plot(0, 0, "o", color="black", markersize=8)
    ax.annotate(r"$(0, 0)$", (0, 0), xytext=(8, -16), textcoords="offset points", fontsize=11)

    # Legend
    ax.plot([], [], color="tab:red", linewidth=2.5, label=r"A type (6 vectors, length $\sqrt{3}$)")
    ax.plot([], [], color="tab:blue", linewidth=2.5, label=r"B type (6 vectors, length $3$)")

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title("12 basis vectors at origin (6 A-type + 6 B-type)", fontsize=12)
    ax.legend(loc="upper right", fontsize=10)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 4 — F₁ and the chosen vector
# ===


def make_F1_and_choice(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 8))

    _draw_lattice(ax, radius_rings=3)

    A, B = _basis_vectors()
    F1 = np.array([-np.sqrt(3) / 2, -2.5])

    # Draw all 12 basis vectors faintly
    for v in A + B:
        ax.add_patch(FancyArrowPatch((0, 0), v, color="lightgray",
                                     arrowstyle="-|>", mutation_scale=10, linewidth=1.2))

    # Compute dot products and find positives
    positive_vectors = []
    for v in A + B:
        d = v[0] * F1[0] + v[1] * F1[1]
        if d > 0:
            positive_vectors.append((v, d, "A" if v in A else "B"))

    # Draw positive ones in green, except the smallest
    smallest_val = min(d for _, d, _ in positive_vectors)
    for v, d, kind in positive_vectors:
        col = "tab:green"
        lw = 2.0
        if d == smallest_val and kind == "A":
            col = "tab:red"
            lw = 3.5
        ax.add_patch(FancyArrowPatch((0, 0), v, color=col,
                                     arrowstyle="-|>", mutation_scale=14, linewidth=lw))

    # F₁
    ax.add_patch(FancyArrowPatch((0, 0), F1, color="black",
                                 arrowstyle="-|>", mutation_scale=18, linewidth=3))
    ax.annotate(r"$\vec{F_1}$", F1, xytext=(-25, -10), textcoords="offset points",
                fontsize=14, color="black")

    # Annotation
    ax.annotate(r"chosen: $\vec{u} = (-\sqrt{3}, 0)$  (A-type)",
                (-np.sqrt(3) - 0.5, 0.2), fontsize=11, color="tab:red")
    ax.annotate(r"$\vec{u}\cdot\vec{F_1} = 3/2$  (smallest positive)",
                (-4.6, -3.8), fontsize=11, color="tab:red")

    ax.plot(0, 0, "o", color="black", markersize=7)

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"$\vec{F_1} = (-\sqrt{3}/2,\,-5/2)$:  basis vector with min positive $\vec{u}\cdot\vec{F_1}$", fontsize=11)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 5 — Bar chart of dot products
# ===


def make_dot_table(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 5))

    A, B = _basis_vectors()
    F1 = np.array([-np.sqrt(3) / 2, -2.5])

    all_vecs = A + B
    labels = [
        r"$(\sqrt{3},0)$", r"$(\frac{\sqrt{3}}{2},\frac{3}{2})$",
        r"$(-\frac{\sqrt{3}}{2},\frac{3}{2})$", r"$(-\sqrt{3},0)$",
        r"$(-\frac{\sqrt{3}}{2},-\frac{3}{2})$", r"$(\frac{\sqrt{3}}{2},-\frac{3}{2})$",
        r"$(\frac{3\sqrt{3}}{2},\frac{3}{2})$", r"$(0,3)$",
        r"$(-\frac{3\sqrt{3}}{2},\frac{3}{2})$", r"$(-\frac{3\sqrt{3}}{2},-\frac{3}{2})$",
        r"$(0,-3)$", r"$(\frac{3\sqrt{3}}{2},-\frac{3}{2})$",
    ]
    dots = [v[0] * F1[0] + v[1] * F1[1] for v in all_vecs]

    # Colors: positive vs negative; highlight smallest positive
    smallest_positive = min(d for d in dots if d > 0)
    colors = []
    for d in dots:
        if d == smallest_positive:
            colors.append("tab:red")
        elif d > 0:
            colors.append("tab:green")
        else:
            colors.append("lightgray")

    ax.bar(range(12), dots, color=colors)
    ax.set_xticks(range(12))
    ax.set_xticklabels(labels, rotation=45, fontsize=10, ha="right")
    ax.axhline(0, color="black", linewidth=0.8)

    # Annotate smallest positive
    idx = dots.index(smallest_positive)
    ax.annotate(rf"$\min^+ = {smallest_positive:.1f}$", (idx, smallest_positive),
                xytext=(0, 14), textcoords="offset points", fontsize=12,
                color="tab:red", ha="center",
                arrowprops=dict(arrowstyle="->", color="tab:red"))

    ax.set_ylabel(r"$\vec{u}\cdot\vec{F_1}$", fontsize=11)
    ax.set_title(r"Dot product $\vec{u}\cdot\vec{F_1}$ for the 12 basis vectors  ($\vec{F_1} = (-\sqrt{3}/2,\,-5/2)$)", fontsize=11)
    ax.grid(alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 6 — F₂ at k = 2 and reversal
# ===


def make_F2_and_reverse(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 8))

    _draw_lattice(ax, radius_rings=3)

    A, B = _basis_vectors()
    F1 = np.array([-np.sqrt(3) / 2, -2.5])

    k = 2
    F2 = 3 * F1 + np.array([np.sqrt(3) * k, 0])

    # All 12 vectors faint
    for v in A + B:
        ax.add_patch(FancyArrowPatch((0, 0), v, color="lightgray",
                                     arrowstyle="-|>", mutation_scale=10, linewidth=1.2))

    # The reversed direction -u where u = (-√3, 0) so -u = (√3, 0)
    minus_u = (np.sqrt(3), 0)
    ax.add_patch(FancyArrowPatch((0, 0), minus_u, color="tab:red",
                                 arrowstyle="-|>", mutation_scale=16, linewidth=3.5))
    ax.annotate(r"$-\vec{u} = (\sqrt{3}, 0)$", minus_u, xytext=(8, 8),
                textcoords="offset points", fontsize=12, color="tab:red")

    # F₂
    ax.add_patch(FancyArrowPatch((0, 0), F2, color="black",
                                 arrowstyle="-|>", mutation_scale=18, linewidth=3))
    ax.annotate(r"$\vec{F_2} = 3\vec{F_1} + (\sqrt{3}\cdot 2,\,0)$",
                F2, xytext=(8, 8), textcoords="offset points", fontsize=12)

    # Original u direction grayed out
    ax.add_patch(FancyArrowPatch((0, 0), (-np.sqrt(3), 0), color="gray",
                                 arrowstyle="-|>", mutation_scale=14, linewidth=2, linestyle=":"))
    ax.annotate(r"original $\vec{u} = (-\sqrt{3}, 0)$", (-np.sqrt(3), 0),
                xytext=(-30, -20), textcoords="offset points", fontsize=10, color="gray")

    ax.plot(0, 0, "o", color="black", markersize=7)

    # Note
    ax.annotate(r"$k = 2$:  $(-\vec{u})\cdot\vec{F_2} = 3/2 > 0$, min positive",
                (-4.5, -4.5), fontsize=11, color="tab:red")

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"$k = 2$:  electron motion reverses to $-\vec{u}$ direction", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Entry point
# ===

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    make_hex_lattice(out_dir / "example1_hex_lattice.png")
    make_dot_product_sign(out_dir / "example2_dot_product_sign.png")
    make_twelve_vectors(out_dir / "exercise1_twelve_vectors.png")
    make_F1_and_choice(out_dir / "exercise2_F1_and_choice.png")
    make_dot_table(out_dir / "exercise2_dot_table.png")
    make_F2_and_reverse(out_dir / "exercise3_F2_and_reverse.png")
    print(f"Wrote figures to {out_dir}")
