# XSpectra Pipeline

Every calculation follows the same three-step pipeline.

## Step 1: Extract the core wavefunction

```bash
$TOOLS_DIR/upf2plotcore.sh O.pbe-n-kjpaw_psl.0.1.UPF > O.wfc
```

This creates the initial core orbital used by XSpectra.

Important: for FCH/HCH calculations, still extract `filecore` from the original non-core-hole pseudopotential.

## Step 2: Run SCF with `pw.x`

```bash
pw.x < scf.in > scf.out
```

The SCF calculation creates the charge density and wavefunction data in `outdir`.

## Step 3: Run `xspectra.x`

```bash
xspectra.x < xspectra.in > xspectra.out
```

The output spectrum is written as `xanes.dat`, which the scripts rename to a descriptive filename.

## Key XSpectra variables

- `calculation='xanes_dipole'`: electric dipole transitions.
- `edge='K'`, `edge='L2'`, or `edge='L3'`: selected edge.
- `xepsilon(1:3)`: polarization direction.
- `xiabs`: absorbing species index.
- `filecore`: extracted core wavefunction file.
- `xgamma`: Lorentzian broadening in eV.
- `xemin`, `xemax`: plotted energy window.
- `cut_occ_states`: removes occupied-state artifacts below the edge.
- `xonly_plot`: replots from a saved Lanczos file without rerunning the expensive part.

## Flow diagram

```text
UPF pseudopotential
   │
   ├── upf2plotcore.sh → O.wfc / Ti.wfc / C.wfc
   │
SCF input → pw.x → charge density in tmp/
   │
XSpectra input + core wavefunction → xspectra.x → xanes.dat
```
