#!/usr/bin/env python3
"""Digitize experimental EELS spectra from David Muller's SrTiO3 figure,
determine onset energies, and plot together with calculated XSpectra results."""

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt


def extract_blue_curve(arr, row_min, row_max, col_min, col_max):
    """Extract the delta=0 (blue solid) curve from a panel region.
    Returns (col_positions, row_positions) of the curve centerline."""
    region = arr[row_min:row_max, col_min:col_max, :].astype(float)
    r, g, b = region[:,:,0], region[:,:,1], region[:,:,2]

    blue_score = b - 0.5 * (r + g)
    blue_mask = (blue_score > 40) & (b > 80)

    cols_out = []
    rows_out = []
    height = row_max - row_min

    for c in range(blue_mask.shape[1]):
        col_pixels = np.where(blue_mask[:, c])[0]
        if len(col_pixels) == 0:
            continue
        weights = blue_score[col_pixels, c]
        weights = np.clip(weights, 0, None)
        if weights.sum() > 0:
            centroid = np.average(col_pixels, weights=weights)
        else:
            centroid = np.mean(col_pixels)
        cols_out.append(c + col_min)
        rows_out.append(centroid + row_min)

    return np.array(cols_out), np.array(rows_out)


def pixel_to_data(px_coords, calib_points):
    """Linear mapping from pixel to data coordinates.
    calib_points: list of (pixel, data_value) tuples."""
    px = np.array([p[0] for p in calib_points])
    dv = np.array([p[1] for p in calib_points])
    slope, intercept = np.polyfit(px, dv, 1)
    return slope * px_coords + intercept


img = Image.open("EELS_STO_david_muller.png")
arr = np.array(img)[:, :, :3]

# Panel (a) O K-edge calibration:
#   x-axis: col 207=530eV, 341=540eV, 476=550eV
#   y-axis: row 270=0, 204=2000, 156=4000, 108=6000

cols_a, rows_a = extract_blue_curve(arr, row_min=30, row_max=270, col_min=95, col_max=542)

energy_a = pixel_to_data(cols_a, [(207, 530), (341, 540), (476, 550)])
intensity_a = pixel_to_data(rows_a, [(270, 0), (204, 2000), (156, 4000), (108, 6000)])
intensity_a = np.clip(intensity_a, 0, None)

sort_a = np.argsort(energy_a)
energy_a = energy_a[sort_a]
intensity_a = intensity_a[sort_a]
intensity_a_smooth = gaussian_filter1d(intensity_a, sigma=1.5)

# Panel (b) Ti L-edge calibration:
#   x-axis: col 115=450eV, 218=455eV, 325=460eV, 434=465eV, 537=470eV
#   y-axis: row 566=0, 503=1e4, 440=2e4, 380=3e4

cols_b, rows_b = extract_blue_curve(arr, row_min=315, row_max=566, col_min=109, col_max=542)

energy_b = pixel_to_data(cols_b, [(115, 450), (218, 455), (325, 460), (434, 465), (537, 470)])
intensity_b = pixel_to_data(rows_b, [(566, 0), (503, 10000), (440, 20000), (380, 30000)])
intensity_b = np.clip(intensity_b, 0, None)

sort_b = np.argsort(energy_b)
energy_b = energy_b[sort_b]
intensity_b = intensity_b[sort_b]
intensity_b_smooth = gaussian_filter1d(intensity_b, sigma=1.5)

calc_o = np.loadtxt("../reference_output/SrTiO3/O_Kedge/O_Kedge.dat")
calc_ti = np.loadtxt("../reference_output/SrTiO3/Ti_Ledge/Ti_Ledge.dat")


def find_first_peak(energy, intensity, search_frac=0.4):
    """Find the first major peak in the leading portion of a spectrum."""
    n = int(len(energy) * search_frac)
    peak_idx = np.argmax(intensity[:n])
    return energy[peak_idx]


expt_peak_o = find_first_peak(energy_a, intensity_a_smooth)
calc_peak_o = find_first_peak(calc_o[:, 0], calc_o[:, 1])
shift_o = expt_peak_o - calc_peak_o
print(f"O K-edge: expt 1st peak={expt_peak_o:.1f} eV, calc={calc_peak_o:.1f} eV → shift={shift_o:.1f} eV")

# Ti: our calc is edge='L2' (2p1/2 → 3d), so align calc peak with the expt L2 peak (~462-466 eV)
# Expt L3 peaks: t2g~457, eg~459; Expt L2 peaks: t2g~462, eg~465
calc_peak_ti = calc_ti[np.argmax(calc_ti[:, 1]), 0]
EXPT_TI_L2_EG = 465.1
shift_ti = EXPT_TI_L2_EG - calc_peak_ti
print(f"Ti L-edge: expt L2-eg={EXPT_TI_L2_EG:.1f} eV, calc peak={calc_peak_ti:.1f} eV → shift={shift_ti:.1f} eV")

np.savetxt("O_Kedge_expt.dat",
           np.column_stack([energy_a, intensity_a_smooth]),
           header="Energy(eV)  Intensity(a.u.) — digitized from Muller EELS, delta=0",
           fmt="%.2f  %.1f")
np.savetxt("Ti_Ledge_expt.dat",
           np.column_stack([energy_b, intensity_b_smooth]),
           header="Energy(eV)  Intensity(a.u.) — digitized from Muller EELS, delta=0",
           fmt="%.2f  %.1f")
print("Saved: O_Kedge_expt.dat, Ti_Ledge_expt.dat")


fig, axes = plt.subplots(2, 1, figsize=(10, 9), constrained_layout=True)

ax1 = axes[0]
ax1_exp = ax1
color_exp = "black"
color_calc = "#2060D0"

ax1_exp.plot(energy_a, intensity_a_smooth, color=color_exp, linewidth=1.5,
             label=f"Expt. EELS (Muller, $\\delta\\approx0$)")
ax1_exp.set_ylabel("Expt. Intensity (a.u.)", color=color_exp)
ax1_exp.tick_params(axis="y", labelcolor=color_exp)

ax1_calc = ax1.twinx()
ax1_calc.plot(calc_o[:, 0] + shift_o, calc_o[:, 1], color=color_calc, linewidth=1.5,
              label="Calc. XSpectra (initial-state, dipole)")
ax1_calc.set_ylabel("Calc. Absorption (arb. units)", color=color_calc)
ax1_calc.tick_params(axis="y", labelcolor=color_calc)

ax1.set_xlabel("Energy Loss (eV)")
ax1.set_xlim(525, 555)
ax1.set_title("SrTiO$_3$ — O K-edge")

lines1 = ax1_exp.get_legend_handles_labels()
lines2 = ax1_calc.get_legend_handles_labels()
ax1.legend(lines1[0] + lines2[0], lines1[1] + lines2[1],
           loc="upper right", frameon=False, fontsize=9)

ax2 = axes[1]
ax2_exp = ax2

ax2_exp.plot(energy_b, intensity_b_smooth, color=color_exp, linewidth=1.5,
             label=f"Expt. EELS (Muller, $\\delta\\approx0$)")
ax2_exp.set_ylabel("Expt. Intensity (a.u.)", color=color_exp)
ax2_exp.tick_params(axis="y", labelcolor=color_exp)

ax2_calc = ax2.twinx()
ax2_calc.plot(calc_ti[:, 0] + shift_ti, calc_ti[:, 1], color=color_calc, linewidth=1.5,
              label="Calc. XSpectra (initial-state, L$_2$ dipole)")
ax2_calc.set_ylabel("Calc. Absorption (arb. units)", color=color_calc)
ax2_calc.tick_params(axis="y", labelcolor=color_calc)

ax2.set_xlabel("Energy Loss (eV)")
ax2.set_xlim(450, 470)
ax2.set_title("SrTiO$_3$ — Ti L$_{2,3}$-edge")

lines1 = ax2_exp.get_legend_handles_labels()
lines2 = ax2_calc.get_legend_handles_labels()
ax2.legend(lines1[0] + lines2[0], lines1[1] + lines2[1],
           loc="upper right", frameon=False, fontsize=9)

fig.suptitle("SrTiO$_3$ — Calculated vs Experimental XANES/EELS",
             fontsize=14, fontweight="bold")

plt.savefig("SrTiO3_comparison.png", dpi=150, bbox_inches="tight")
print("Saved: SrTiO3_comparison.png")
plt.close()
