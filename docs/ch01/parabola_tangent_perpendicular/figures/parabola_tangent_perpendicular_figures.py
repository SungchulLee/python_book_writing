"""Figures for parabola_tangent_perpendicular.md.

Generates PNGs in this directory:

- ``example1_parabola_tangent.png``  : the parabola y = x²/2 with a tangent
  at (a, a²/2) and the normal at the same point.
- ``example2_three_cases.png``       : three cases for the location of
  P = L_1 ∩ L_2 — above the parabola, on the parabola, below the parabola.
- ``exercise1_gamma.png``            : a = 3 case — point P moves with b
  and y(P) > γ = 29/2.
- ``exercise2_max_distance.png``     : distance from Q on parabola to L_1
  maximized at q = -1/a.
- ``exercise3_ab_relation.png``      : the locus of (a, b) such that P lies
  on the parabola, with the range 0 < a < √2.
- ``exercise4_circumcircle.png``     : the circumscribed circle of △PAB for
  a = 1.
- ``exercise5_area_ratio.png``       : the regions S_1, S_2 and the limit
  S_2/S_1 → 14 as a → 0+.

Run with ``python parabola_tangent_perpendicular_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle


def _parabola(x):
    return 0.5 * x**2


def _tangent_slope(x):
    return x


# ===
# Figure 1 — Parabola y = x²/2 with tangent and normal at a point
# ===


def make_parabola_tangent(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))

    xs = np.linspace(-3, 3, 200)
    ax.plot(xs, _parabola(xs), color="tab:blue", linewidth=2.2)
    ax.annotate(r"$y = \frac{1}{2} x^2$", (2.0, 2.5), fontsize=13, color="tab:blue")

    a = 1.5
    pa = (a, _parabola(a))
    slope_t = _tangent_slope(a)

    # Tangent line
    tx = np.linspace(a - 1.5, a + 1.5, 30)
    ty = pa[1] + slope_t * (tx - a)
    ax.plot(tx, ty, color="tab:red", linewidth=1.6, linestyle="--", label=r"tangent $\ell$ at $A$")

    # Normal line (perpendicular)
    slope_n = -1 / slope_t
    nx = np.linspace(a - 1.5, a + 1.5, 30)
    ny = pa[1] + slope_n * (nx - a)
    ax.plot(nx, ny, color="tab:green", linewidth=1.6, linestyle=":", label=r"normal $L$ at $A$")

    ax.plot(*pa, "o", color="black", markersize=9)
    ax.annotate(rf"$A(a,\,\frac{{a^2}}{{2}})$", pa, xytext=(10, 5),
                textcoords="offset points", fontsize=12)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-1.5, 4)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"Parabola $y = \frac{1}{2}x^2$:  tangent slope at $(a, a^2/2)$ is $a$", fontsize=12)
    ax.legend(loc="upper left", fontsize=11)
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 2 — Three cases of P location
# ===


def _compute_P(a, b):
    """L_1: through A=(a, a²/2) with slope -1/a. L_2: through B=(b, b²/2) with slope -1/b."""
    # L_1: y - a²/2 = -1/a (x - a), i.e., y = -x/a + 1/2 + a²/2
    # L_2: y = -x/b + 1/2 + b²/2
    # Intersection: -x/a + a²/2 + 1/2 = -x/b + b²/2 + 1/2
    # x(1/b - 1/a) = (b² - a²)/2 = (b-a)(b+a)/2
    # x = (b-a)(b+a)/2 / ((a-b)/ab) = -ab(b+a)/2
    x = -0.5 * a * b * (a + b)
    y = -x / a + 0.5 + a**2 / 2
    return x, y


def make_three_cases(out_path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    cases = [
        (0.7, 1.5, r"Case 1: $P$ above parabola"),
        (1.0, 2.0, r"Case 2: $P$ on parabola  ($ab = 2$)"),
        (1.3, 2.3, r"Case 3: $P$ below parabola"),
    ]

    for ax, (a, b, title) in zip(axes, cases):
        xs = np.linspace(-2, 4, 200)
        ax.plot(xs, _parabola(xs), color="tab:blue", linewidth=2)

        A = (a, _parabola(a))
        B = (b, _parabola(b))
        P = _compute_P(a, b)

        # Draw L_1 from A, L_2 from B
        for pt, slope, color in [(A, -1/a, "tab:red"), (B, -1/b, "tab:green")]:
            tx = np.linspace(pt[0] - 3, pt[0] + 3, 30)
            ty = pt[1] + slope * (tx - pt[0])
            ax.plot(tx, ty, color=color, linewidth=1.4, linestyle="--")

        # Mark points
        ax.plot(*A, "o", color="black", markersize=7)
        ax.annotate("A", A, xytext=(8, 5), textcoords="offset points", fontsize=11)
        ax.plot(*B, "o", color="black", markersize=7)
        ax.annotate("B", B, xytext=(8, 5), textcoords="offset points", fontsize=11)
        ax.plot(*P, "o", color="tab:red", markersize=9)
        ax.annotate("P", P, xytext=(8, 5), textcoords="offset points", fontsize=11, color="tab:red")

        ax.axhline(0, color="black", linewidth=0.5)
        ax.axvline(0, color="black", linewidth=0.5)
        ax.set_xlim(-3, 4)
        ax.set_ylim(-1, 5.5)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel(r"$x$", fontsize=10)
        ax.set_ylabel(r"$y$", fontsize=10)

    fig.suptitle(r"Three cases for $P = L_1 \cap L_2$  ($L_i \perp$ tangent at $A_i / B_i$)", fontsize=12)
    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 3 — Exercise 1: γ = 29/2
# ===


def make_gamma(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    a = 3
    # P_y = (11 + b² + 3b) / 2 for b > a = 3
    bs = np.linspace(3.01, 8, 300)
    P_y = (11 + bs**2 + 3 * bs) / 2

    ax.plot(bs, P_y, color="tab:blue", linewidth=2.2, label=r"$y$-coord of $P$ as $b$ varies ($a = 3$)")
    ax.axhline(29 / 2, color="tab:red", linewidth=2, linestyle="--",
               label=r"$\gamma = 29/2$")

    # Mark limit at b → a
    ax.plot(3, 29 / 2, "o", color="tab:red", markersize=10)
    ax.annotate(r"$\lim_{b \to a^+} y_P = \frac{29}{2}$",
                (3, 29 / 2), xytext=(15, -15), textcoords="offset points",
                fontsize=12, color="tab:red",
                arrowprops=dict(arrowstyle="->", color="tab:red"))

    ax.set_xlabel(r"$b$  (with $b > a = 3$)", fontsize=11)
    ax.set_ylabel(r"$y$-coord of $P$", fontsize=11)
    ax.set_title(r"$y$-coord of $P$ exceeds $\gamma = 29/2$ for all $b > a = 3$", fontsize=11)
    ax.legend(loc="upper left", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 4 — Exercise 2: max distance from Q on parabola to L_1
# ===


def make_max_distance(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))

    a = 1.5
    H_x = -a - 2 / a
    A = (a, a**2 / 2)

    # Parabola
    xs = np.linspace(H_x - 0.5, a + 0.5, 200)
    ax.plot(xs, _parabola(xs), color="tab:blue", linewidth=2.2, label=r"$y = \frac{1}{2}x^2$")

    # L_1: through A with slope -1/a
    tx = np.linspace(H_x - 0.5, a + 0.5, 30)
    ty = A[1] - (1 / a) * (tx - a)
    ax.plot(tx, ty, color="tab:red", linewidth=1.6, linestyle="--", label=r"$L_1$")

    # Mark A and H
    ax.plot(*A, "o", color="black", markersize=8)
    ax.annotate("A", A, xytext=(8, 5), textcoords="offset points", fontsize=12)
    H_y = _parabola(H_x)
    ax.plot(H_x, H_y, "o", color="tab:purple", markersize=8)
    ax.annotate(r"$H$ (other intersection)", (H_x, H_y), xytext=(-100, 5),
                textcoords="offset points", fontsize=10, color="tab:purple")

    # Q at q = -1/a (where distance is max)
    q = -1 / a
    Q = (q, _parabola(q))
    ax.plot(*Q, "o", color="tab:green", markersize=10)
    ax.annotate(rf"$Q$ at $q = -1/a$  (max distance)",
                Q, xytext=(15, -25), textcoords="offset points",
                fontsize=11, color="tab:green",
                arrowprops=dict(arrowstyle="->", color="tab:green"))

    # Draw perpendicular from Q to L_1
    # Foot of perpendicular: parametrize and find closest point on line
    line_dir = np.array([1, -1/a])
    line_dir = line_dir / np.linalg.norm(line_dir)
    Q_arr = np.array(Q)
    A_arr = np.array(A)
    t = np.dot(Q_arr - A_arr, line_dir)
    foot = A_arr + t * line_dir
    ax.plot([Q[0], foot[0]], [Q[1], foot[1]], color="tab:green", linewidth=1.2)

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(H_x - 1, a + 1)
    ax.set_ylim(-1, max(H_y, A[1]) + 1)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"Max distance from $Q$ to $L_1$:  $Q$ at $x = -1/a$, distance $= \frac{(a^2+1)\sqrt{a^2+1}}{2a}$", fontsize=10)
    ax.legend(loc="upper right", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 5 — Exercise 3: ab = 2 locus
# ===


def make_ab_relation(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))

    a_vals = np.linspace(0.1, 3, 200)
    b_vals = 2 / a_vals

    ax.plot(a_vals, b_vals, color="tab:blue", linewidth=2.2, label=r"$ab = 2$")

    # Constraint 0 < a < b: line b = a
    a_diag = np.linspace(0, 3, 50)
    ax.plot(a_diag, a_diag, color="tab:gray", linewidth=1, linestyle="--", label=r"$b = a$")

    # Highlight allowed region: a < b and ab = 2 → a < sqrt(2)
    sqrt2 = np.sqrt(2)
    a_allowed = np.linspace(0.05, sqrt2, 100)
    ax.plot(a_allowed, 2 / a_allowed, color="tab:red", linewidth=3.5, alpha=0.8,
            label=rf"allowed $a$: $0 < a < \sqrt{{2}}$")

    ax.plot(sqrt2, sqrt2, "o", color="black", markersize=10)
    ax.annotate(r"$a = b = \sqrt{2}$  (boundary)", (sqrt2, sqrt2),
                xytext=(10, 10), textcoords="offset points", fontsize=11)

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$a$", fontsize=11)
    ax.set_ylabel(r"$b$", fontsize=11)
    ax.set_title(r"$P$ lies on parabola ⟺ $ab = 2$;  with $0 < a < b$, allowed $a \in (0, \sqrt{2})$", fontsize=11)
    ax.legend(loc="upper right", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 6 — Exercise 4: circumcircle of △PAB for a = 1
# ===


def make_circumcircle(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 8))

    a, b = 1.0, 2.0  # ab = 2
    A = (a, a**2 / 2)
    B = (b, b**2 / 2)
    P = _compute_P(a, b)

    # Parabola
    xs = np.linspace(-2, 3, 200)
    ax.plot(xs, _parabola(xs), color="tab:blue", linewidth=2)

    # Triangle PAB
    triangle_x = [P[0], A[0], B[0], P[0]]
    triangle_y = [P[1], A[1], B[1], P[1]]
    ax.fill(triangle_x, triangle_y, color="tab:orange", alpha=0.2)
    ax.plot(triangle_x, triangle_y, color="tab:orange", linewidth=1.8)

    # Circumcircle center: (-3/4, 11/4), radius √(130)/4 = √130/4
    center = (-3/4, 11/4)
    radius = np.sqrt(130) / 4
    circle = Circle(center, radius, fill=False, color="tab:red", linewidth=2,
                    linestyle="--")
    ax.add_patch(circle)

    # Mark center
    ax.plot(*center, "x", color="tab:red", markersize=12)
    ax.annotate(rf"center $\left(-\frac{{3}}{{4}},\,\frac{{11}}{{4}}\right)$", center,
                xytext=(-100, -20), textcoords="offset points", fontsize=11, color="tab:red")

    # Mark vertices
    for pt, name in [(P, "P"), (A, "A"), (B, "B")]:
        ax.plot(*pt, "o", color="black", markersize=9)
        ax.annotate(name, pt, xytext=(8, 8), textcoords="offset points", fontsize=13)

    # Show radius
    ax.annotate(rf"radius $= \frac{{\sqrt{{130}}}}{{4}}$", (center[0] + 0.5, center[1] + 1.5),
                fontsize=11, color="tab:red")

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlim(-3, 4)
    ax.set_ylim(-1, 6)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"$a = 1, b = 2$:  circumcircle of $\triangle PAB$", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 7 — Exercise 5: S_2 / S_1 → 14
# ===


def make_area_ratio(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    a_vals = np.linspace(0.05, 1.5, 200)
    # S_1 = (a + 2/a)^3 / 24
    S1 = (a_vals + 2 / a_vals)**3 / 24
    # S_2 = 14/(3a^3) - (7/12)a^3 - a + 2/a
    S2 = 14 / (3 * a_vals**3) - (7 / 12) * a_vals**3 - a_vals + 2 / a_vals
    ratio = S2 / S1

    ax.plot(a_vals, ratio, color="tab:blue", linewidth=2.2, label=r"$S_2 / S_1$")
    ax.axhline(14, color="tab:red", linewidth=1.8, linestyle="--",
               label=r"$\lim_{a \to 0^+} S_2 / S_1 = 14$")

    ax.set_xlabel(r"$a$", fontsize=11)
    ax.set_ylabel(r"$S_2 / S_1$", fontsize=11)
    ax.set_title(r"Area ratio $S_2 / S_1$ approaches $14$ as $a \to 0^+$", fontsize=12)
    ax.set_ylim(0, 30)
    ax.legend(loc="upper right", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Entry point
# ===

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    make_parabola_tangent(out_dir / "example1_parabola_tangent.png")
    make_three_cases(out_dir / "example2_three_cases.png")
    make_gamma(out_dir / "exercise1_gamma.png")
    make_max_distance(out_dir / "exercise2_max_distance.png")
    make_ab_relation(out_dir / "exercise3_ab_relation.png")
    make_circumcircle(out_dir / "exercise4_circumcircle.png")
    make_area_ratio(out_dir / "exercise5_area_ratio.png")
    print(f"Wrote figures to {out_dir}")
