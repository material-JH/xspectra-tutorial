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
echo "  SrTiO3 — O K-edge XAS (HCH, 2x2x2 supercell)"
echo "=========================================="

# --- Extract core wavefunction from the original non-core-hole pseudo ---
extract_core_if_missing "O.wfc" "$PSEUDO_DIR/O.pbe-n-kjpaw_psl.0.1.UPF" "O 1s"

# --- SCF ---
# 2x2x2 supercell of SrTiO3 cubic perovskite
# Unit cell: a=7.38 bohr, 5 atoms (Sr, Ti, 3×O)
# Supercell: a=14.76 bohr, 40 atoms (8 Sr, 8 Ti, 24 O)
# O K-edge HCH: 1 absorber Oh with HCH pseudo, 23 normal O
# ntyp=4: Sr, Ti, Oh, O
# xiabs=3 -> Oh (3rd species)
# tot_charge = +0.5 (single half core-hole)
# nbnd = 240 (30 * 8, scaled from unit cell)
# K_POINTS: 2 2 2 (from 4 4 4 / 2)

cat > scf.in << EOF
 &control
    calculation='scf',
    pseudo_dir = '$PSEUDO_DIR/',
    outdir='./tmp/',
    prefix='SrTiO3_OK_HCH_super',
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
Sr  87.62   Sr.pbe-spn-kjpaw_psl.1.0.0.UPF
Ti  47.867  Ti.pbe-spn-kjpaw_psl.1.0.0.UPF
Oh  15.999  O.pbe-n-kjpaw_psl.0.1-HCH.UPF
O   15.999  O.pbe-n-kjpaw_psl.0.1.UPF
ATOMIC_POSITIONS crystal
Sr  0.000  0.000  0.000
Sr  0.500  0.000  0.000
Sr  0.000  0.500  0.000
Sr  0.000  0.000  0.500
Sr  0.500  0.500  0.000
Sr  0.500  0.000  0.500
Sr  0.000  0.500  0.500
Sr  0.500  0.500  0.500
Ti  0.250  0.250  0.250
Ti  0.750  0.250  0.250
Ti  0.250  0.750  0.250
Ti  0.250  0.250  0.750
Ti  0.750  0.750  0.250
Ti  0.750  0.250  0.750
Ti  0.250  0.750  0.750
Ti  0.750  0.750  0.750
Oh  0.250  0.250  0.000
O   0.250  0.000  0.250
O   0.000  0.250  0.250
O   0.750  0.250  0.000
O   0.750  0.000  0.250
O   0.500  0.250  0.250
O   0.250  0.750  0.000
O   0.250  0.500  0.250
O   0.000  0.750  0.250
O   0.250  0.250  0.500
O   0.250  0.000  0.750
O   0.000  0.250  0.750
O   0.750  0.750  0.000
O   0.750  0.500  0.250
O   0.500  0.750  0.250
O   0.750  0.250  0.500
O   0.750  0.000  0.750
O   0.500  0.250  0.750
O   0.250  0.750  0.500
O   0.250  0.500  0.750
O   0.000  0.750  0.750
O   0.750  0.750  0.500
O   0.750  0.500  0.750
O   0.500  0.750  0.750
K_POINTS automatic
2 2 2 1 1 1
EOF

echo "  Running pw.x SCF (HCH, 2x2x2 supercell)..."
$PW_CMD < scf.in > scf.out 2>&1
echo "  pw.x done (exit: $?)"
grep "PWSCF.*WALL" scf.out || true

# --- XSpectra ---
cat > xspectra.in << EOF
 &input_xspectra
    calculation='xanes_dipole',
    prefix='SrTiO3_OK_HCH_super',
    outdir='./tmp/',
    xniter=2000,
    xcheck_conv=50,
    xepsilon(1)=1.0,
    xepsilon(2)=0.0,
    xepsilon(3)=0.0,
    xiabs=3,
    x_save_file='O_Kedge_HCH_super.sav',
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
2 2 2 1 1 1
EOF

echo "  Running xspectra.x (O K-edge HCH, 2x2x2 supercell)..."
$XS_CMD < xspectra.in > xspectra.out 2>&1
echo "  xspectra.x done (exit: $?)"
move_xanes_or_fail O_Kedge_HCH_super.dat
grep "xanes.*WALL" xspectra.out || true

echo ""
echo "  O K-edge HCH (2x2x2 supercell) COMPLETE."
echo "  Output: O_Kedge_HCH_super.dat"
