#!/usr/bin/env bash
#SBATCH --job-name=xspectra-sto-til
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=00:30:00
#SBATCH --output=slurm-%x-%j.out

set -euo pipefail

cd "$SLURM_SUBMIT_DIR"
source ./env.sh

export NPROCS="${SLURM_NTASKS:-${NPROCS:-4}}"
export MPI_RUN="${MPI_RUN:-srun -n $NPROCS}"

cd SrTiO3/Ti_Ledge
bash run.sh
