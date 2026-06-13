"""Figures for functional_equation_tangent.md.

Generates PNGs in this directory:

- ``example1_F_monotone.png``     : F(x) = kx + sin x for k = 3 is strictly
  increasing because F'(x) = k + cos x > 0.
- ``example2_implicit.png``       : the implicit equation F(g(x)) = F(x)/m
  determines g(x); shows g for (m, k) = (3, 18).
- ``exercise1_F_invertible.png``  : F⁻¹ exists because F is one-to-one and
  onto; reflection across y = x.
- ``exercise2_g_explicit.png``    : g(x) on a wider range for (m, k) = (3, 18)
  showing g(kπ) = nπ, g(mπ) = π, g(nπ) = (n/m)π.
- ``exercise3_three_tangents.png``: three tangent slopes at P₁, P₂, P₃ all
  equal to α = 1/m for (m, n, k) = (3, 6, 18).
- ``exercise3_search_space.png``  : the (m, n) lattice with m odd, m | n,
  m < n, mn ≤ 26 — only one point (3, 6).

Run with ``python functional_equation_tangent_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq


# ===
# Figure 1 — F(x) = kx + sin x is strictly increasing
# ===


def make_F_monotone(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    k = 3
    xs = np.linspace(-2 * np.pi, 2 * np.pi, 400)
    Fs = k * xs + np.sin(xs)
    Fps = k + np.cos(xs)

    ax.plot(xs, Fs, color="tab:blue", linewidth=2.2, label=r"$F(x) = kx + \sin x$  ($k = 3$)")
    ax.plot(xs, Fps, color="tab:red", linewidth=1.5, linestyle="--",
            label=r"$F'(x) = k + \cos x \geq k - 1 > 0$")

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.axhline(k - 1, color="gray", linewidth=0.5, linestyle=":")
    ax.annotate(rf"$F' \geq k - 1 = {k-1}$", (-2 * np.pi + 0.3, k - 1 + 0.3),
                fontsize=10, color="gray")

    ax.set_xlim(-2 * np.pi, 2 * np.pi)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_title(r"$F$ is strictly increasing on $\mathbb{R}$ because $F' > 0$", fontsize=11)
    ax.legend(loc="upper left", fontsize=11)
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Helper to compute g(x) numerically
# ===


def _compute_g(m, k, xs):
    """Compute g(x) such that k*g + sin(g) = (k*x + sin x)/m."""
    def F(t):
        return k * t + np.sin(t)
    ys = []
    for x in xs:
        target = F(x) / m
        # F is monotone; bracket
        lo = (target - 1) / k
        hi = (target + 1) / k
        # widen bracket
        while F(lo) > target:
            lo -= 1
        while F(hi) < target:
            hi += 1
        g_val = brentq(lambda t: F(t) - target, lo, hi)
        ys.append(g_val)
    return np.array(ys)


# ===
# Figure 2 — F(g(x)) = F(x)/m for (m, k) = (3, 18)
# ===


def make_implicit(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))

    m, k = 3, 18

    xs = np.linspace(-6 * np.pi, 6 * np.pi, 400)
    gs = _compute_g(m, k, xs)
    ax.plot(xs, gs, color="tab:blue", linewidth=2.2)

    # Mark P₁(kπ, g(kπ) = nπ), P₂(mπ, π), P₃(nπ, qπ) where n = 6, q = 2
    n = 6
    q = n // m

    points = [
        (k * np.pi, n * np.pi, r"$P_1 = (k\pi,\,n\pi)$"),
        (m * np.pi, np.pi, r"$P_2 = (m\pi,\,\pi)$"),
        (n * np.pi, q * np.pi, r"$P_3 = (n\pi,\,(n/m)\pi)$"),
    ]
    colors = ["tab:red", "tab:green", "tab:purple"]
    for (px, py, label), col in zip(points, colors):
        ax.plot(px, py, "o", color=col, markersize=9)
        ax.annotate(label, (px, py), xytext=(10, 8), textcoords="offset points",
                    fontsize=11, color=col)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$g(x)$", fontsize=11)
    ax.set_title(
        r"$y = g(x)$ defined by $F(g(x)) = F(x)/m$  for  $(m, k) = (3, 18)$",
        fontsize=11,
    )
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 3 — F is invertible (one-to-one and onto)
# ===


def make_F_invertible(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.5, 6.5))

    k = 3
    xs = np.linspace(-3 * np.pi, 3 * np.pi, 400)
    Fs = k * xs + np.sin(xs)

    # F
    ax.plot(xs, Fs, color="tab:blue", linewidth=2.2, label=r"$y = F(x) = kx + \sin x$")
    # F⁻¹ (swap x, y)
    ax.plot(Fs, xs, color="tab:red", linewidth=2.2, label=r"$y = F^{-1}(x)$")
    # y = x
    diag = np.linspace(-3 * k * np.pi, 3 * k * np.pi, 50)
    ax.plot(diag, diag, color="gray", linewidth=0.8, linestyle="--", label=r"$y = x$")

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-3 * k * np.pi, 3 * k * np.pi)
    ax.set_ylim(-3 * k * np.pi, 3 * k * np.pi)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$y$", fontsize=11)
    ax.set_title(r"$F$ and $F^{-1}$ reflect across $y = x$", fontsize=12)
    ax.legend(loc="upper left", fontsize=10)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 4 — g(x) explicit: zoom in around P₁, P₂, P₃
# ===


def make_g_explicit(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))

    m, k, n = 3, 18, 6
    q = n // m

    xs = np.linspace(-2, 20 * np.pi, 600)
    gs = _compute_g(m, k, xs)

    ax.plot(xs, gs, color="tab:blue", linewidth=2)

    # Mark all three points and dashed lines to axes
    points = [
        (m * np.pi, np.pi, r"$g(m\pi) = \pi$", "tab:green"),
        (n * np.pi, q * np.pi, r"$g(n\pi) = (n/m)\pi = 2\pi$", "tab:purple"),
        (k * np.pi, n * np.pi, r"$g(k\pi) = n\pi = 6\pi$", "tab:red"),
    ]
    for px, py, label, col in points:
        ax.plot(px, py, "o", color=col, markersize=8)
        ax.plot([px, px], [0, py], color=col, linewidth=0.7, linestyle=":")
        ax.plot([0, px], [py, py], color=col, linewidth=0.7, linestyle=":")
        ax.annotate(label, (px, py), xytext=(8, 8), textcoords="offset points",
                    fontsize=11, color=col)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-2, 20 * np.pi)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$g(x)$", fontsize=11)
    ax.set_title(r"$g$ evaluates exactly at multiples of $\pi$ when $n/m \in \mathbb{N}$", fontsize=11)
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 5 — three tangent slopes equal α = 1/m
# ===


def make_three_tangents(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))

    m, k, n = 3, 18, 6
    q = n // m
    alpha = 1.0 / m

    xs = np.linspace(-2, 20 * np.pi, 600)
    gs = _compute_g(m, k, xs)
    ax.plot(xs, gs, color="tab:blue", linewidth=2)

    # Three tangent lines
    points = [
        (m * np.pi, np.pi, "tab:green"),
        (n * np.pi, q * np.pi, "tab:purple"),
        (k * np.pi, n * np.pi, "tab:red"),
    ]
    for px, py, col in points:
        # Tangent line: y - py = alpha (x - px)
        tx = np.linspace(px - 4, px + 4, 30)
        ty = py + alpha * (tx - px)
        ax.plot(tx, ty, color=col, linewidth=2, linestyle="--")
        ax.plot(px, py, "o", color=col, markersize=9)

    # Label
    ax.annotate(
        r"slope $\alpha = 1/m = 1/3$ at all three points",
        (10 * np.pi, 0.3),
        fontsize=12,
    )

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-2, 20 * np.pi)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$g(x)$", fontsize=11)
    ax.set_title(r"Three tangent slopes equal  $(m, n, k) = (3, 6, 18)$", fontsize=12)
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 6 — search space: lattice (m, n) with m odd, m | n, m < n, mn ≤ 26
# ===


def make_search_space(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 6.5))

    # Plot grid of (m, n) for m, n natural up to 26
    max_val = 27
    for m_val in range(1, max_val):
        for n_val in range(1, max_val):
            valid = (
                m_val < n_val
                and n_val < m_val * n_val
                and m_val * n_val <= 26
                and m_val % 2 == 1
                and n_val % m_val == 0
            )
            partial = (m_val < n_val) and (m_val * n_val <= 26)

            if valid:
                ax.plot(m_val, n_val, "o", color="tab:red", markersize=14)
                ax.annotate(rf"$({m_val}, {n_val})$", (m_val, n_val),
                            xytext=(8, 6), textcoords="offset points",
                            fontsize=12, color="tab:red", fontweight="bold")
            elif partial:
                ax.plot(m_val, n_val, ".", color="tab:gray", markersize=3, alpha=0.4)

    # Boundary curve mn = 26
    ms = np.linspace(0.5, 26, 200)
    ax.plot(ms, 26.0 / ms, color="tab:blue", linewidth=1.2, linestyle="--",
            label=r"$mn = 26$")
    ax.fill_between(ms, ms, 26.0 / ms, where=(26.0 / ms > ms), color="tab:blue", alpha=0.05)

    # Line n = m
    ms2 = np.linspace(1, 26, 50)
    ax.plot(ms2, ms2, color="tab:green", linewidth=1, linestyle=":",
            label=r"$n = m$")

    ax.set_xlim(0.5, 10)
    ax.set_ylim(0.5, 20)
    ax.set_xlabel(r"$m$  (must be odd, $\geq 3$)", fontsize=11)
    ax.set_ylabel(r"$n$  (must be a multiple of $m$, $n > m$)", fontsize=11)
    ax.set_title(
        r"Lattice search for $(m, n)$: only $(3, 6)$ satisfies all constraints",
        fontsize=11,
    )
    ax.legend(loc="upper right", fontsize=10)
    ax.set_xticks(range(1, 11))
    ax.set_yticks(range(1, 21, 2))
    ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Entry point
# ===

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    make_F_monotone(out_dir / "example1_F_monotone.png")
    make_implicit(out_dir / "example2_implicit.png")
    make_F_invertible(out_dir / "exercise1_F_invertible.png")
    make_g_explicit(out_dir / "exercise2_g_explicit.png")
    make_three_tangents(out_dir / "exercise3_three_tangents.png")
    make_search_space(out_dir / "exercise3_search_space.png")
    print(f"Wrote figures to {out_dir}")
