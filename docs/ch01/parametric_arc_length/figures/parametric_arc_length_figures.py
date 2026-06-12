"""Figures for parametric_arc_length.md.

Generates PNGs in this directory:

- ``example1_circle.png``         : the unit circle as a parametric curve
  x = cos t, y = sin t.
- ``example2_ellipse.png``        : the ellipse x = 3 cos t, y = 2 sin t
  with two tangent lines and their (M, N) intercepts.
- ``exercise1_line_segment.png``  : when A = B = 1, θ = 0, the relationship
  x = y on [-1, 1].
- ``exercise2_lissajous.png``     : when A = B = 1, θ = π/3, the resulting
  Lissajous-like trajectory.
- ``exercise3_circle_path.png``   : when A = B = √5, θ = π/2, the path is a
  full circle of radius √5; first quarter highlighted.
- ``exercise4_ellipse_tangent.png``: the ellipse 4x² + 9y² = 36 with the
  tangent at P(x₁, y₁) cutting axes at M(9/x₁, 0) and N(0, 4/y₁).
- ``exercise4_AM_GM.png``         : AM-GM lower bound for triangle area
  S = 18/(x₁y₁) ≥ 6.

Run with ``python parametric_arc_length_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# ===
# Figure 1 — Unit circle as parametric curve
# ===


def make_circle(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))

    t = np.linspace(0, 2 * np.pi, 200)
    x = np.cos(t)
    y = np.sin(t)

    ax.plot(x, y, color="tab:blue", linewidth=2.2)

    # Mark four sample points
    for tp, name in [(0, "t = 0"), (np.pi / 2, "t = π/2"), (np.pi, "t = π"),
                     (3 * np.pi / 2, "t = 3π/2")]:
        ax.plot(np.cos(tp), np.sin(tp), "o", color="tab:red", markersize=7)
        ax.annotate(name, (np.cos(tp), np.sin(tp)),
                    xytext=(8, 8), textcoords="offset points", fontsize=10)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"$x = \cos t,\;y = \sin t$:  parametric circle, $t \in [0, 2\pi]$", fontsize=11)
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 2 — Ellipse with two tangents
# ===


def make_ellipse(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))

    t = np.linspace(0, 2 * np.pi, 200)
    x = 3 * np.cos(t)
    y = 2 * np.sin(t)
    ax.plot(x, y, color="tab:blue", linewidth=2.2, label=r"$4x^2 + 9y^2 = 36$")

    # Tangent line at (3, 0): 4·3·x + 9·0·y = 36 → x = 3 (vertical)
    # Tangent line at P = (3·cos(π/3), 2·sin(π/3)) = (1.5, √3): 4·1.5·x + 9·√3·y = 36
    # → 6x + 9√3 y = 36, intercepts: x = 6 (when y=0), y = 36/(9√3) = 4/√3 (when x=0)
    p_x, p_y = 1.5, np.sqrt(3)
    ax.plot(p_x, p_y, "o", color="tab:red", markersize=9)
    ax.annotate(r"$P(x_1, y_1)$", (p_x, p_y), xytext=(8, 8),
                textcoords="offset points", fontsize=11, color="tab:red")

    # Plot tangent line
    tan_xs = np.linspace(0, 6.5, 50)
    tan_ys = (36 - 6 * tan_xs) / (9 * np.sqrt(3))
    ax.plot(tan_xs, tan_ys, color="tab:red", linewidth=1.5, linestyle="--")

    # M and N
    M = (6, 0)
    N = (0, 4 / np.sqrt(3))
    ax.plot(*M, "o", color="black", markersize=7)
    ax.annotate(r"$M\left(\frac{9}{x_1},\,0\right)$", M, xytext=(8, 6),
                textcoords="offset points", fontsize=11)
    ax.plot(*N, "o", color="black", markersize=7)
    ax.annotate(r"$N\left(0,\,\frac{4}{y_1}\right)$", N, xytext=(8, 6),
                textcoords="offset points", fontsize=11)

    # Triangle OMN
    triangle_x = [0, M[0], N[0], 0]
    triangle_y = [0, M[1], N[1], 0]
    ax.fill(triangle_x, triangle_y, color="tab:green", alpha=0.15)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-4, 7.5)
    ax.set_ylim(-3, 3.5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"Ellipse $4x^2 + 9y^2 = 36$ and tangent at $P$ cutting axes at $M, N$", fontsize=11)
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 3 — Exercise 1: line segment y = x on [-1, 1]
# ===


def make_line_segment(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))

    # x = cos 2πt, y = cos 2πt = x for any t. So x ranges over [-1, 1]
    t = np.linspace(0, 1, 200)
    x = np.cos(2 * np.pi * t)
    y = np.cos(2 * np.pi * t)
    ax.plot(x, y, color="tab:blue", linewidth=3, alpha=0.5)

    # Mark endpoints
    ax.plot(1, 1, "o", color="tab:red", markersize=9)
    ax.plot(-1, -1, "o", color="tab:red", markersize=9)
    ax.annotate(r"$(1, 1)$", (1, 1), xytext=(8, 8), textcoords="offset points", fontsize=11)
    ax.annotate(r"$(-1, -1)$", (-1, -1), xytext=(-50, -20), textcoords="offset points", fontsize=11)

    # Reference grid
    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_xticks(range(-3, 4))
    ax.set_yticks(range(-3, 4))
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"$A = B = 1,\;\theta = 0$:  $y = x$ on $[-1, 1]$", fontsize=11)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 4 — Exercise 2: Lissajous-like for θ = π/3
# ===


def make_lissajous(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))

    t = np.linspace(0, 1, 400)
    A, B = 1, 1
    theta = np.pi / 3
    x = A * np.cos(2 * np.pi * t)
    y = B * np.cos(2 * np.pi * t + theta)
    ax.plot(x, y, color="tab:blue", linewidth=2)

    # Mark a sample point for tangent illustration
    t_sample = 0.1
    xs = A * np.cos(2 * np.pi * t_sample)
    ys = B * np.cos(2 * np.pi * t_sample + theta)
    ax.plot(xs, ys, "o", color="tab:red", markersize=8)

    # Tangent slope: a + b cot(2πt) where a = 1/2, b = √3/2
    a = 0.5
    b = np.sqrt(3) / 2
    slope = a + b / np.tan(2 * np.pi * t_sample)
    tan_dx = 0.4
    tx = np.array([xs - tan_dx, xs + tan_dx])
    ty = ys + slope * (tx - xs)
    ax.plot(tx, ty, color="tab:red", linewidth=1.5, linestyle="--",
            label=rf"tangent slope $= a + b \cot 2\pi t$")

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"$A = B = 1,\;\theta = \pi/3$:  $\frac{dy}{dx} = \frac{1}{2} + \frac{\sqrt{3}}{2}\cot 2\pi t$", fontsize=11)
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 5 — Exercise 3: circle of radius √5 with first quarter highlighted
# ===


def make_circle_path(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))

    t = np.linspace(0, 1, 400)
    A = B = np.sqrt(5)
    theta = np.pi / 2
    x = A * np.cos(2 * np.pi * t)
    y = B * np.cos(2 * np.pi * t + theta)  # = -√5 sin 2πt

    ax.plot(x, y, color="tab:blue", linewidth=2, alpha=0.4, label="full circle (period $p = 1$)")

    # Highlight t ∈ [0, 1/4]
    t_q = np.linspace(0, 0.25, 100)
    x_q = A * np.cos(2 * np.pi * t_q)
    y_q = B * np.cos(2 * np.pi * t_q + theta)
    ax.plot(x_q, y_q, color="tab:red", linewidth=3.5, label=r"$t \in [0,\,p/4]$ (length $= \sqrt{5}\,\pi/2$)")

    # Arrow showing direction
    ax.annotate("",
                xy=(x_q[60], y_q[60]),
                xytext=(x_q[40], y_q[40]),
                arrowprops=dict(arrowstyle="->", color="tab:red", linewidth=2.2))

    ax.plot(A, 0, "o", color="black", markersize=7)
    ax.annotate(r"$t = 0$:  $(\sqrt{5},\,0)$", (A, 0), xytext=(8, 6),
                textcoords="offset points", fontsize=11)
    ax.plot(0, -B, "o", color="black", markersize=7)
    ax.annotate(r"$t = 1/4$:  $(0,\,-\sqrt{5})$", (0, -B), xytext=(8, -15),
                textcoords="offset points", fontsize=11)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"$A = B = \sqrt{5},\;\theta = \pi/2$:  circle traced clockwise", fontsize=11)
    ax.legend(loc="lower left", fontsize=10)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 6 — Exercise 4: ellipse with tangent
# ===


def make_ellipse_tangent(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    # Ellipse 4x² + 9y² = 36, semi-axes 3 and 2
    t = np.linspace(0, 2 * np.pi, 200)
    x = 3 * np.cos(t)
    y = 2 * np.sin(t)
    ax.plot(x, y, color="tab:blue", linewidth=2.2)

    # Pick P in first quadrant — minimum case: x₁ y₁ = 3, so 4x₁² = 9y₁² = 18,
    # x₁ = 3/√2, y₁ = √2
    x1 = 3 / np.sqrt(2)
    y1 = np.sqrt(2)
    ax.plot(x1, y1, "o", color="tab:red", markersize=10)
    ax.annotate(rf"$P(x_1, y_1) = (3/\sqrt{{2}},\,\sqrt{{2}})$", (x1, y1), xytext=(8, 8),
                textcoords="offset points", fontsize=11, color="tab:red")

    # Tangent: 4x₁ x + 9y₁ y = 36
    # y = (36 - 4x₁ x) / (9y₁)
    M = (9 / x1, 0)
    N = (0, 4 / y1)
    tan_xs = np.linspace(0, M[0] + 0.4, 50)
    tan_ys = (36 - 4 * x1 * tan_xs) / (9 * y1)
    ax.plot(tan_xs, tan_ys, color="tab:red", linewidth=1.6, linestyle="--",
            label=rf"$4x_1 x + 9y_1 y = 36$")

    ax.plot(*M, "o", color="black", markersize=8)
    ax.annotate(rf"$M\left({M[0]:.2f},\,0\right)$", M, xytext=(8, -16),
                textcoords="offset points", fontsize=11)
    ax.plot(*N, "o", color="black", markersize=8)
    ax.annotate(rf"$N\left(0,\,{N[1]:.2f}\right)$", N, xytext=(-95, -8),
                textcoords="offset points", fontsize=11)

    # Triangle OMN — minimum area = 6
    triangle_x = [0, M[0], N[0], 0]
    triangle_y = [0, M[1], N[1], 0]
    ax.fill(triangle_x, triangle_y, color="tab:green", alpha=0.18, label=r"$\triangle OMN$  (min area $= 6$)")

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-4, 7.5)
    ax.set_ylim(-3, 4)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"Tangent to ellipse $4x^2 + 9y^2 = 36$ at $P$, area of $\triangle OMN$ minimized", fontsize=11)
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 7 — Exercise 4: AM-GM bound on S = 18/(x₁y₁)
# ===


def make_AM_GM(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 5))

    # Parametrize P on the ellipse: x₁ = 3 cos s, y₁ = 2 sin s, s ∈ (0, π/2)
    s_vals = np.linspace(0.05, np.pi / 2 - 0.05, 200)
    x1s = 3 * np.cos(s_vals)
    y1s = 2 * np.sin(s_vals)

    S_vals = 18 / (x1s * y1s)

    ax.plot(s_vals, S_vals, color="tab:blue", linewidth=2.2, label=r"$S = 18/(x_1 y_1)$")
    ax.axhline(6, color="tab:red", linewidth=1.5, linestyle="--", label=r"$S_{\min} = 6$  (AM-GM)")

    # Minimum at s = π/4 (when 4x₁² = 9y₁², x₁ = 3/√2, y₁ = √2)
    s_min = np.pi / 4
    ax.plot(s_min, 6, "o", color="tab:red", markersize=10)
    ax.annotate(r"min at $s = \pi/4$", (s_min, 6), xytext=(15, -20),
                textcoords="offset points", fontsize=11, color="tab:red",
                arrowprops=dict(arrowstyle="->", color="tab:red"))

    ax.set_xlabel(r"$s$ (where $x_1 = 3\cos s,\;y_1 = 2\sin s$)", fontsize=11)
    ax.set_ylabel(r"$S$", fontsize=11)
    ax.set_title(r"AM-GM:  $36 = 4x_1^2 + 9y_1^2 \geq 12\,x_1 y_1$, so $x_1 y_1 \leq 3$", fontsize=11)
    ax.set_xticks([0, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2])
    ax.set_xticklabels(["0", r"$\pi/8$", r"$\pi/4$", r"$3\pi/8$", r"$\pi/2$"])
    ax.set_ylim(4, 30)
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
    make_circle(out_dir / "example1_circle.png")
    make_ellipse(out_dir / "example2_ellipse.png")
    make_line_segment(out_dir / "exercise1_line_segment.png")
    make_lissajous(out_dir / "exercise2_lissajous.png")
    make_circle_path(out_dir / "exercise3_circle_path.png")
    make_ellipse_tangent(out_dir / "exercise4_ellipse_tangent.png")
    make_AM_GM(out_dir / "exercise4_AM_GM.png")
    print(f"Wrote figures to {out_dir}")
