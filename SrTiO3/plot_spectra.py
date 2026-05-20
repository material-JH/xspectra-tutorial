#!/usr/bin/env python3
"""Plot SrTiO3 O K-edge and Ti L-edge XANES spectra."""

import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 1, figsize=(8, 8), constrained_layout=True)

data_o = np.loadtxt("../reference_output/SrTiO3/O_Kedge/O_Kedge.dat")
ax = axes[0]
ax.plot(data_o[:, 0], data_o[:, 1], "b-", linewidth=1.5)
ax.set_xlabel("Energy (eV)")
ax.set_ylabel("Absorption (arb. units)")
ax.set_title("SrTiO3 — O K-edge (dipole, initial-state)")
ax.set_xlim(-5, 35)
ax.axvline(0, color="gray", linestyle="--", alpha=0.5, label="Fermi level")
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)

data_ti = np.loadtxt("../reference_output/SrTiO3/Ti_Ledge/Ti_Ledge.dat")
ax = axes[1]
ax.plot(data_ti[:, 0], data_ti[:, 1], "r-", linewidth=1.5)
ax.set_xlabel("Energy (eV)")
ax.set_ylabel("Absorption (arb. units)")
ax.set_title("SrTiO3 — Ti L-edge (L$_2$, dipole, initial-state)")
ax.set_xlim(-5, 35)
ax.axvline(0, color="gray", linestyle="--", alpha=0.5, label="Fermi level")
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)

fig.suptitle("SrTiO3 Cubic Perovskite — XANES Spectra", fontsize=14, fontweight="bold")
plt.savefig("SrTiO3_spectra.png", dpi=150, bbox_inches="tight")
print("Saved: SrTiO3_spectra.png")
plt.close()
