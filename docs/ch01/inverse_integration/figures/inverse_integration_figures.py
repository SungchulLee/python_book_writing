"""Figure for ch01/inverse_integration."""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 140, "axes.grid": True, "grid.alpha": 0.25})


def fig_inverse_symmetry():
    fig, ax = plt.subplots(figsize=(7, 6))
    x = np.linspace(0, 2, 200)
    # use a sample increasing function: f(x) = x^2 / 2
    f = x**2 / 2
    ax.plot(x, f, "b-", lw=2, label=r"$y = f(x)$")
    # inverse: x = sqrt(2y), plot as y = sqrt(2x)
    yi = np.linspace(0, 2, 200)
    xi = np.sqrt(2*yi)
    ax.plot(xi, yi, "r-", lw=2, label=r"$y = f^{-1}(x)$")
    # rectangle
    ax.fill_between(x, f, alpha=0.2, color="blue", label=r"$\int_0^b f(x)\,dx$")
    # area under inverse (in y direction): plot as area on the left of f^-1
    ax.fill_betweenx(yi, 0, xi, alpha=0.2, color="red", label=r"$\int_0^{f(b)} f^{-1}(y)\,dy$")
    ax.axvline(2, color="k", ls=":", lw=0.5)
    ax.axhline(2, color="k", ls=":", lw=0.5)
    ax.set_xlim(0, 2.5); ax.set_ylim(0, 2.5)
    ax.set_aspect("equal")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title(r"$\int_0^b f\,dx + \int_0^{f(b)} f^{-1}\,dy = b\,f(b)$")
    ax.legend(fontsize=9, loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "inverse_symmetry.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_inverse_symmetry()
    print(f"figures written to {OUT}")
