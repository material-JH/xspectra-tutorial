#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

if [ ! -f "$PROJECT_ROOT/env.sh" ]; then
    echo "FAIL env.sh: missing"
    echo "  Fix: cp env.sh.example env.sh && edit env.sh for your cluster"
    exit 1
fi

# shellcheck source=/dev/null
source "$PROJECT_ROOT/env.sh"

failures=0
pass() { echo "PASS $1"; }
fail() { echo "FAIL $1"; failures=$((failures + 1)); }
check_file() {
    local label="$1"
    local path="$2"
    if [ -f "$path" ]; then
        pass "$label: $path"
    else
        fail "$label: missing at $path"
    fi
}
check_exec() {
    local label="$1"
    local path="$2"
    if [ -x "$path" ]; then
        pass "$label: $path"
    elif [ -f "$path" ]; then
        fail "$label: found but not executable: $path"
    else
        fail "$label: missing at $path"
    fi
}

: "${BIN_DIR:=}"
: "${TOOLS_DIR:=}"
: "${EXAMPLE_PSEUDO_DIR:=}"
: "${NPROCS:=4}"
: "${MPI_RUN:=mpirun -np $NPROCS}"

check_exec "pw.x" "$BIN_DIR/pw.x"
check_exec "xspectra.x" "$BIN_DIR/xspectra.x"
check_exec "ld1.x" "$BIN_DIR/ld1.x"
check_exec "upf2plotcore.sh" "$TOOLS_DIR/upf2plotcore.sh"

check_file "example C pseudo" "$EXAMPLE_PSEUDO_DIR/C_PBE_TM_2pj.UPF"
check_file "example core-hole C pseudo" "$EXAMPLE_PSEUDO_DIR/Ch_PBE_TM_2pj.UPF"
check_file "SrTiO3 Sr pseudo" "$PROJECT_ROOT/SrTiO3/pseudo/Sr.pbe-spn-kjpaw_psl.1.0.0.UPF"
check_file "SrTiO3 Ti pseudo" "$PROJECT_ROOT/SrTiO3/pseudo/Ti.pbe-spn-kjpaw_psl.1.0.0.UPF"
check_file "SrTiO3 O pseudo" "$PROJECT_ROOT/SrTiO3/pseudo/O.pbe-n-kjpaw_psl.0.1.UPF"

if python3 - <<'PY' >/dev/null 2>&1
import numpy, matplotlib, scipy
from PIL import Image
PY
then
    pass "python packages: numpy matplotlib scipy Pillow"
else
    fail "python packages: install with 'python3 -m pip install -r requirements.txt' or load a Python module"
fi

if mkdir -p "$PROJECT_ROOT/.setup_check_tmp" && touch "$PROJECT_ROOT/.setup_check_tmp/write-test"; then
    pass "working directory is writable"
    rm -rf "$PROJECT_ROOT/.setup_check_tmp"
else
    fail "working directory is not writable"
fi

if [ -n "${SLURM_JOB_ID:-}" ]; then
    pass "scheduler context: Slurm job $SLURM_JOB_ID"
elif [ -n "${PBS_JOBID:-}" ]; then
    pass "scheduler context: PBS job $PBS_JOBID"
else
    echo "INFO scheduler context: no job allocation detected"
    echo "  This setup check is lightweight, but run QE calculations through the scheduler."
fi

MPI_LAUNCHER_CMD="${MPI_RUN%% *}"
if command -v "$MPI_LAUNCHER_CMD" >/dev/null 2>&1; then
    pass "MPI launcher command found: $MPI_LAUNCHER_CMD"
else
    fail "MPI launcher command not found: $MPI_LAUNCHER_CMD"
fi

if [ "$failures" -eq 0 ]; then
    echo ""
    echo "Setup check passed. You can submit the tutorial jobs."
else
    echo ""
    echo "Setup check found $failures problem(s). Fix them before the tutorial."
    exit 1
fi
