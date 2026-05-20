#!/bin/bash
set -euo pipefail

WORK_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$WORK_DIR/../.." && pwd)"
source "$PROJECT_ROOT/scripts/common.sh"
load_xspectra_env "$PROJECT_ROOT"
PSEUDO_DIR="${SRTIO3_PSEUDO_DIR:-$WORK_DIR/../pseudo}"
KPOOLS="${KPOOLS:-$NPROCS}"
set_qe_commands "$KPOOLS"

cd "$WORK_DIR"
mkdir -p tmp
print_cluster_warning
extract_core_if_missing "O.wfc" "$PSEUDO_DIR/O.pbe-n-kjpaw_psl.0.1.UPF" "O 1s"


echo "=========================================="
echo "  SrTiO3 — O K-edge XAS"
echo "=========================================="

cat > scf.in << EOF
 &control
    calculation='scf',
    pseudo_dir = '$PSEUDO_DIR/',
    outdir='./tmp/',
    prefix='SrTiO3_OK',
 /
 &system
    ibrav = 1,
    celldm(1) = 7.38,
    nat = 5,
    ntyp = 4,
    ecutwfc = 55.0,
    ecutrho = 600.0,
    nbnd = 30,
    occupations = 'smearing',
    smearing = 'mp',
    degauss = 0.01,
 /
 &electrons
    mixing_beta = 0.3,
    conv_thr = 1.0d-8,
 /
ATOMIC_SPECIES
Sr  87.62   Sr.pbe-spn-kjpaw_psl.1.0.0.UPF
Ti  47.867  Ti.pbe-spn-kjpaw_psl.1.0.0.UPF
Oh   15.999  O.pbe-n-kjpaw_psl.0.1.UPF
O   15.999  O.pbe-n-kjpaw_psl.0.1.UPF
ATOMIC_POSITIONS crystal
Sr  0.00  0.00  0.00
Ti  0.50  0.50  0.50
Oh  0.50  0.50  0.00
O   0.50  0.00  0.50
O   0.00  0.50  0.50
K_POINTS automatic
4 4 4 1 1 1
EOF

echo "  Running pw.x SCF..."
$PW_CMD < scf.in > scf.out 2>&1
echo "  pw.x done (exit: $?)"
grep "PWSCF.*WALL" scf.out || true

cat > xspectra.in << EOF
 &input_xspectra
    calculation='xanes_dipole',
    prefix='SrTiO3_OK',
    outdir='./tmp/',
    xniter=2000,
    xcheck_conv=50,
    xepsilon(1)=1.0,
    xepsilon(2)=0.0,
    xepsilon(3)=0.0,
    xiabs=3,
    x_save_file='O_Kedge.sav',
    xerror=0.001,
 /
 &plot
    xnepoint=1000,
    xgamma=0.8,
    xemin=-10.0,
    xemax=40.0,
    terminator=.true.,
    cut_occ_states=.true.,
 /
 &pseudos
    filecore='O.wfc',
    r_paw(1)=1.2,
 /
 &cut_occ
    cut_desmooth=0.1,
 /
4 4 4 1 1 1
EOF

echo "  Running xspectra.x (O K-edge, dipole)..."
$XS_CMD < xspectra.in > xspectra.out 2>&1
echo "  xspectra.x done (exit: $?)"
move_xanes_or_fail O_Kedge.dat
grep "xanes.*WALL" xspectra.out || true

echo ""
echo "  O K-edge COMPLETE."
echo "  Output: O_Kedge.dat"
