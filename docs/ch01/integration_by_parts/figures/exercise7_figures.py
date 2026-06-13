"""Figures for 연습문제 7 in integration_by_parts.md.

Generates two PNGs in this directory:

- ``exercise7_setup.png``  : curve y = f(x) with the unit circle at P and
  highlighted arc ℓ(x).
- ``exercise7_cases.png``  : two-case diagram of triangle PHQ for
  f(x) ≤ 0 and f(x) > 0.

Run with ``python exercise7_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

# ===
# Figure 1 — setup with y = f(x) curve and sample circle
# ===


def make_setup(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(5.5, 4.5))

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)

    xs = np.linspace(-0.2, 2.05, 250)
    ys = xs**3 - 4 * xs**2 + 5 * xs - 1
    ax.plot(xs, ys, color="black", linewidth=1.0)

    px = 0.5
    py = px**3 - 4 * px**2 + 5 * px - 1

    ax.add_patch(Circle((px, py), 1, fill=False, color="black", linewidth=0.9))

    if py < 0:
        t_start = np.arcsin(-py)
        t_end = np.pi - t_start
    elif py > 0:
        t_start = -np.arcsin(py)
        t_end = np.pi + np.arcsin(py)
    else:
        t_start, t_end = 0.0, np.pi
    ts = np.linspace(t_start, t_end, 200)
    ax.plot(px + np.cos(ts), py + np.sin(ts), color="red", linewidth=2.5)

    ax.plot(px, py, "ko", markersize=4)
    ax.annotate("P", (px, py), xytext=(6, -10), textcoords="offset points", fontsize=11)

    mid_t = (t_start + t_end) / 2
    ax.annotate(
        r"$\ell(x)$",
        (px + np.cos(mid_t) + 0.05, py + np.sin(mid_t) - 0.1),
        color="red",
        fontsize=12,
    )

    ax.annotate(r"$y = f(x)$", (1.55, 1.4), fontsize=11)

    ax.set_xlim(-1.3, 2.3)
    ax.set_ylim(-1.8, 2.0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.annotate(r"$x$", (2.2, -0.18), fontsize=12)
    ax.annotate(r"$y$", (-0.18, 1.85), fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 2 — two cases of triangle PHQ
# ===


def _draw_case(ax, py: float, title: str, angle_label: str) -> None:
    ax.axhline(0, color="black", linewidth=0.8)
    ax.add_patch(Circle((0, py), 1, fill=False, color="black", linewidth=0.9))

    if py < 0:
        t_start = np.arcsin(-py)
        t_end = np.pi - t_start
    else:
        t_start = -np.arcsin(py)
        t_end = np.pi + np.arcsin(py)
    ts = np.linspace(t_start, t_end, 200)
    ax.plot(np.cos(ts), py + np.sin(ts), color="red", linewidth=2.5)

    qx = np.cos(t_start)

    ax.plot([0, 0], [py, 0], color="black", linestyle="--", linewidth=0.8)
    ax.plot([0, qx], [py, 0], color="black", linestyle="--", linewidth=0.8)
    ax.plot([0, qx], [py, py], color="black", linestyle="--", linewidth=0.8)

    ax.plot(0, py, "ko", markersize=4)
    ax.annotate("P(x, f(x))", (0, py),
                xytext=(8, -3 if py < 0 else 6),
                textcoords="offset points", fontsize=10)
    ax.plot(0, 0, "ko", markersize=4)
    ax.annotate("H", (0, 0),
                xytext=(-14 if py > 0 else 7, 6 if py < 0 else -14),
                textcoords="offset points", fontsize=11)
    ax.plot(qx, 0, "ko", markersize=4)
    ax.annotate("Q", (qx, 0), xytext=(6, 6), textcoords="offset points", fontsize=11)

    half_angle_label_y = py + (0.22 if py < 0 else -0.28)
    ax.annotate(angle_label,
                (0.08, half_angle_label_y), fontsize=10)

    mid_t = (t_start + t_end) / 2
    ax.annotate(r"$\ell(x)$",
                (np.cos(mid_t) + 0.05, py + np.sin(mid_t) - 0.05),
                color="red", fontsize=12)

    ax.set_title(title, fontsize=11)

    ax.set_xlim(-1.6, 1.9)
    ax.set_ylim(-1.8, 1.8)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.annotate(r"$x$", (1.8, -0.18), fontsize=11)


def make_endpoints(out_path: Path) -> None:
    """Figure showing the two endpoint configurations at x = 0 and x = 1."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # --- x = 0: P = (0, -1), circle tangent to x-axis from below ---
    ax1.axhline(0, color="black", linewidth=0.8)
    ax1.add_patch(Circle((0, -1), 1, fill=False, color="black", linewidth=0.9))
    # ℓ(0) = 0: arc degenerates to the single tangent point at origin
    ax1.plot(0, 0, "o", color="red", markersize=9)
    ax1.plot(0, -1, "ko", markersize=4)
    ax1.annotate("P(0, -1)", (0, -1),
                 xytext=(8, -3), textcoords="offset points", fontsize=10)
    ax1.annotate(r"$\ell(0) = 0$", (0.08, 0.1), color="red", fontsize=12)
    ax1.set_title(r"$x = 0$:  $f(0) = -1$", fontsize=11)
    ax1.set_xlim(-1.6, 1.8)
    ax1.set_ylim(-2.4, 1.0)
    ax1.set_aspect("equal")
    ax1.set_xticks([])
    ax1.set_yticks([])
    for s in ("top", "right", "left", "bottom"):
        ax1.spines[s].set_visible(False)
    ax1.annotate(r"$x$", (1.7, -0.18), fontsize=11)

    # --- x = 1: P = (1, 1), circle tangent to x-axis from above ---
    ax2.axhline(0, color="black", linewidth=0.8)
    # The arc ℓ(1) = 2π is the entire circle (above x-axis)
    ax2.add_patch(Circle((1, 1), 1, fill=False, color="red", linewidth=2.5))
    ax2.plot(1, 1, "ko", markersize=4)
    ax2.annotate("P(1, 1)", (1, 1),
                 xytext=(8, -3), textcoords="offset points", fontsize=10)
    ax2.annotate(r"$\ell(1) = 2\pi$", (1.15, 1.6), color="red", fontsize=12)
    ax2.set_title(r"$x = 1$:  $f(1) = 1$", fontsize=11)
    ax2.set_xlim(-0.6, 2.8)
    ax2.set_ylim(-0.6, 2.8)
    ax2.set_aspect("equal")
    ax2.set_xticks([])
    ax2.set_yticks([])
    for s in ("top", "right", "left", "bottom"):
        ax2.spines[s].set_visible(False)
    ax2.annotate(r"$x$", (2.7, -0.18), fontsize=11)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def make_cases(out_path: Path) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    _draw_case(ax1, py=-0.5, title=r"$f(x) \leq 0$",
               angle_label=r"$\frac{1}{2}\ell(x)$")
    _draw_case(ax2, py=0.5, title=r"$f(x) > 0$",
               angle_label=r"$\pi - \frac{1}{2}\ell(x)$")
    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Entry point
# ===

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    make_setup(out_dir / "exercise7_setup.png")
    make_endpoints(out_dir / "exercise7_endpoints.png")
    make_cases(out_dir / "exercise7_cases.png")
    print(f"Wrote figures to {out_dir}")
