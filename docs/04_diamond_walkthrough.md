# Diamond C K-edge Walkthrough

Diamond is the first exercise because it is small and runs quickly.

## What it teaches

- Basic XSpectra workflow.
- Absorber labeling with `C_h`.
- No-core-hole vs full-core-hole spectra.
- Replotting with `xonly_plot`.
- Removing occupied-state artifacts with `cut_occ_states`.

## Run

On a compute node or through a scheduler:

```bash
bash run_all_examples.sh diamond-only
python3 plot_spectra.py
```

The public tutorial script keeps Diamond as the short first exercise. The SrTiO3 examples are run separately in later lessons or with `bash run_all_examples.sh srtio3`.

## Files

- `diamond/diamond.scf.in`
- `diamond/diamond.xspectra.in`
- `diamond/diamond.xspectra_replot.in`
- `diamond/diamondh.scf.in`
- `diamond/diamondh.xspectra.in`

## Check output

```bash
ls diamond/*.dat
grep "WALL" diamond/*.out
```

Expected spectra are in:

```text
reference_output/diamond/
```
