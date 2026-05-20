# PBS/Torque Examples

If your cluster uses PBS/Torque instead of Slurm, adapt this template.

```bash
#!/usr/bin/env bash
#PBS -N xspectra-diamond
#PBS -l select=1:ncpus=4:mpiprocs=4
#PBS -l walltime=00:30:00
#PBS -j oe

set -euo pipefail
cd "$PBS_O_WORKDIR"
source ./env.sh

export NPROCS="${PBS_NP:-4}"
export MPI_RUN="mpirun -np $NPROCS"

bash run_all_examples.sh diamond-only
python3 plot_spectra.py
```

Submit with:

```bash
qsub job.pbs
qstat -u "$USER"
```
