"""Figures for space_projection_dot_product.md.

Generates PNGs in this directory:

- ``example1_projection.png``     : a point B in space and its projection B'
  onto plane α; B'B = perpendicular distance.
- ``example2_dot_product.png``    : geometric meaning of the dot product of
  two 2D vectors (projection times magnitude).
- ``exercise1_setup.png``         : A'B = 10, BB' = 5√3, R divides A'B
  with ratio t : (5 - t), R' is projection of R onto plane α.
- ``exercise1_triangle.png``      : the resulting triangle △ on plane α
  (base 2, height 1, area 1) — two possible orientations relative to A'B'.
- ``exercise2_T_projection.png``  : the projection T' = circle C ∪ two
  tangent segments l₁, l₂; the path T sits on a sphere O of radius √2.
- ``exercise2_inner_cases.png``   : an 8-case grid for case 2 of the inner
  product I = P₁'Q₁' · P₂'Q₂'.

Run with ``python space_projection_dot_product_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Polygon


# ===
# Figure 1 — Projection of a 3D point onto a plane
# ===


def make_projection(out_path: Path) -> None:
    fig = plt.figure(figsize=(7.5, 5))
    ax = fig.add_subplot(111, projection="3d")

    # Plane α (z = 0)
    xs, ys = np.meshgrid(np.linspace(-2, 4, 10), np.linspace(-2, 3, 10))
    zs = np.zeros_like(xs)
    ax.plot_surface(xs, ys, zs, alpha=0.18, color="tab:blue")

    # Points
    A = np.array([0, 0, 0])
    Bp = np.array([2.5, 1.5, 0])
    B = np.array([2.5, 1.5, 2])

    # Line from B to B'
    ax.plot([B[0], Bp[0]], [B[1], Bp[1]], [B[2], Bp[2]], color="tab:red", linewidth=2)
    # Line from A' to B
    ax.plot([A[0], B[0]], [A[1], B[1]], [A[2], B[2]], color="black", linewidth=1.4)
    # Line from A' to B'
    ax.plot([A[0], Bp[0]], [A[1], Bp[1]], [A[2], Bp[2]], color="black", linewidth=1.4, linestyle="--")

    # Point labels
    for pt, name, off in [(A, "A'", (-0.2, -0.2, 0.1)), (Bp, "B'", (0.2, 0.1, 0)), (B, "B", (0.1, 0.1, 0.1))]:
        ax.scatter(*pt, color="black", s=40)
        ax.text(pt[0] + off[0], pt[1] + off[1], pt[2] + off[2], name, fontsize=13)

    # Right angle marker
    ax.text(2.6, 1.6, 0.05, r"$\bot$", fontsize=11, color="tab:red")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title(r"Projection $B \to B'$ onto plane $\alpha$", fontsize=12)
    ax.view_init(elev=22, azim=-55)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 2 — Geometric meaning of the dot product
# ===


def make_dot_product(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5.5))

    # Two vectors u and v
    u = np.array([3.0, 1.0])
    v = np.array([2.0, 2.5])

    # Draw arrows
    arrow_u = FancyArrowPatch((0, 0), u, color="tab:blue", arrowstyle="-|>", mutation_scale=15, linewidth=2)
    arrow_v = FancyArrowPatch((0, 0), v, color="tab:red", arrowstyle="-|>", mutation_scale=15, linewidth=2)
    ax.add_patch(arrow_u)
    ax.add_patch(arrow_v)

    # Projection of v onto u
    proj_scalar = np.dot(u, v) / np.dot(u, u)
    proj = proj_scalar * u

    # Draw projection
    arrow_proj = FancyArrowPatch((0, 0), proj, color="tab:green", arrowstyle="-|>",
                                  mutation_scale=12, linewidth=3, alpha=0.7)
    ax.add_patch(arrow_proj)

    # Dashed line from v to projection
    ax.plot([v[0], proj[0]], [v[1], proj[1]], color="gray", linewidth=1, linestyle="--")

    # Labels
    ax.annotate(r"$\vec{u}$", (u[0] - 0.2, u[1] + 0.2), fontsize=14, color="tab:blue")
    ax.annotate(r"$\vec{v}$", (v[0] - 0.1, v[1] + 0.15), fontsize=14, color="tab:red")
    ax.annotate(r"$\mathrm{proj}_{\vec{u}}\,\vec{v}$", proj, xytext=(8, -16), textcoords="offset points",
                fontsize=12, color="tab:green")

    # Theta angle marker
    ax.annotate(r"$\theta$", (0.45, 0.18), fontsize=13)

    ax.annotate(
        r"$\vec{u} \cdot \vec{v} = |\vec{u}|\,|\vec{v}|\cos\theta = |\vec{u}|\,|\mathrm{proj}_{\vec{u}}\vec{v}|$  (signed)",
        (0.2, 3.1),
        fontsize=12,
    )

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-0.5, 4)
    ax.set_ylim(-0.5, 3.5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title("Dot product = magnitude $\\times$ projection (signed)", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 3 — Exercise 1 setup
# ===


def make_setup(out_path: Path) -> None:
    fig = plt.figure(figsize=(8, 5.5))
    ax = fig.add_subplot(111, projection="3d")

    # Plane
    xs, ys = np.meshgrid(np.linspace(-1, 7, 12), np.linspace(-3, 3, 12))
    zs = np.zeros_like(xs)
    ax.plot_surface(xs, ys, zs, alpha=0.15, color="tab:blue")

    # A' at origin, B' = (5, 0, 0), B = (5, 0, 5√3)
    Ap = np.array([0, 0, 0])
    Bp = np.array([5, 0, 0])
    B = np.array([5, 0, 5 * np.sqrt(3)])

    # R divides A'B with ratio t : (5-t), say t = 2
    t = 2.0
    R = (t / 5) * B + ((5 - t) / 5) * Ap
    # Wait, R divides A'B with ratio t : (5 - t) from A' to B, so R = A' + (t/5)(B - A') ... but A'B = 10, not 5
    # Actually problem says: 선분 A'B를 t:(5-t)로 내분, 그리고 A'B = 10. So R = ((5-t)/5) A' + (t/5) B... no
    # Internally dividing A'B in ratio t:(5-t) means R = ((5-t)A' + tB)/(t + (5-t)) = ((5-t)A' + tB)/5
    R = ((5 - t) * Ap + t * B) / 5
    Rp = np.array([R[0], R[1], 0])  # projection onto plane

    # Draw segments
    ax.plot([Ap[0], B[0]], [Ap[1], B[1]], [Ap[2], B[2]], color="black", linewidth=1.5, label=r"$A'B = 10$")
    ax.plot([Bp[0], B[0]], [Bp[1], B[1]], [Bp[2], B[2]], color="tab:red", linewidth=1.5, label=r"$B'B = 5\sqrt{3}$")
    ax.plot([Ap[0], Bp[0]], [Ap[1], Bp[1]], [Ap[2], Bp[2]], color="tab:gray", linewidth=1.5, linestyle="--",
            label=r"$A'B' = 5$")
    ax.plot([R[0], Rp[0]], [R[1], Rp[1]], [R[2], Rp[2]], color="tab:purple", linewidth=1.5, linestyle=":")

    # Points
    for pt, name in [(Ap, "A'"), (Bp, "B'"), (B, "B"), (R, "R"), (Rp, "R'")]:
        ax.scatter(*pt, color="black", s=40)
        ax.text(pt[0] + 0.2, pt[1] + 0.15, pt[2] + 0.1, name, fontsize=12)

    # Triangle ∆ (just a hint; will be detailed in next figure)
    tri = [(2, -1, 0), (3, -1, 0), (2.5, 0, 0)]
    poly_x = [p[0] for p in tri] + [tri[0][0]]
    poly_y = [p[1] for p in tri] + [tri[0][1]]
    poly_z = [p[2] for p in tri] + [tri[0][2]]
    ax.plot(poly_x, poly_y, poly_z, color="tab:green", linewidth=2)
    ax.text(2.5, -0.5, 0.5, r"$\triangle$", fontsize=14, color="tab:green")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title(r"Setup: $A'B = 10$, $BB' = 5\sqrt{3}$ (so $A'B' = 5$)", fontsize=11)
    ax.view_init(elev=15, azim=-65)
    ax.legend(loc="upper left", fontsize=9)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 4 — Triangle △ (base 2, height 1) — two orientations
# ===


def make_triangle(out_path: Path) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

    # Both share the same A'B' = 5 segment with the triangle attached differently
    for ax, label in zip((ax1, ax2), ("Orientation 1", "Orientation 2")):
        ax.plot([0, 5], [0, 0], color="black", linewidth=2)
        ax.plot(0, 0, "o", color="black", markersize=7)
        ax.plot(5, 0, "o", color="black", markersize=7)
        ax.annotate("A'", (0, 0), xytext=(-15, -5), textcoords="offset points", fontsize=12)
        ax.annotate("B'", (5, 0), xytext=(8, -5), textcoords="offset points", fontsize=12)

        if label == "Orientation 1":
            # Triangle with apex above x-axis pointing toward A' side
            tri_pts = [(2, 0), (4, 0), (3, 1)]
            ax.set_title(r"Orientation 1:  apex $G_1'$ above $A'B'$", fontsize=11)
        else:
            # Triangle on the other side
            tri_pts = [(1, 0), (3, 0), (2, 1)]
            ax.set_title(r"Orientation 2:  apex $G_2'$ above $A'B'$", fontsize=11)

        poly = Polygon(tri_pts, closed=True, fill=True, facecolor="tab:green", alpha=0.3,
                       edgecolor="tab:green", linewidth=2)
        ax.add_patch(poly)

        # Annotate side lengths
        ax.annotate("base $= 2$", ((tri_pts[0][0] + tri_pts[1][0]) / 2, -0.18),
                    fontsize=11, ha="center", color="tab:green")
        ax.plot([tri_pts[2][0], tri_pts[2][0]], [0, tri_pts[2][1]], color="gray", linestyle=":")
        ax.annotate("height $= 1$", (tri_pts[2][0] + 0.1, 0.5), fontsize=11, color="gray")
        ax.annotate(r"area $= 1$", (tri_pts[2][0] - 1.5, 0.7), fontsize=12, color="tab:green", fontweight="bold")

        ax.set_xlim(-1, 6)
        ax.set_ylim(-0.5, 2)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", linewidth=0.5)

    fig.suptitle(r"Triangle $\triangle$ on plane $\alpha$:  base $2$, height $1$, area $= 1$", fontsize=12)
    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 5 — Projection T' and the sphere O above
# ===


def make_T_projection(out_path: Path) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    # Left: 2D projection T' = circle C + two tangent segments l₁, l₂
    radius = 1.0  # radius of C
    Hp = np.array([0, 0])
    Kp = np.array([2 * radius, 0])
    center_C = np.array([radius, 0])

    circle = Circle(center_C, radius, fill=False, color="tab:blue", linewidth=2.2)
    ax1.add_patch(circle)

    # Tangent segments l₁ from H', l₂ from K' — perpendicular to H'K' direction
    # Length = 2r (diameter of C)
    ax1.plot([Hp[0], Hp[0]], [Hp[1], Hp[1] + 2 * radius], color="tab:red", linewidth=2.5, label=r"$\ell_1$")
    ax1.plot([Kp[0], Kp[0]], [Kp[1], Kp[1] + 2 * radius], color="tab:purple", linewidth=2.5, label=r"$\ell_2$")

    # Labels
    ax1.plot(*Hp, "o", color="black", markersize=7)
    ax1.plot(*Kp, "o", color="black", markersize=7)
    ax1.plot(*center_C, "x", color="black", markersize=9)
    ax1.annotate("H'", Hp, xytext=(-15, -10), textcoords="offset points", fontsize=12)
    ax1.annotate("K'", Kp, xytext=(8, -10), textcoords="offset points", fontsize=12)
    ax1.annotate(r"center of $C$", center_C, xytext=(-15, 12), textcoords="offset points", fontsize=10)

    ax1.set_xlim(-1, 3)
    ax1.set_ylim(-1.5, 3)
    ax1.set_aspect("equal")
    ax1.set_title(r"$T' =$ circle $C$ $\cup$ two tangent segments  $\ell_1, \ell_2$", fontsize=11)
    ax1.set_xlabel(r"projection plane $\alpha$", fontsize=11)
    ax1.legend(loc="upper right", fontsize=11)
    ax1.grid(alpha=0.25)

    # Right: 3D view of sphere O and path T
    ax2 = fig.add_subplot(122, projection="3d")
    # Sphere O of radius √2 above plane
    u_vals = np.linspace(0, 2 * np.pi, 30)
    v_vals = np.linspace(0, np.pi, 20)
    R_sphere = np.sqrt(2)
    cx, cy, cz = 1.0, 0.0, 1.5
    xs = cx + R_sphere * np.outer(np.cos(u_vals), np.sin(v_vals))
    ys = cy + R_sphere * np.outer(np.sin(u_vals), np.sin(v_vals))
    zs = cz + R_sphere * np.outer(np.ones_like(u_vals), np.cos(v_vals))
    ax2.plot_surface(xs, ys, zs, alpha=0.18, color="tab:orange")

    # Plane α (z = 0)
    px, py = np.meshgrid(np.linspace(-1, 3, 6), np.linspace(-1.5, 1.5, 6))
    ax2.plot_surface(px, py, np.zeros_like(px), alpha=0.12, color="tab:blue")

    # Projection T' on the plane
    theta = np.linspace(0, 2 * np.pi, 100)
    circle_x = 1 + np.cos(theta)
    circle_y = np.sin(theta)
    ax2.plot(circle_x, circle_y, 0, color="tab:blue", linewidth=2)
    ax2.plot([0, 0], [0, 2], [0, 0], color="tab:red", linewidth=2)
    ax2.plot([2, 2], [0, 2], [0, 0], color="tab:purple", linewidth=2)

    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_zlabel("z")
    ax2.set_title(r"Sphere $O$ of radius $\sqrt{2}$ projects to $T'$ on $\alpha$", fontsize=11)
    ax2.view_init(elev=18, azim=-60)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 6 — Eight cases of inner product (case 2 with P₁' on l₁)
# ===


def make_inner_cases(out_path: Path) -> None:
    fig, axes = plt.subplots(2, 4, figsize=(14, 7))

    a_val = 0.5  # P₁' at distance a from segment H'K'

    # 8 cases — different positions of P₁', Q₁', P₂', Q₂' on T'
    # We just illustrate them schematically
    case_labels = [
        "2-1:  $I = -1$",
        "2-2:  $I = 0$",
        "2-3:  $I = +1$",
        "2-4:  $I = 0$",
        "2-5:  $I = -2 - \\sqrt{3}$",
        "2-6:  $I = -2 - \\sqrt{3}$",
        "2-7:  $I = -1 - \\sqrt{3}$",
        "2-8:  $I = -2 - \\sqrt{3}$",
    ]

    for idx, (ax, label) in enumerate(zip(axes.flat, case_labels)):
        radius = 1.0
        circle = Circle((1, 0), radius, fill=False, color="tab:blue", linewidth=1.5)
        ax.add_patch(circle)
        # ℓ₁ and ℓ₂
        ax.plot([0, 0], [0, 2 * radius], color="tab:gray", linewidth=1)
        ax.plot([2 * radius, 2 * radius], [0, 2 * radius], color="tab:gray", linewidth=1)
        # H'K' line
        ax.plot([0, 2 * radius], [0, 0], color="tab:gray", linewidth=0.8, linestyle="--")

        # Schematic arrows for P₁'Q₁' and P₂'Q₂' (placement varies by case)
        # Just draw representative arrows; details would come from full case analysis
        # For demo, draw two parallel arrows at a typical position
        if idx == 0:  # 2-1: opposite parallel
            ax.annotate("", xy=(0.3, 0.4), xytext=(0.6, 0.6),
                        arrowprops=dict(arrowstyle="->", color="tab:red", linewidth=2))
            ax.annotate("", xy=(1.4, 0.6), xytext=(1.7, 0.4),
                        arrowprops=dict(arrowstyle="->", color="tab:green", linewidth=2))
        elif idx == 2:  # 2-3: parallel same direction
            ax.annotate("", xy=(0.6, 0.6), xytext=(0.3, 0.4),
                        arrowprops=dict(arrowstyle="->", color="tab:red", linewidth=2))
            ax.annotate("", xy=(1.7, 0.6), xytext=(1.4, 0.4),
                        arrowprops=dict(arrowstyle="->", color="tab:green", linewidth=2))
        else:
            # Generic arrows
            ax.annotate("", xy=(0.7, 0.7), xytext=(0.3, 0.3),
                        arrowprops=dict(arrowstyle="->", color="tab:red", linewidth=1.8))
            ax.annotate("", xy=(1.6, 1.4), xytext=(1.3, 1.7),
                        arrowprops=dict(arrowstyle="->", color="tab:green", linewidth=1.8))

        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-0.5, 2.5)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(label, fontsize=10)

    fig.suptitle(
        r"Eight sub-cases for case 2 (P₁' on $\ell_1$): values of $I = \overrightarrow{P_1' Q_1'} \cdot \overrightarrow{P_2' Q_2'}$",
        fontsize=12,
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Entry point
# ===

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    make_projection(out_dir / "example1_projection.png")
    make_dot_product(out_dir / "example2_dot_product.png")
    make_setup(out_dir / "exercise1_setup.png")
    make_triangle(out_dir / "exercise1_triangle.png")
    make_T_projection(out_dir / "exercise2_T_projection.png")
    make_inner_cases(out_dir / "exercise2_inner_cases.png")
    print(f"Wrote figures to {out_dir}")
