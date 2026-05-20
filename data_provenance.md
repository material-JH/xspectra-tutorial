# Data and Pseudopotential Provenance

This tutorial contains input files, plotting scripts, reference outputs, pseudopotentials, and digitized/derived experimental comparison data. Before redistributing or publishing derived results, verify the license and citation requirements of each source.

## Quantum ESPRESSO Diamond example pseudopotentials

The Diamond example expects the standard pseudopotentials from the Quantum ESPRESSO XSpectra example distribution, typically under:

```text
$QE_ROOT/XSpectra/examples/pseudo/
```

These files are not bundled in this repository; configure `EXAMPLE_PSEUDO_DIR` in `env.sh`.

## SrTiO3 pseudopotentials

The SrTiO3 examples use PAW pseudopotentials from PSLibrary and derived core-hole variants generated with `ld1.x` inputs in `SrTiO3/pseudo/`.

Core-hole pseudopotentials are tutorial artifacts. The core wavefunction used by XSpectra should be extracted from the original non-core-hole pseudopotential.

## Experimental EELS comparison data

The SrTiO3 comparison uses a David Muller EELS reference image and digitized spectra in the `SrTiO3/` directory. The digitized files are for tutorial comparison and should not be treated as a substitute for the original experimental data source.

## Reference outputs

The `reference_output/` directory contains precomputed Quantum ESPRESSO / XSpectra outputs for tutorial validation. Numerical differences can occur across QE versions, compilers, MPI libraries, and processor counts.
