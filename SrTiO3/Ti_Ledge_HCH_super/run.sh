#!/bin/bash
set -euo pipefail

WORK_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$WORK_DIR/../.." && pwd)"
source "$PROJECT_ROOT/scripts/common.sh"
load_xspectra_env "$PROJECT_ROOT"
PSEUDO_DIR="${SRTIO3_PSEUDO_DIR:-$WORK_DIR/../pseudo}"
KPOOLS="${KPOOLS:-4}"
set_qe_commands "$KPOOLS" 1

cd "$WORK_DIR"
mkdir -p tmp
print_cluster_warning


echo "=========================================="
echo "  SrTiO3 — Ti L-edge XAS (HCH, 2x2x2 supercell)"
echo "=========================================="

# --- Extract core wavefunction from the original non-core-hole pseudo ---
extract_core_if_missing "Ti.wfc" "$PSEUDO_DIR/Ti.pbe-spn-kjpaw_psl.1.0.0.UPF" "Ti 2p"

# 2x2x2 supercell: 40 atoms (8 Sr, 8 Ti, 24 O)
# Ti L-edge HCH: 1 absorber Tih with HCH pseudo, 7 normal Ti
# ntyp=4: Sr, Tih, Ti, O  -> xiabs=2 (Tih is 2nd species)

cat > scf.in << EOF
 &control
    calculation='scf',
    pseudo_dir = '$PSEUDO_DIR/',
    outdir='./tmp/',
    prefix='SrTiO3_TiL_HCH_super',
 /
 &system
    ibrav = 1,
    celldm(1) = 14.76,
    nat = 40,
    ntyp = 4,
    ecutwfc = 55.0,
    ecutrho = 600.0,
    nbnd = 240,
    occupations = 'smearing',
    smearing = 'mp',
    degauss = 0.01,
    tot_charge = +0.5,
 /
 &electrons
    mixing_beta = 0.3,
    conv_thr = 1.0d-8,
 /
ATOMIC_SPECIES
Sr   87.62   Sr.pbe-spn-kjpaw_psl.1.0.0.UPF
Tih  47.867  Ti.pbe-spn-kjpaw_psl.1.0.0-HCH.UPF
Ti   47.867  Ti.pbe-spn-kjpaw_psl.1.0.0.UPF
O    15.999  O.pbe-n-kjpaw_psl.0.1.UPF
ATOMIC_POSITIONS crystal
Sr   0.000  0.000  0.000
Sr   0.500  0.000  0.000
Sr   0.000  0.500  0.000
Sr   0.000  0.000  0.500
Sr   0.500  0.500  0.000
Sr   0.500  0.000  0.500
Sr   0.000  0.500  0.500
Sr   0.500  0.500  0.500
Tih  0.250  0.250  0.250
Ti   0.750  0.250  0.250
Ti   0.250  0.750  0.250
Ti   0.250  0.250  0.750
Ti   0.750  0.750  0.250
Ti   0.750  0.250  0.750
Ti   0.250  0.750  0.750
Ti   0.750  0.750  0.750
O    0.250  0.250  0.000
O    0.250  0.000  0.250
O    0.000  0.250  0.250
O    0.750  0.250  0.000
O    0.750  0.000  0.250
O    0.500  0.250  0.250
O    0.250  0.750  0.000
O    0.250  0.500  0.250
O    0.000  0.750  0.250
O    0.250  0.250  0.500
O    0.250  0.000  0.750
O    0.000  0.250  0.750
O    0.750  0.750  0.000
O    0.750  0.500  0.250
O    0.500  0.750  0.250
O    0.750  0.250  0.500
O    0.750  0.000  0.750
O    0.500  0.250  0.750
O    0.250  0.750  0.500
O    0.250  0.500  0.750
O    0.000  0.750  0.750
O    0.750  0.750  0.500
O    0.750  0.500  0.750
O    0.500  0.750  0.750
K_POINTS automatic
2 2 2 1 1 1
EOF

echo "  Running pw.x SCF (HCH, 2x2x2 supercell)..."
$PW_CMD < scf.in > scf.out 2>&1
echo "  pw.x done (exit: $?)"
grep "PWSCF.*WALL" scf.out || true

cat > xspectra.in << EOF
 &input_xspectra
    calculation='xanes_dipole',
    edge='L2',
    prefix='SrTiO3_TiL_HCH_super',
    outdir='./tmp/',
    xniter=2000,
    xcheck_conv=50,
    xepsilon(1)=1.0,
    xepsilon(2)=1.0,
    xepsilon(3)=1.0,
    xiabs=2,
    x_save_file='Ti_Ledge_HCH_super.sav',
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
    filecore='Ti.wfc',
    r_paw(0)=1.8,
    r_paw(2)=1.8,
 /
 &cut_occ
    cut_desmooth=0.1,
 /
2 2 2 1 1 1
EOF

echo "  Running xspectra.x (Ti L-edge HCH, 2x2x2 supercell)..."
$XS_CMD < xspectra.in > xspectra.out 2>&1
echo "  xspectra.x done (exit: $?)"
move_xanes_or_fail Ti_Ledge_HCH_super.dat
grep "xanes.*WALL" xspectra.out || true

echo ""
echo "  Ti L-edge HCH (2x2x2 supercell) COMPLETE."
echo "  Output: Ti_Ledge_HCH_super.dat"
