#!/usr/bin/env python3
"""Generate slide-friendly plots for docs/xspectra_tutorial_presentation.html.

The full tutorial/reference plots are intentionally detailed and often portrait
or near-square.  The HTML presentation uses a 16:9 slide canvas with text next to
figures, so these companion plots are redrawn in a wide layout with larger labels
and legends that fit inside the slide image frames.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "docs" / "assets"


def load_xanes(path: Path) -> np.ndarray:
    return np.loadtxt(path)


def normalize(intensity: np.ndarray) -> np.ndarray:
    arr = np.asarray(intensity, dtype=float).copy()
    arr -= np.nanmin(arr)
    max_val = np.nanmax(arr)
    if max_val > 0:
        arr /= max_val
    return arr


def load_experiment(csv_path: Path, smooth_sigma: float = 1.5) -> tuple[np.ndarray, np.ndarray]:
    data = np.loadtxt(csv_path, delimiter=",", skiprows=1)
    data = data[np.argsort(data[:, 0])]
    energy = data[:, 0]
    intensity = normalize(data[:, 1])
    return energy, gaussian_filter1d(intensity, sigma=smooth_sigma)


def find_first_peak(energy: np.ndarray, intensity: np.ndarray, search_frac: float = 0.4) -> float:
    n = max(1, int(len(energy) * search_frac))
    return float(energy[np.argmax(intensity[:n])])


def save_diamond_plot() -> Path:
    d_raw = load_xanes(ROOT / "reference_output/diamond/diamond.xspectra.dat")
    d_no_hole = load_xanes(ROOT / "reference_output/diamond/diamond.xspectra_replot.dat")
    d_hole = load_xanes(ROOT / "reference_output/diamond/diamondh.xspectra.dat")

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.5), constrained_layout=True)

    ax = axes[0]
    ax.plot(d_raw[:, 0], normalize(d_raw[:, 1]), color="0.45", lw=1.7, alpha=0.75,
            label="No core-hole, raw")
    ax.plot(d_no_hole[:, 0], normalize(d_no_hole[:, 1]), color="#2166ac", lw=2.2,
            label="No core-hole, occ. cut")
    ax.plot(d_hole[:, 0], normalize(d_hole[:, 1]), color="#d6604d", lw=2.2,
            label="Full core-hole")
    ax.set_title("(a) Diamond C K-edge workflow output", loc="left", fontweight="bold")
    ax.set_xlim(-5, 30)
    ax.set_xlabel("Relative energy (eV)")
    ax.set_ylabel("Normalized absorption")
    ax.legend(loc="upper right", fontsize=8, frameon=True)
    ax.grid(True, alpha=0.22)

    ax = axes[1]
    ax.plot(d_no_hole[:, 0], normalize(d_no_hole[:, 1]), color="#2166ac", lw=2.4,
            label="No core-hole")
    ax.plot(d_hole[:, 0], normalize(d_hole[:, 1]), color="#d6604d", lw=2.4,
            label="Full core-hole")
    ax.set_title("(b) Same run, different core-hole model", loc="left", fontweight="bold")
    ax.set_xlim(-2, 25)
    ax.set_xlabel("Relative energy (eV)")
    ax.set_ylabel("Normalized absorption")
    ax.legend(loc="upper right", fontsize=8, frameon=True)
    ax.grid(True, alpha=0.22)

    fig.suptitle("Diamond XSpectra example — slide-friendly view", fontsize=14, fontweight="bold")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    outpath = OUTDIR / "presentation_diamond_ckedge.png"
    fig.savefig(outpath, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return outpath


def save_srtio3_comparison_plot() -> Path:
    o_expt = {
        key: load_experiment(ROOT / "SrTiO3" / "O-K" / f"data_{key}_clean.csv")
        for key in ("blue", "red", "black")
    }
    ti_expt = {
        key: load_experiment(ROOT / "SrTiO3" / "Ti-L" / f"data_{key}_clean.csv")
        for key in ("blue", "red", "black")
    }

    o_hch_uc = load_xanes(ROOT / "reference_output/SrTiO3/O_Kedge_HCH/O_Kedge_HCH.dat")
    o_hch_sc = load_xanes(ROOT / "reference_output/SrTiO3/O_Kedge_HCH_super/O_Kedge_HCH_super.dat")
    ti_hch_uc = load_xanes(ROOT / "reference_output/SrTiO3/Ti_Ledge_HCH/Ti_Ledge_HCH.dat")
    ti_hch_sc = load_xanes(ROOT / "reference_output/SrTiO3/Ti_Ledge_HCH_super/Ti_Ledge_HCH_super.dat")

    for arr in (o_hch_uc, o_hch_sc, ti_hch_uc, ti_hch_sc):
        arr[:, 1] = normalize(arr[:, 1])

    expt_peak_o = find_first_peak(*o_expt["blue"])
    shift_o_uc = expt_peak_o - find_first_peak(o_hch_uc[:, 0], o_hch_uc[:, 1])
    shift_o_sc = expt_peak_o - find_first_peak(o_hch_sc[:, 0], o_hch_sc[:, 1])

    expt_ti_l2_eg = 465.1
    shift_ti_uc = expt_ti_l2_eg - ti_hch_uc[np.argmax(ti_hch_uc[:, 1]), 0]
    shift_ti_sc = expt_ti_l2_eg - ti_hch_sc[np.argmax(ti_hch_sc[:, 1]), 0]

    expt_labels = {
        "blue": r"Expt. $\delta\approx0$",
        "red": r"Expt. $\delta\approx0.13$",
        "black": r"Expt. $\delta\approx0.25$",
    }
    expt_colors = {"blue": "#8b0000", "red": "#cc4400", "black": "#e69500"}
    expt_styles = {
        "blue": dict(lw=1.8, ls="-"),
        "red": dict(lw=1.5, ls="--"),
        "black": dict(lw=1.3, ls=":"),
    }

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.5), constrained_layout=True)

    ax = axes[0]
    for key in ("blue", "red", "black"):
        energy, intensity = o_expt[key]
        ax.plot(energy, intensity, color=expt_colors[key], label=expt_labels[key],
                **expt_styles[key])
    ax.plot(o_hch_uc[:, 0] + shift_o_uc, o_hch_uc[:, 1], color="#2166ac", lw=2.2,
            label="Calc. HCH unit cell")
    ax.plot(o_hch_sc[:, 0] + shift_o_sc, o_hch_sc[:, 1], color="#2ca02c", lw=2.2,
            ls="--", label="Calc. HCH 2×2×2")
    ax.set_title("(a) SrTiO3 O K-edge", loc="left", fontweight="bold")
    ax.set_xlim(525, 555)
    ax.set_ylim(-0.05, 1.15)
    ax.set_xlabel("Energy loss (eV)")
    ax.set_ylabel("Normalized intensity")
    ax.legend(loc="upper right", fontsize=7.3, frameon=True)
    ax.grid(True, alpha=0.22)

    ax = axes[1]
    for key in ("blue", "red", "black"):
        energy, intensity = ti_expt[key]
        ax.plot(energy, intensity, color=expt_colors[key], label=expt_labels[key],
                **expt_styles[key])
    ax.plot(ti_hch_uc[:, 0] + shift_ti_uc, ti_hch_uc[:, 1], color="#2166ac", lw=2.2,
            label="Calc. HCH unit cell")
    ax.plot(ti_hch_sc[:, 0] + shift_ti_sc, ti_hch_sc[:, 1], color="#2ca02c", lw=2.2,
            ls="--", label="Calc. HCH 2×2×2")
    ax.set_title("(b) SrTiO3 Ti L-edge", loc="left", fontweight="bold")
    ax.set_xlim(450, 470)
    ax.set_ylim(-0.05, 1.15)
    ax.set_xlabel("Energy loss (eV)")
    ax.set_ylabel("Normalized intensity")
    ax.legend(loc="upper right", fontsize=7.3, frameon=True)
    ax.grid(True, alpha=0.22)

    fig.suptitle(r"SrTiO$_{3-\delta}$ — calculated HCH XANES vs experimental EELS",
                 fontsize=14, fontweight="bold")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    outpath = OUTDIR / "presentation_srtio3_eels_comparison.png"
    fig.savefig(outpath, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return outpath


def main() -> None:
    for outpath in (save_diamond_plot(), save_srtio3_comparison_plot()):
        print(f"Saved: {outpath.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
