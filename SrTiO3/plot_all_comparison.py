#!/usr/bin/env python3
"""Plot SrTiO3 XANES: HCH calculations vs all experimental EELS delta series.

Experimental EELS from David Muller — SrTiO_{3-δ} for δ ≈ 0, 0.13, 0.25.
Digitized CSV files in O-K/ and Ti-L/ directories.

Two panels: (a) O K-edge, (b) Ti L-edge.
Calculated spectra aligned to δ≈0 experiment by matching first peak positions.
"""

import numpy as np
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt


def load_expt(csv_path, smooth_sigma=1.5):
    """Load digitized experimental CSV (Energy,Intensity) and smooth."""
    d = np.loadtxt(csv_path, delimiter=",", skiprows=1)
    idx = np.argsort(d[:, 0])
    energy, intensity = d[idx, 0], d[idx, 1]
    intensity -= intensity.min()
    intensity /= intensity.max()
    intensity_smooth = gaussian_filter1d(intensity, sigma=smooth_sigma)
    return energy, intensity_smooth


def find_first_peak(energy, intensity, search_frac=0.4):
    """Find energy of the first prominent peak in the first fraction of data."""
    n = int(len(energy) * search_frac)
    return energy[np.argmax(intensity[:n])]


# --- Load experimental data ---
# Color mapping from original figure:
#   blue  = δ ≈ 0    (stoichiometric)
#   red   = δ ≈ 0.13
#   black = δ ≈ 0.25

expt_labels = {
    "blue":  r"Expt. $\delta\approx0$",
    "red":   r"Expt. $\delta\approx0.13$",
    "black": r"Expt. $\delta\approx0.25$",
}
expt_colors = {
    "blue":  "#8b0000",
    "red":   "#cc4400",
    "black": "#e69500",
}
expt_styles = {
    "blue":  dict(lw=1.8, ls="-"),
    "red":   dict(lw=1.5, ls="--"),
    "black": dict(lw=1.2, ls=":"),
}

o_expt = {}
for color in ["blue", "red", "black"]:
    e, i = load_expt(f"O-K/data_{color}_clean.csv")
    o_expt[color] = (e, i)

ti_expt = {}
for color in ["blue", "red", "black"]:
    e, i = load_expt(f"Ti-L/data_{color}_clean.csv")
    ti_expt[color] = (e, i)

# --- Load calculated spectra ---
o_hch_uc = np.loadtxt("../reference_output/SrTiO3/O_Kedge_HCH/O_Kedge_HCH.dat")
o_hch_sc = np.loadtxt("../reference_output/SrTiO3/O_Kedge_HCH_super/O_Kedge_HCH_super.dat")
ti_hch_uc = np.loadtxt("../reference_output/SrTiO3/Ti_Ledge_HCH/Ti_Ledge_HCH.dat")
ti_hch_sc = np.loadtxt("../reference_output/SrTiO3/Ti_Ledge_HCH_super/Ti_Ledge_HCH_super.dat")

for arr in [o_hch_uc, o_hch_sc, ti_hch_uc, ti_hch_sc]:
    arr[:, 1] -= arr[:, 1].min()
    arr[:, 1] /= arr[:, 1].max()

# --- Align calculated to δ≈0 experiment (first peak matching) ---
# O K-edge
expt_peak_o = find_first_peak(*o_expt["blue"])
calc_peak_o_uc = find_first_peak(o_hch_uc[:, 0], o_hch_uc[:, 1])
calc_peak_o_sc = find_first_peak(o_hch_sc[:, 0], o_hch_sc[:, 1])
shift_o_uc = expt_peak_o - calc_peak_o_uc
shift_o_sc = expt_peak_o - calc_peak_o_sc

# Ti L-edge (align to highest peak — L2 eg)
EXPT_TI_L2_EG = 465.1
calc_peak_ti_uc = ti_hch_uc[np.argmax(ti_hch_uc[:, 1]), 0]
calc_peak_ti_sc = ti_hch_sc[np.argmax(ti_hch_sc[:, 1]), 0]
shift_ti_uc = EXPT_TI_L2_EG - calc_peak_ti_uc
shift_ti_sc = EXPT_TI_L2_EG - calc_peak_ti_sc

print(f"O K-edge shifts:  UC={shift_o_uc:.1f} eV, SC={shift_o_sc:.1f} eV")
print(f"Ti L-edge shifts: UC={shift_ti_uc:.1f} eV, SC={shift_ti_sc:.1f} eV")

# --- Plot ---
calc_color_uc = "#2166ac"
calc_color_sc = "#2ca02c"

fig, axes = plt.subplots(2, 1, figsize=(10, 9), constrained_layout=True)

# (a) O K-edge
ax = axes[0]
for color in ["blue", "red", "black"]:
    e, i = o_expt[color]
    ax.plot(e, i, color=expt_colors[color], label=expt_labels[color],
            **expt_styles[color])

ax.plot(o_hch_uc[:, 0] + shift_o_uc, o_hch_uc[:, 1],
        color=calc_color_uc, lw=2.0, label="Calc. HCH unit cell")
ax.plot(o_hch_sc[:, 0] + shift_o_sc, o_hch_sc[:, 1],
        color=calc_color_sc, lw=2.0, ls="--", label="Calc. HCH 2×2×2 supercell")

ax.set_xlabel("Energy Loss (eV)")
ax.set_ylabel("Normalized Intensity (a.u.)")
ax.set_xlim(525, 555)
ax.set_ylim(-0.05, 1.15)
ax.set_title("(a) O K-edge", fontsize=13, fontweight="bold", loc="left")
ax.legend(loc="upper right", frameon=True, fancybox=False, edgecolor="0.7", fontsize=9)

# (b) Ti L-edge
ax = axes[1]
for color in ["blue", "red", "black"]:
    e, i = ti_expt[color]
    ax.plot(e, i, color=expt_colors[color], label=expt_labels[color],
            **expt_styles[color])

ax.plot(ti_hch_uc[:, 0] + shift_ti_uc, ti_hch_uc[:, 1],
        color=calc_color_uc, lw=2.0, label="Calc. HCH unit cell")
ax.plot(ti_hch_sc[:, 0] + shift_ti_sc, ti_hch_sc[:, 1],
        color=calc_color_sc, lw=2.0, ls="--", label="Calc. HCH 2×2×2 supercell")

ax.set_xlabel("Energy Loss (eV)")
ax.set_ylabel("Normalized Intensity (a.u.)")
ax.set_xlim(450, 470)
ax.set_ylim(-0.05, 1.15)
ax.set_title("(b) Ti L-edge", fontsize=13, fontweight="bold", loc="left")
ax.legend(loc="upper right", frameon=True, fancybox=False, edgecolor="0.7", fontsize=9)

fig.suptitle(r"SrTiO$_{3-\delta}$ — HCH XANES vs Experimental EELS (Muller)",
             fontsize=14, fontweight="bold")
plt.savefig("SrTiO3_all_comparison.png", dpi=150, bbox_inches="tight")
print("Saved: SrTiO3_all_comparison.png")
plt.close()
