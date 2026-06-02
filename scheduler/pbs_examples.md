# PBS/Torque Examples

This tutorial environment uses PBS/Torque. Ready-to-submit templates are:

```bash
cd /scratch/$USER/xspectra-tutorial
qsub scheduler/pbs_diamond.pbs
qsub scheduler/pbs_srtio3_okedge.pbs
qsub scheduler/pbs_srtio3_tiledge.pbs
qstat -u "$USER"
```

On systems that reject jobs from home directories, clone or copy this tutorial
under `/scratch/$USER` before running `qsub`. The PBS templates use the
`norm_skl` queue and run 4 MPI ranks with `mpirun -np 4`, matching the QE module
stack used in this tutorial environment.

The Diamond template is:

```bash
#!/usr/bin/env bash
#PBS -N xspectra-diamond
#PBS -A qe
#PBS -q norm_skl
#PBS -l select=1:ncpus=4:mpiprocs=4
#PBS -l walltime=00:30:00
#PBS -j oe

set -euo pipefail
cd "$PBS_O_WORKDIR"
source ./env.sh

export NPROCS=4
export MPI_RUN="mpirun -np $NPROCS"

bash run_all_examples.sh diamond-only
```

Submit with:

```bash
cd /scratch/$USER/xspectra-tutorial
qsub job.pbs
qstat -u "$USER"
```

After the PBS job finishes, make plots as a separate post-processing step:

```bash
python3 plot_spectra.py
```

Keeping plotting outside the PBS calculation job avoids failing a completed QE/XSpectra job because a compute-node Python or matplotlib library is different from the login-node environment.
