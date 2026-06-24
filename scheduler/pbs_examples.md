# PBS/Torque Examples

This tutorial environment uses PBS/Torque. Ready-to-submit templates are:

```bash
cd /scratch/$USER/xspectra-tutorial
qsub scheduler/pbs_diamond.pbs
qsub scheduler/pbs_srtio3_okedge.pbs
qstat -u "$USER"
```

On systems that reject jobs from home directories, clone or copy this tutorial
under `/scratch/$USER` before running `qsub`. Submit from the scratch copy, not
from `$HOME`, because the PBS job starts in `PBS_O_WORKDIR`.

Do not run `bash run_all_examples.sh` directly on the login node. The script now
stops outside PBS/Slurm unless an instructor explicitly sets
`XSPECTRA_ALLOW_LOGIN_RUN=1`.

The Diamond template is:

```bash
#!/usr/bin/env bash
#PBS -N xspectra-diamond
#PBS -A qe
#PBS -q gachon
#PBS -l select=1:ncpus=16:mpiprocs=16
#PBS -l walltime=00:30:00
#PBS -j oe

set -euo pipefail

cd "$PBS_O_WORKDIR"
export XSPECTRA_CRAY_TARGET_MODULE=craype-mic-knl
source ./env.sh

# The gachon account runs on KNL nodes. Use 16 MPI ranks for the tutorial
# calculation while loading the matching mic-knl QE build above.
export NPROCS=16
export MPI_RUN="mpirun -np $NPROCS"

bash run_all_examples.sh diamond-only
```

Submit with:

```bash
cd /scratch/$USER/xspectra-tutorial
qsub scheduler/pbs_diamond.pbs
qstat -u "$USER"
```

After the PBS job finishes, make plots as a separate post-processing step:

```bash
cd /scratch/$USER/xspectra-tutorial
python3 plot_spectra.py
ls xanes_spectra.png
```

`plot_spectra.py` uses the generated Diamond files in `diamond/` when they are
present:

```text
diamond/diamond.xspectra.dat
diamond/diamond.xspectra_replot.dat
diamond/diamondh.xspectra.dat
```

If those files are not present yet, it falls back to `reference_output/diamond/`.
The figure is written as `xanes_spectra.png` in the repository root. Keeping
plotting outside the PBS calculation job avoids failing a completed QE/XSpectra
job because a compute-node Python or matplotlib library is different from the
login-node environment.
