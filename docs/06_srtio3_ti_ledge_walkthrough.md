# SrTiO3 Ti L-edge Walkthrough

The Ti L-edge probes transitions from Ti 2p core states to Ti 3d-like unoccupied states. This is familiar to TEM/EELS users because Ti L2,3 white-line shape and splitting are sensitive to valence and crystal field.

## Run

```bash
cd SrTiO3/Ti_Ledge
bash run.sh
cd ../..
```

On a cluster, prefer:

```bash
sbatch scheduler/slurm_srtio3_tiledge.sbatch
```

## Important input choices

The Ti absorber is labeled `Tih`:

```fortran
ATOMIC_SPECIES
Sr   ...
Tih  ...   ! absorber
O    ...
```

Therefore:

```fortran
ntyp = 3
xiabs = 2
edge = 'L2'
```

## Interpretation cautions

- Experimental EELS usually shows both L3 and L2 edges.
- This example uses `edge='L2'`; treat it as a tutorial calculation, not a complete quantitative L2,3 simulation.
- Compare qualitative peak positions and relative shapes after energy alignment.
