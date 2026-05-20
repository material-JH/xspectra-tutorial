#!/usr/bin/env python3
"""Plot the curated Diamond XSpectra reference output.

Run from the repository root:

    python3 plot_spectra.py

The SrTiO3 plots are generated separately with:

    cd SrTiO3 && python3 plot_spectra.py
"""
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent


def load_xanes(filepath: Path) -> np.ndarray:
    if not filepath.exists():
        raise FileNotFoundError(
            f"Missing {filepath}. Run the Diamond example or keep reference_output/diamond/."
        )
    return np.loadtxt(filepath)


def main() -> None:
    ref = BASE / "reference_output" / "diamond"
    raw = load_xanes(ref / "diamond.xspectra.dat")
    no_hole = load_xanes(ref / "diamond.xspectra_replot.dat")
    full_hole = load_xanes(ref / "diamondh.xspectra.dat")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)

    ax1.plot(raw[:, 0], raw[:, 1], color="0.55", alpha=0.65, label="No core-hole, occupied states included")
    ax1.plot(no_hole[:, 0], no_hole[:, 1], color="C0", label="No core-hole, occupied states cut")
    ax1.plot(full_hole[:, 0], full_hole[:, 1], color="C3", label="Full core-hole, occupied states cut")
    ax1.set_title("Diamond C K-edge")
    ax1.set_xlabel("Energy (eV)")
    ax1.set_ylabel("Absorption cross-section (arb. units)")
    ax1.set_xlim(-5, 30)
    ax1.legend(fontsize=8)

    ax2.plot(no_hole[:, 0], no_hole[:, 1], color="C0", label="No core-hole")
    ax2.plot(full_hole[:, 0], full_hole[:, 1], color="C3", label="Full core-hole")
    ax2.set_title("Core-hole effect")
    ax2.set_xlabel("Energy (eV)")
    ax2.set_ylabel("Absorption cross-section (arb. units)")
    ax2.set_xlim(-2, 25)
    ax2.legend(fontsize=8)

    outpath = BASE / "xanes_spectra.png"
    fig.savefig(outpath, dpi=180, facecolor="white")
    print(f"Saved: {outpath}")

    if "--show" in sys.argv:
        plt.show()


if __name__ == "__main__":
    main()
