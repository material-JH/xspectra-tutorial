# Supercell and MPI Notes

## Why use a supercell?

With periodic boundary conditions, a core hole repeats in every unit cell. A supercell increases the distance between core-hole images and reduces artificial interaction.

For SrTiO3:

- unit cell: 5 atoms.
- 2x2x2 supercell: 40 atoms.
- one absorber uses the HCH pseudopotential.
- all other atoms use standard pseudopotentials.
- `tot_charge=+0.5` stays the same for one half core hole.

## MPI and k-point pools

XSpectra benefits strongly from k-point pool parallelization:

```bash
xspectra.x -nk N
```

For the 2x2x2 SrTiO3 supercell examples, use a small number of k-point pools such as:

```bash
-nk 4
```

The supercell SCF examples use:

```bash
-nd 1
```

to avoid ScaLAPACK diagonalization failures observed for this tutorial system.

## Cluster recommendation

Run supercell jobs only through the scheduler. Example:

```bash
sbatch scheduler/slurm_srtio3_okedge.sbatch
```

Adjust wall time and partition based on the instructor's cluster.
