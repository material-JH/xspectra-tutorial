# Quantum ESPRESSO Input Basics

QE inputs are plain text. They contain namelists and cards.

## Namelists

Example:

```fortran
&control
   calculation='scf',
   prefix='SrTiO3_OK',
   outdir='./tmp/',
   pseudo_dir='../pseudo/',
/
```

Common namelists:

- `&control`: what calculation to run and where files go.
- `&system`: crystal, cutoffs, bands, occupations.
- `&electrons`: SCF convergence settings.

## Cards

Example:

```fortran
ATOMIC_SPECIES
Sr  87.62   Sr.pbe-spn-kjpaw_psl.1.0.0.UPF
Ti  47.867  Ti.pbe-spn-kjpaw_psl.1.0.0.UPF
Oh  15.999  O.pbe-n-kjpaw_psl.0.1.UPF
O   15.999  O.pbe-n-kjpaw_psl.0.1.UPF
```

Important cards:

- `ATOMIC_SPECIES`: labels, masses, pseudopotential files.
- `ATOMIC_POSITIONS`: atom labels and coordinates.
- `K_POINTS`: Brillouin-zone sampling.

## Parameters students should recognize

- `nat`: number of atoms.
- `ntyp`: number of atomic species labels.
- `ecutwfc`: plane-wave cutoff for wavefunctions.
- `ecutrho`: charge-density cutoff, important for PAW/USPP.
- `nbnd`: number of bands. XSpectra needs enough unoccupied states.
- `prefix`: name used for QE saved files.
- `outdir`: scratch directory.
- `pseudo_dir`: directory containing UPF pseudopotentials.

## Absorber labels

XSpectra identifies the absorbing atom by species index, not atom number. Therefore the absorber is often given a special label such as `Oh`, `Tih`, or `C_h`.

For SrTiO3 O K-edge:

```fortran
ATOMIC_SPECIES
Sr  ...
Ti  ...
Oh  ...   ! absorber, species 3
O   ...   ! spectator oxygen, species 4
```

Then in XSpectra:

```fortran
xiabs=3
```

This is one of the most common mistakes in first XSpectra calculations.
