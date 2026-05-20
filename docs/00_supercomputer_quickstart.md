# Supercomputer Quickstart

This tutorial is designed for a shared supercomputer. The exact module names and queues differ by site, so use the commands supplied by the instructor when they differ from the examples below.

## 1. Log in

```bash
ssh username@cluster.example.edu
```

## 2. Get the tutorial files

```bash
git clone https://github.com/material-JH/xspectra-tutorial.git
cd xspectra-tutorial
```

If the instructor provides a shared copy, use that path instead.

## 3. Configure the environment

```bash
cp env.sh.example env.sh
vim env.sh
```

Typical cluster setup in `env.sh`:

```bash
module purge
module load quantum-espresso
module load openmpi
module load python
export QE_ROOT=/path/to/q-e
export BIN_DIR=$QE_ROOT/bin
export TOOLS_DIR=$QE_ROOT/XSpectra/tools
export EXAMPLE_PSEUDO_DIR=$QE_ROOT/XSpectra/examples/pseudo
export NPROCS=4
export MPI_RUN="srun -n $NPROCS"      # inside Slurm jobs
```

If your site uses `mpirun`, use:

```bash
export MPI_RUN="mpirun -np $NPROCS"
```

## 4. Run the setup check

```bash
bash check_setup.sh
```

The setup check is lightweight and safe on the login node. It does not run a QE calculation.

## 5. Submit a job

For Slurm:

```bash
sbatch scheduler/slurm_diamond.sbatch
squeue -u "$USER"
```

Cancel a job if needed:

```bash
scancel <jobid>
```

For PBS/Torque, see `scheduler/pbs_examples.md`.

## 6. Login node vs compute node

Do not run expensive MPI calculations directly on the login node. Use one of:

- `sbatch` for batch jobs.
- `salloc` + `srun` for interactive Slurm sessions.
- `qsub` for PBS/Torque jobs.

Small file editing, plotting, `git`, and `bash check_setup.sh` are usually fine on login nodes.

## 7. Where outputs go

Each calculation directory writes:

- `scf.in`, `scf.out` from `pw.x`.
- `xspectra.in`, `xspectra.out` from `xspectra.x`.
- `*.wfc` core wavefunction extracted from the pseudopotential.
- `*.dat` final spectrum.
- `tmp/` QE scratch files.

If a job fails, start with:

```bash
tail -80 scf.out
tail -80 xspectra.out
```
