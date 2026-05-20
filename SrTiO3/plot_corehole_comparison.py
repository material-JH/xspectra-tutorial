#!/usr/bin/env python3
"""
Plot SrTiO3 XANES spectra comparison: no core-hole vs FCH vs HCH.
Two panels: O K-edge (top) and Ti L-edge (bottom).
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Load all spectra ---
# O K-edge
o_noch = np.loadtxt("../reference_output/SrTiO3/O_Kedge/O_Kedge.dat")
o_fch  = np.loadtxt("../reference_output/SrTiO3/O_Kedge_FCH/O_Kedge_FCH.dat")
o_hch  = np.loadtxt("../reference_output/SrTiO3/O_Kedge_HCH/O_Kedge_HCH.dat")

# Ti L-edge
ti_noch = np.loadtxt("../reference_output/SrTiO3/Ti_Ledge/Ti_Ledge.dat")
ti_fch  = np.loadtxt("../reference_output/SrTiO3/Ti_Ledge_FCH/Ti_Ledge_FCH.dat")
ti_hch  = np.loadtxt("../reference_output/SrTiO3/Ti_Ledge_HCH/Ti_Ledge_HCH.dat")

# --- Plot ---
fig, axes = plt.subplots(2, 1, figsize=(10, 9), constrained_layout=True)

colors = {"No CH": "#2166ac", "HCH": "#4dac26", "FCH": "#d6604d"}
lw = 1.8

# Panel (a): O K-edge
ax = axes[0]
ax.plot(o_noch[:, 0], o_noch[:, 1], color=colors["No CH"], lw=lw, label="No core-hole (initial state)")
ax.plot(o_hch[:, 0],  o_hch[:, 1],  color=colors["HCH"],  lw=lw, label="Half core-hole (HCH)", ls="--")
ax.plot(o_fch[:, 0],  o_fch[:, 1],  color=colors["FCH"],  lw=lw, label="Full core-hole (FCH)", ls="-.")
ax.set_xlabel("Energy (eV)", fontsize=12)
ax.set_ylabel("Absorption (arb. units)", fontsize=12)
ax.set_title("(a) O K-edge", fontsize=13, fontweight="bold", loc="left")
ax.set_xlim(-5, 35)
ax.axvline(0, color="gray", ls=":", alpha=0.5, lw=1)
ax.legend(frameon=True, fancybox=False, edgecolor="0.7", fontsize=10, loc="upper right")
ax.grid(True, alpha=0.2)

# Panel (b): Ti L-edge
ax = axes[1]
ax.plot(ti_noch[:, 0], ti_noch[:, 1], color=colors["No CH"], lw=lw, label="No core-hole (initial state)")
ax.plot(ti_hch[:, 0],  ti_hch[:, 1],  color=colors["HCH"],  lw=lw, label="Half core-hole (HCH)", ls="--")
ax.plot(ti_fch[:, 0],  ti_fch[:, 1],  color=colors["FCH"],  lw=lw, label="Full core-hole (FCH)", ls="-.")
ax.set_xlabel("Energy (eV)", fontsize=12)
ax.set_ylabel("Absorption (arb. units)", fontsize=12)
ax.set_title("(b) Ti L$_2$-edge", fontsize=13, fontweight="bold", loc="left")
ax.set_xlim(-5, 35)
ax.axvline(0, color="gray", ls=":", alpha=0.5, lw=1)
ax.legend(frameon=True, fancybox=False, edgecolor="0.7", fontsize=10, loc="upper right")
ax.grid(True, alpha=0.2)

fig.suptitle("SrTiO$_3$ — Core-Hole Effect on XANES Spectra", fontsize=15, fontweight="bold")
plt.savefig("SrTiO3_corehole_comparison.png", dpi=150, bbox_inches="tight")
print("Saved: SrTiO3_corehole_comparison.png")
plt.close()
