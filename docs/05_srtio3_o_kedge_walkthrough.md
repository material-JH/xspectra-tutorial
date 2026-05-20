# SrTiO3 O K-edge Walkthrough

The O K-edge probes transitions from O 1s to unoccupied O 2p-projected states. In SrTiO3, those O 2p states hybridize strongly with Ti 3d states, so the edge is sensitive to Ti-O bonding and octahedral electronic structure.

## Run

```bash
cd SrTiO3/O_Kedge
bash run.sh
cd ../..
```

On a cluster, prefer:

```bash
sbatch scheduler/slurm_srtio3_okedge.sbatch
```

## Important input choices

In the SCF input, one oxygen is labeled `Oh`:

```fortran
ATOMIC_SPECIES
Sr  ...
Ti  ...
Oh  ...   ! absorber
O   ...   ! spectator oxygens
```

Therefore:

```fortran
ntyp = 4
xiabs = 3
```

## TEM/EELS interpretation

- O K-edge: O 1s to O 2p-like unoccupied states.
- In SrTiO3, early O K-edge features reflect hybridization with Ti t2g/eg-like conduction states.
- Calculated spectra use a relative energy axis and must be aligned before comparison to experimental energy loss.
- Broadening is chosen by `xgamma`; it is not a full instrument-response model.

## Output

```text
SrTiO3/O_Kedge/O_Kedge.dat
```

Plot with:

```bash
cd SrTiO3
python3 plot_spectra.py
```
