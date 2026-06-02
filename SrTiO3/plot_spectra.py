#!/usr/bin/env python3
"""Plot SrTiO3 O K-edge XANES spectra."""

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(8, 4.8), constrained_layout=True)

data_o = np.loadtxt("../reference_output/SrTiO3/O_Kedge/O_Kedge.dat")
ax.plot(data_o[:, 0], data_o[:, 1], "b-", linewidth=1.5)
ax.set_xlabel("Energy (eV)")
ax.set_ylabel("Absorption (arb. units)")
ax.set_title("SrTiO3 — O K-edge (dipole, initial-state)")
ax.set_xlim(-5, 35)
ax.axvline(0, color="gray", linestyle="--", alpha=0.5, label="Fermi level")
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)

fig.suptitle("SrTiO3 Cubic Perovskite — O K-edge XANES", fontsize=14, fontweight="bold")
plt.savefig("SrTiO3_spectra.png", dpi=150, bbox_inches="tight")
print("Saved: SrTiO3_spectra.png")
plt.close()
