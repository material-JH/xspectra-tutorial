#!/bin/bash
set -euo pipefail

# =============================================================================
# XSpectra Examples - Master Run Script
# Runs the bundled XSpectra examples using paths from env.sh.
# =============================================================================

WORK_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$WORK_DIR"
source "$PROJECT_ROOT/scripts/common.sh"
load_xspectra_env "$PROJECT_ROOT"
BUNDLED_DIAMOND_PSEUDO_DIR="$PROJECT_ROOT/diamond/pseudo"
PSEUDO_DIR="${EXAMPLE_PSEUDO_DIR:-}"
if [ -z "$PSEUDO_DIR" ] && [ -f "$BUNDLED_DIAMOND_PSEUDO_DIR/C_PBE_TM_2pj.UPF" ]; then
    PSEUDO_DIR="$BUNDLED_DIAMOND_PSEUDO_DIR"
fi
if [ -z "$PSEUDO_DIR" ] || [ ! -f "$PSEUDO_DIR/C_PBE_TM_2pj.UPF" ] || [ ! -f "$PSEUDO_DIR/Ch_PBE_TM_2pj.UPF" ]; then
    cat >&2 <<EOF
ERROR: Diamond pseudopotentials were not found.

Expected these files in EXAMPLE_PSEUDO_DIR or diamond/pseudo/:
  C_PBE_TM_2pj.UPF
  Ch_PBE_TM_2pj.UPF

Fix options:
  1. Use the bundled repo copy: export EXAMPLE_PSEUDO_DIR="$BUNDLED_DIAMOND_PSEUDO_DIR"
  2. Download QE source: git clone --depth 1 --branch develop https://github.com/QEF/q-e.git ~/q-e
     then set: export EXAMPLE_PSEUDO_DIR="$HOME/q-e/XSpectra/examples/pseudo"
EOF
    exit 1
fi
PSEUDO_DIR="$(cd "$PSEUDO_DIR" && pwd)"
set_qe_commands "${KPOOLS:-$NPROCS}"
PW_COMMAND="$PW_CMD"
X_COMMAND="$XS_CMD"

cd "$WORK_DIR"
print_cluster_warning

echo "============================================"
echo "  XSpectra Tutorial - Curated Examples"
echo "============================================"
echo "  BIN_DIR:    $BIN_DIR"
echo "  PSEUDO_DIR: $PSEUDO_DIR"
echo "  WORK_DIR:   $WORK_DIR"
echo ""

# #############################################################################
# EXAMPLE 1: DIAMOND (Carbon K-edge)
# #############################################################################
echo ""
echo "============================================"
echo "  EXAMPLE 1: DIAMOND (Carbon K-edge)"
echo "============================================"

mkdir -p diamond/tmp
cd diamond

# Extract core wavefunction
echo "  Extracting core wavefunction from C pseudo..."
$TOOLS_DIR/upf2plotcore.sh $PSEUDO_DIR/C_PBE_TM_2pj.UPF > C.wfc
echo "  done"

# --- 1a: SCF without core hole ---
echo ""
echo "  --- Step 1a: SCF (no core hole) ---"
cat > diamond.scf.in << EOF
 &control
    calculation='scf',
    pseudo_dir = '$PSEUDO_DIR/',
    outdir='./tmp/',
    prefix='diamond',
 /
 &system
    ibrav = 1,
    celldm(1) = 6.740256,
    nat=8,
    ntyp=2,
    nbnd=16,
    ecutwfc=40.0,
 /
 &electrons
    mixing_beta = 0.3,
 /
ATOMIC_SPECIES
C_h 12.0 C_PBE_TM_2pj.UPF
C 12.0 C_PBE_TM_2pj.UPF
ATOMIC_POSITIONS crystal
C_h 0.0 0.0 0.0
C 0.0 0.5 0.5
C 0.5 0.0 0.5
C 0.5 0.5 0.0
C 0.75 0.75 0.25
C 0.75 0.25 0.75
C 0.25 0.75 0.75
C 0.25 0.25 0.25
K_POINTS automatic
4 4 4 0 0 0
EOF

echo "  Running pw.x for diamond (no core hole)..."
$PW_COMMAND < diamond.scf.in > diamond.scf.out 2>&1
echo "  pw.x done (exit: $?)"

# --- 1b: XSpectra (including occupied states) ---
echo ""
echo "  --- Step 1b: XSpectra (dipole, including occupied) ---"
cat > diamond.xspectra.in << EOF
 &input_xspectra
    calculation='xanes_dipole',
    prefix='diamond',
    outdir='./tmp/',
    xniter=1000,
    xcheck_conv=50,
    xepsilon(1)=1.0,
    xepsilon(2)=0.0,
    xepsilon(3)=0.0,
    xiabs=1,
    x_save_file='diamond.xspectra.sav',
    xerror=0.001,
 /
 &plot
    xnepoint=300,
    xgamma=0.8,
    xemin=-10.0,
    xemax=30.0,
    terminator=.true.,
    cut_occ_states=.false.,
 /
 &pseudos
    filecore='C.wfc',
    r_paw(1)=3.2,
 /
 &cut_occ
 /
4 4 4 1 1 1
EOF

echo "  Running xspectra.x (dipole, no occ cut)..."
$X_COMMAND < diamond.xspectra.in > diamond.xspectra.out 2>&1
echo "  xspectra.x done (exit: $?)"
move_xanes_or_fail diamond.xspectra.dat

# --- 1c: XSpectra replot (cutting occupied states) ---
echo ""
echo "  --- Step 1c: XSpectra replot (cutting occupied) ---"
cat > diamond.xspectra_replot.in << EOF
 &input_xspectra
    calculation='xanes_dipole',
    prefix='diamond',
    outdir='./tmp/',
    xonly_plot=.true.,
    xniter=1000,
    xcheck_conv=50,
    xepsilon(1)=1.0,
    xepsilon(2)=0.0,
    xepsilon(3)=0.0,
    xiabs=1,
    x_save_file='diamond.xspectra.sav',
    xerror=0.001,
 /
 &plot
    xnepoint=1000,
    xgamma=0.8,
    xemin=-10.0,
    xemax=30.0,
    terminator=.true.,
    cut_occ_states=.true.,
 /
 &pseudos
    filecore='C.wfc',
    r_paw(1)=3.2,
 /
 &cut_occ
    cut_desmooth=0.1,
    cut_stepl=0.01,
 /
4 4 4 1 1 1
EOF

echo "  Running xspectra.x (replot with occ cut)..."
$X_COMMAND < diamond.xspectra_replot.in > diamond.xspectra_replot.out 2>&1
echo "  xspectra.x done (exit: $?)"
move_xanes_or_fail diamond.xspectra_replot.dat

# --- 1d: SCF with core hole ---
echo ""
echo "  --- Step 1d: SCF (with core hole) ---"
rm -rf ./tmp/*

cat > diamondh.scf.in << EOF
 &control
    calculation='scf',
    pseudo_dir = '$PSEUDO_DIR/',
    outdir='./tmp/',
    prefix='diamondh',
 /
 &system
    ibrav = 1,
    celldm(1) = 6.740256,
    nat=8,
    ntyp=2,
    nbnd=16,
    tot_charge=+1.0,
    ecutwfc=40.0,
 /
 &electrons
    mixing_beta = 0.3,
 /
ATOMIC_SPECIES
C_h 12.0 Ch_PBE_TM_2pj.UPF
C 12.0 C_PBE_TM_2pj.UPF
ATOMIC_POSITIONS crystal
C_h 0.0 0.0 0.0
C 0.0 0.5 0.5
C 0.5 0.0 0.5
C 0.5 0.5 0.0
C 0.75 0.75 0.25
C 0.75 0.25 0.75
C 0.25 0.75 0.75
C 0.25 0.25 0.25
K_POINTS automatic
4 4 4 0 0 0
EOF

echo "  Running pw.x for diamond (with core hole)..."
$PW_COMMAND < diamondh.scf.in > diamondh.scf.out 2>&1
echo "  pw.x done (exit: $?)"

# --- 1e: XSpectra with core hole ---
echo ""
echo "  --- Step 1e: XSpectra (with core hole, occ cut) ---"
cat > diamondh.xspectra.in << EOF
 &input_xspectra
    calculation='xanes_dipole',
    prefix='diamondh',
    outdir='./tmp/',
    xonly_plot=.false.,
    xniter=1000,
    xcheck_conv=10,
    xepsilon(1)=1.0,
    xepsilon(2)=0.0,
    xepsilon(3)=0.0,
    xiabs=1,
    x_save_file='diamondh.xspectra.sav',
    xerror=0.001,
 /
 &plot
    xnepoint=1000,
    xgamma=0.8,
    xemin=-10.0,
    xemax=30.0,
    terminator=.true.,
    cut_occ_states=.true.,
 /
 &pseudos
    filecore='C.wfc',
    r_paw(1)=3.2,
 /
 &cut_occ
    cut_desmooth=0.1,
    cut_stepl=0.01,
 /
4 4 4 1 1 1
EOF

echo "  Running xspectra.x (core hole)..."
$X_COMMAND < diamondh.xspectra.in > diamondh.xspectra.out 2>&1
echo "  xspectra.x done (exit: $?)"
move_xanes_or_fail diamondh.xspectra.dat
rm -rf ./tmp/*

echo ""
echo "  DIAMOND example COMPLETE."
echo "  Output files: diamond.xspectra.dat, diamond.xspectra_replot.dat, diamondh.xspectra.dat"
cd "$WORK_DIR"

if [ "${1:-all}" = "diamond-only" ]; then
    echo ""
    echo "  diamond-only mode requested; stopping after Diamond."
    exit 0
fi


# #############################################################################
# OPTIONAL INCLUDED SrTiO3 EXAMPLES
# #############################################################################
MODE="${1:-all}"

run_srtio3_okedge() {
    echo ""
    echo "============================================"
    echo "  SrTiO3 O K-edge"
    echo "============================================"
    bash "$WORK_DIR/SrTiO3/O_Kedge/run.sh"
    bash "$WORK_DIR/SrTiO3/O_Kedge_FCH/run.sh"
    bash "$WORK_DIR/SrTiO3/O_Kedge_HCH/run.sh"
}

run_srtio3_okedge_super() {
    echo ""
    echo "============================================"
    echo "  SrTiO3 O K-edge HCH supercell"
    echo "============================================"
    bash "$WORK_DIR/SrTiO3/O_Kedge_HCH_super/run.sh"
}

case "$MODE" in
    all)
        run_srtio3_okedge
        ;;
    srtio3)
        run_srtio3_okedge
        ;;
    srtio3-okedge)
        run_srtio3_okedge
        ;;
    srtio3-okedge-super)
        run_srtio3_okedge_super
        ;;
    diamond-only)
        # Already handled above.
        ;;
    *)
        echo "Unknown mode: $MODE" >&2
        echo "Usage: bash run_all_examples.sh [all|diamond-only|srtio3|srtio3-okedge|srtio3-okedge-super]" >&2
        exit 2
        ;;
esac

echo ""
echo "============================================"
echo "  Selected tutorial examples complete"
echo "============================================"
echo "Next plotting commands:"
echo "  python3 plot_spectra.py"
echo "  cd SrTiO3 && python3 plot_spectra.py"
