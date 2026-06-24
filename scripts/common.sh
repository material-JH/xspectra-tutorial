#!/usr/bin/env bash
# Shared helpers for the XSpectra tutorial scripts. Source this file; do not run it.

load_xspectra_env() {
    local project_root="$1"

    if [ -f "$project_root/env.sh" ]; then
        # shellcheck source=/dev/null
        source "$project_root/env.sh"
    else
        cat >&2 <<EOF
ERROR: env.sh not found in $project_root

Create it from the template and edit it for your cluster:
  cp env.sh.example env.sh
  vim env.sh

At minimum, load the QE module in env.sh so that 'command -v pw.x' works.
Diamond pseudopotentials are bundled in diamond/pseudo/. If your cluster does
not provide XSpectra/tools/upf2plotcore.sh, download QEF/q-e or ask the
instructor for TOOLS_DIR.
EOF
        exit 1
    fi

    : "${BIN_DIR:?BIN_DIR is not set. Edit env.sh.}"
    : "${TOOLS_DIR:?TOOLS_DIR is not set. Edit env.sh.}"
    : "${NPROCS:=4}"
    : "${MPI_RUN:=mpirun -np $NPROCS}"

    PW_BIN="${PW_BIN:-$BIN_DIR/pw.x}"
    XSPECTRA_BIN="${XSPECTRA_BIN:-$BIN_DIR/xspectra.x}"
    LD1_BIN="${LD1_BIN:-$BIN_DIR/ld1.x}"
}

set_qe_commands() {
    local k_pools="${1:-$NPROCS}"
    local ndiag="${2:-}"

    if [ "${NPROCS:-1}" -le 1 ]; then
        PW_CMD="$PW_BIN"
        XS_CMD="$XSPECTRA_BIN"
    else
        PW_CMD="$MPI_RUN $PW_BIN -nk $k_pools"
        if [ -n "$ndiag" ]; then
            PW_CMD="$PW_CMD -nd $ndiag"
        fi
        XS_CMD="$MPI_RUN $XSPECTRA_BIN -nk $k_pools"
    fi
}

require_file() {
    local path="$1"
    local label="${2:-required file}"
    if [ ! -f "$path" ]; then
        echo "ERROR: Missing $label: $path" >&2
        exit 1
    fi
}

extract_core_if_missing() {
    local output_wfc="$1"
    local pseudo_file="$2"
    local label="${3:-core}"

    require_file "$pseudo_file" "$label pseudopotential"
    require_file "$TOOLS_DIR/upf2plotcore.sh" "upf2plotcore.sh"

    if [ ! -f "$output_wfc" ]; then
        echo "  Extracting $label core wavefunction -> $output_wfc"
        "$TOOLS_DIR/upf2plotcore.sh" "$pseudo_file" > "$output_wfc"
    else
        echo "  Reusing existing $output_wfc"
    fi
}

move_xanes_or_fail() {
    local destination="$1"
    local output_file="${2:-xspectra.out}"

    if [ ! -f xanes.dat ]; then
        echo "ERROR: xspectra.x did not produce xanes.dat" >&2
        echo "Check $output_file. Last 40 lines:" >&2
        tail -40 "$output_file" >&2 || true
        exit 1
    fi
    mv xanes.dat "$destination"
}

require_scheduler_for_calculation() {
    local work_dir="${1:-$(pwd)}"

    if [ -n "${SLURM_JOB_ID:-}" ] || [ -n "${PBS_JOBID:-}" ]; then
        return
    fi

    if [ "${XSPECTRA_ALLOW_LOGIN_RUN:-0}" = "1" ]; then
        print_cluster_warning
        return
    fi

    cat >&2 <<EOF
ERROR: QE/XSpectra calculation was started outside a scheduler job.

This tutorial is meant for batch execution on a compute node, not for direct
MPI execution on a login node. Beginners should run it from scratch with qsub:

  cd /scratch/\$USER/xspectra-tutorial
  cp env.sh.example env.sh        # only once
  ./check_setup.sh
  qsub scheduler/pbs_diamond.pbs
  qstat -u "\$USER"

Current directory:
  $work_dir

Do not run 'bash run_all_examples.sh' directly on the login node.
If an instructor intentionally gave you an interactive compute allocation, set:
  XSPECTRA_ALLOW_LOGIN_RUN=1
EOF
    exit 1
}

print_cluster_warning() {
    if [ -z "${SLURM_JOB_ID:-}" ] && [ -z "${PBS_JOBID:-}" ] && [ "${NPROCS:-1}" -gt 8 ]; then
        cat >&2 <<EOF
WARNING: NPROCS=$NPROCS and no scheduler job ID was detected.
On a supercomputer, do not run large MPI jobs on the login node.
Use qsub/sbatch or start an interactive allocation first.
EOF
    fi
}
