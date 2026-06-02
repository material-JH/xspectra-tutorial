#!/usr/bin/env python3
"""Plot SrTiO3 O K-edge XANES vs the delta=0 experimental EELS curve.

Experimental EELS from David Muller — stoichiometric SrTiO3, δ≈0.
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


o_expt = load_expt("O-K/data_blue_clean.csv")

# --- Load calculated spectra ---
o_hch_uc = np.loadtxt("../reference_output/SrTiO3/O_Kedge_HCH/O_Kedge_HCH.dat")
o_hch_sc = np.loadtxt("../reference_output/SrTiO3/O_Kedge_HCH_super/O_Kedge_HCH_super.dat")

for arr in [o_hch_uc, o_hch_sc]:
    arr[:, 1] -= arr[:, 1].min()
    arr[:, 1] /= arr[:, 1].max()

# --- Align calculated to δ≈0 experiment (first peak matching) ---
expt_peak_o = find_first_peak(*o_expt)
calc_peak_o_uc = find_first_peak(o_hch_uc[:, 0], o_hch_uc[:, 1])
calc_peak_o_sc = find_first_peak(o_hch_sc[:, 0], o_hch_sc[:, 1])
shift_o_uc = expt_peak_o - calc_peak_o_uc
shift_o_sc = expt_peak_o - calc_peak_o_sc

print(f"O K-edge shifts:  UC={shift_o_uc:.1f} eV, SC={shift_o_sc:.1f} eV")

# --- Plot ---
calc_color_uc = "#2166ac"
calc_color_sc = "#2ca02c"

fig, ax = plt.subplots(1, 1, figsize=(9, 5.2), constrained_layout=True)

e, i = o_expt
ax.plot(e, i, color="#8b0000", lw=1.8, label=r"Expt. EELS $\delta\approx0$")

ax.plot(o_hch_uc[:, 0] + shift_o_uc, o_hch_uc[:, 1],
        color=calc_color_uc, lw=2.0, label="Calc. HCH unit cell")
ax.plot(o_hch_sc[:, 0] + shift_o_sc, o_hch_sc[:, 1],
        color=calc_color_sc, lw=2.0, ls="--", label="Calc. HCH 2×2×2 supercell")

ax.set_xlabel("Energy Loss (eV)")
ax.set_ylabel("Normalized Intensity (a.u.)")
ax.set_xlim(525, 555)
ax.set_ylim(-0.05, 1.15)
ax.set_title("O K-edge", fontsize=13, fontweight="bold", loc="left")
ax.legend(loc="upper right", frameon=True, fancybox=False, edgecolor="0.7", fontsize=9)

fig.suptitle(r"SrTiO$_3$ O K-edge — HCH XANES vs Experimental EELS ($\delta\approx0$)",
             fontsize=14, fontweight="bold")
plt.savefig("SrTiO3_all_comparison.png", dpi=150, bbox_inches="tight")
print("Saved: SrTiO3_all_comparison.png")
plt.close()
