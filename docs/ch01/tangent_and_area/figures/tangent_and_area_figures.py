"""Figures for tangent_and_area.md.

Generates PNGs in this directory:

- ``example1_derivative.png``     : visualisation of the derivative as the
  slope of the tangent line at a point.
- ``example2_FTC.png``            : (1/x) ∫_1^(x+1) k(t) dt  →  k(1) as x → 0
  visualised as the difference quotient.
- ``exercise1_tan_value.png``     : f(x) = cos x - sin x with f(a) = 0
  at a = π/4 (smallest positive solution of tan a = 1).
- ``exercise2_two_curves.png``    : g(x) = (cos x - sin x) e^(-x) and
  h(x) = b e^(-x) for b = √2 — they touch at p₁ = 7π/4, p₂ = 15π/4, ...
- ``exercise3_zeros.png``         : zeros of g(x) at x = π/4 + nπ and the
  signed area A_k between consecutive zeros.
- ``exercise3_decay.png``         : log-scale comparison of A_1, A_2, ...
  showing the geometric decay ratio e^(-π).

Run with ``python tangent_and_area_figures.py``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def _f(x):
    return np.cos(x) - np.sin(x)


def _g(x):
    return _f(x) * np.exp(-x)


# ===
# Figure 1 — Derivative as slope of tangent line
# ===


def make_derivative(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 5))

    xs = np.linspace(-1.6, 2.2, 300)
    ys = 0.4 * xs**3 - 0.8 * xs**2 + 0.5 * xs + 1.2

    ax.plot(xs, ys, color="tab:blue", linewidth=2.2)
    ax.annotate(r"$y = f(x)$", (-1.4, 0.4), fontsize=12, color="tab:blue")

    # Tangent line at a = 1
    a = 1.0
    fa = 0.4 * a**3 - 0.8 * a**2 + 0.5 * a + 1.2
    fpa = 1.2 * a**2 - 1.6 * a + 0.5  # derivative
    tan_xs = np.linspace(a - 1.3, a + 1.3, 50)
    tan_ys = fa + fpa * (tan_xs - a)
    ax.plot(tan_xs, tan_ys, color="tab:red", linewidth=1.8, linestyle="--")
    ax.annotate(
        r"$y - f(a) = f'(a)\,(x - a)$",
        (1.6, 1.6),
        fontsize=12,
        color="tab:red",
    )

    # Mark point of tangency
    ax.plot(a, fa, "o", color="black", markersize=7)
    ax.annotate(
        rf"$(a,\,f(a))$",
        (a, fa),
        xytext=(8, -12),
        textcoords="offset points",
        fontsize=11,
    )

    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.set_xlim(-1.7, 2.6)
    ax.set_ylim(-0.2, 2.5)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_title(r"Tangent line at $(a, f(a))$ has slope $f'(a)$", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 2 — FTC: (1/x) ∫_1^{x+1} k(t) dt → k(1) as x → 0
# ===


def make_FTC(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))

    ts = np.linspace(0.5, 2.5, 300)
    ks = np.exp(-((ts) ** 2)) * (np.cos(ts) - np.sin(ts))  # k(t) = e^(-t²) f(t) for a = 1
    ax.plot(ts, ks, color="tab:blue", linewidth=2)

    # Highlight strip [1, 1 + x] for x = 0.3
    x_demo = 0.3
    mask = (ts >= 1) & (ts <= 1 + x_demo)
    ax.fill_between(ts[mask], ks[mask], 0, alpha=0.35, color="tab:orange")
    ax.axvline(1, color="gray", linewidth=0.7, linestyle="--")
    ax.axvline(1 + x_demo, color="gray", linewidth=0.7, linestyle="--")
    ax.annotate(r"$t = 1$", (1, -0.35), fontsize=10, color="gray", ha="center")
    ax.annotate(r"$t = 1 + x$", (1 + x_demo, -0.35), fontsize=10, color="gray", ha="center")

    # Mark k(1)
    k1 = np.exp(-1) * (np.cos(1) - np.sin(1))
    ax.plot(1, k1, "o", color="tab:red", markersize=7)
    ax.annotate(
        r"$k(1) = e^{-a^2}(\cos a - \sin a)$",
        (1, k1),
        xytext=(20, -10),
        textcoords="offset points",
        fontsize=11,
        color="tab:red",
    )

    ax.annotate(
        r"$\frac{1}{x}\,\int_1^{x+1} k(t)\,dt \to k(1)$  as $x \to 0$",
        (0.55, 0.4),
        fontsize=12,
    )

    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_xlim(0.4, 2.6)
    ax.set_ylim(-0.5, 0.6)
    ax.set_xlabel(r"$t$", fontsize=11)
    ax.set_ylabel(r"$k(t)$", fontsize=11)
    ax.set_title(r"FTC: difference quotient of the integral converges to $k(1)$", fontsize=11)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 3 — f(x) = cos x - sin x with zero at a = π/4
# ===


def make_tan_value(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))

    xs = np.linspace(0, 2 * np.pi, 400)
    ys = _f(xs)
    ax.plot(xs, ys, color="tab:blue", linewidth=2.2)

    # Mark zeros: cos a = sin a → a = π/4 + nπ
    a_first = np.pi / 4
    ax.plot(a_first, 0, "o", color="tab:red", markersize=9)
    ax.annotate(
        r"$a = \frac{\pi}{4}$  (smallest)",
        (a_first, 0),
        xytext=(15, 12),
        textcoords="offset points",
        fontsize=12,
        color="tab:red",
        arrowprops=dict(arrowstyle="->", color="tab:red"),
    )

    a_second = 5 * np.pi / 4
    ax.plot(a_second, 0, "o", color="tab:gray", markersize=6)
    ax.annotate(
        r"$\frac{5\pi}{4}$",
        (a_second, 0),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=11,
        color="tab:gray",
    )

    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_xlim(0, 2 * np.pi + 0.1)
    ax.set_ylim(-1.6, 1.6)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_title(r"$f(x) = \cos x - \sin x$;  zeros at $x = \frac{\pi}{4} + n\pi$", fontsize=12)
    ax.set_xticks([0, np.pi / 4, np.pi / 2, np.pi, 5 * np.pi / 4, 3 * np.pi / 2, 2 * np.pi])
    ax.set_xticklabels(["0", r"$\frac{\pi}{4}$", r"$\frac{\pi}{2}$", r"$\pi$",
                        r"$\frac{5\pi}{4}$", r"$\frac{3\pi}{2}$", r"$2\pi$"])

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 4 — Two curves g(x) and h(x) = b e^(-x) tangent at meeting points
# ===


def make_two_curves(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.5, 5))

    xs = np.linspace(0, 6 * np.pi, 600)
    g_vals = _g(xs)
    b = np.sqrt(2.0)
    h_vals = b * np.exp(-xs)

    ax.plot(xs, g_vals, color="tab:blue", linewidth=2, label=r"$g(x) = (\cos x - \sin x)\,e^{-x}$")
    ax.plot(xs, h_vals, color="tab:red", linewidth=2, label=rf"$h(x) = \sqrt{{2}}\,e^{{-x}}$")

    # Meeting points: 7π/4, 15π/4, ...
    meeting_xs = [7 * np.pi / 4, 15 * np.pi / 4, 23 * np.pi / 4]
    for i, p in enumerate(meeting_xs):
        if p > 6 * np.pi:
            break
        ax.plot(p, _g(p), "o", color="black", markersize=7)
        label = r"$p_1 = \frac{7\pi}{4}$" if i == 0 else (r"$p_2 = \frac{15\pi}{4}$" if i == 1 else None)
        if label is not None:
            ax.annotate(label, (p, _g(p)), xytext=(10, 10), textcoords="offset points", fontsize=11)

    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_xlim(0, 6 * np.pi)
    ax.set_ylim(-0.4, 1.6)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_title(
        r"$y = g(x)$ touches $y = h(x)$ at $p_n = \frac{7\pi}{4} + 2(n-1)\pi$",
        fontsize=11,
    )
    ax.legend(loc="upper right", fontsize=11)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 5 — Zeros of g and the signed area A_k
# ===


def make_zeros_area(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.5, 4.5))

    xs = np.linspace(0, 6 * np.pi, 800)
    g_vals = _g(xs)
    ax.plot(xs, g_vals, color="tab:blue", linewidth=2)
    ax.axhline(0, color="black", linewidth=0.6)

    # Zeros at x = π/4 + (k-1)π for k = 1, 2, ...
    zeros = [np.pi / 4 + (k - 1) * np.pi for k in range(1, 7)]

    # Shade A_1, A_2, A_3
    colors = ["tab:orange", "tab:green", "tab:purple", "tab:orange", "tab:green", "tab:purple"]
    for k, (z1, z2, color) in enumerate(zip(zeros[:-1], zeros[1:], colors)):
        ts = np.linspace(z1, z2, 100)
        gs_k = _g(ts)
        ax.fill_between(ts, gs_k, 0, alpha=0.35, color=color)
        mid = (z1 + z2) / 2
        ymid = _g(mid)
        ax.annotate(
            rf"$A_{{{k+1}}}$",
            (mid, ymid / 2 if abs(ymid) > 0.05 else 0.04),
            fontsize=11,
            ha="center",
        )

    # Mark zeros
    for k, z in enumerate(zeros, start=1):
        ax.plot(z, 0, "o", color="black", markersize=4)
        if k <= 6:
            ax.annotate(rf"$x_{{{k}}}$", (z, 0.04), fontsize=9, ha="center")

    ax.set_xlim(0, 6 * np.pi)
    ax.set_ylim(-0.5, 1.0)
    ax.set_xlabel(r"$x$", fontsize=11)
    ax.set_ylabel(r"$g(x)$", fontsize=11)
    ax.set_title(r"Zeros $x_k = \frac{\pi}{4} + (k-1)\pi$ and areas $A_k$", fontsize=11)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Figure 6 — Geometric decay of A_k
# ===


def make_decay(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    def Ak(k):
        # |[e^(-x) sin x]_{x_k}^{x_{k+1}}|
        # x_k = π/4 + (k-1)π
        x_k = np.pi / 4 + (k - 1) * np.pi
        x_k1 = np.pi / 4 + k * np.pi
        val_low = np.exp(-x_k) * np.sin(x_k)
        val_high = np.exp(-x_k1) * np.sin(x_k1)
        return abs(val_high - val_low)

    ks = np.arange(1, 9)
    A_vals = np.array([Ak(k) for k in ks])

    ax.semilogy(ks, A_vals, "o-", color="tab:blue", linewidth=2, markersize=8)

    # Theoretical: A_k = A_1 * e^(-(k-1)π)
    A1 = A_vals[0]
    theoretical = A1 * np.exp(-(ks - 1) * np.pi)
    ax.semilogy(ks, theoretical, "x", color="tab:red", markersize=10,
                label=r"$A_1\,e^{-(k-1)\pi}$")

    ax.set_xlabel(r"$k$", fontsize=11)
    ax.set_ylabel(r"$A_k$  (log scale)", fontsize=11)
    ax.set_title(r"Geometric decay: $A_{k+1}/A_k = e^{-\pi}$", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3, which="both")

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ===
# Entry point
# ===

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    make_derivative(out_dir / "example1_derivative.png")
    make_FTC(out_dir / "example2_FTC.png")
    make_tan_value(out_dir / "exercise1_tan_value.png")
    make_two_curves(out_dir / "exercise2_two_curves.png")
    make_zeros_area(out_dir / "exercise3_zeros.png")
    make_decay(out_dir / "exercise3_decay.png")
    print(f"Wrote figures to {out_dir}")
