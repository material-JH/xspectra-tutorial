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
BUNDLED_DIAMOND_PSEUDO_DIR="$PROJECT_ROOT/diamond/pseudo"
if [ -z "$EXAMPLE_PSEUDO_DIR" ] && [ -f "$BUNDLED_DIAMOND_PSEUDO_DIR/C_PBE_TM_2pj.UPF" ]; then
    EXAMPLE_PSEUDO_DIR="$BUNDLED_DIAMOND_PSEUDO_DIR"
fi
: "${NPROCS:=4}"
: "${MPI_RUN:=mpirun -np $NPROCS}"
: "${PW_BIN:=${BIN_DIR:+$BIN_DIR/pw.x}}"
: "${XSPECTRA_BIN:=${BIN_DIR:+$BIN_DIR/xspectra.x}}"
: "${LD1_BIN:=${BIN_DIR:+$BIN_DIR/ld1.x}}"

if [ -z "$BIN_DIR" ]; then
    fail "BIN_DIR: not set"
    echo "  Fix: edit env.sh, load the QE module, then run 'command -v pw.x' to find the path."
fi

if [ -n "$PW_BIN" ]; then
    check_exec "pw.x" "$PW_BIN"
else
    fail "pw.x path: not set"
fi

if [ -n "$XSPECTRA_BIN" ]; then
    check_exec "xspectra.x" "$XSPECTRA_BIN"
else
    fail "xspectra.x path: not set"
fi

if [ -n "$LD1_BIN" ]; then
    check_exec "ld1.x" "$LD1_BIN"
else
    fail "ld1.x path: not set"
fi

if [ -n "$TOOLS_DIR" ]; then
    check_exec "upf2plotcore.sh" "$TOOLS_DIR/upf2plotcore.sh"
else
    fail "TOOLS_DIR: not set"
    echo "  Fix: download QEF/q-e for XSpectra/tools or ask the instructor for TOOLS_DIR, then set TOOLS_DIR in env.sh."
fi

if [ -n "$EXAMPLE_PSEUDO_DIR" ]; then
    check_file "Diamond C pseudo" "$EXAMPLE_PSEUDO_DIR/C_PBE_TM_2pj.UPF"
    check_file "Diamond core-hole C pseudo" "$EXAMPLE_PSEUDO_DIR/Ch_PBE_TM_2pj.UPF"
else
    fail "EXAMPLE_PSEUDO_DIR: not set"
    echo "  Fix: use the bundled diamond/pseudo directory, download QEF/q-e, or ask the instructor for the XSpectra example pseudo directory."
fi
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
