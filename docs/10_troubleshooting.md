# Troubleshooting

## `env.sh not found`

Create it from the template:

```bash
cp env.sh.example env.sh
vim env.sh
```

## `pw.x: command not found` or missing `pw.x`

Likely cause: wrong QE module or `BIN_DIR`.

```bash
module avail quantum
module load quantum-espresso
which pw.x
```

Then update `env.sh`.

## `xspectra.x` missing

The loaded QE build may not include XSpectra. Ask the instructor for the XSpectra-enabled QE module.

## `upf2plotcore.sh` missing

Check `TOOLS_DIR`:

```bash
find "$QE_ROOT" -name upf2plotcore.sh
```

Set `TOOLS_DIR` in `env.sh` to the directory containing that script.

## Cannot open pseudopotential file

Check `pseudo_dir` in the generated `scf.in`, and verify the file exists:

```bash
ls SrTiO3/pseudo/
ls "$EXAMPLE_PSEUDO_DIR"
```

## Missing `O.wfc` or `Ti.wfc`

The revised scripts generate these automatically. If needed, regenerate manually:

```bash
$TOOLS_DIR/upf2plotcore.sh SrTiO3/pseudo/O.pbe-n-kjpaw_psl.0.1.UPF > O.wfc
$TOOLS_DIR/upf2plotcore.sh SrTiO3/pseudo/Ti.pbe-spn-kjpaw_psl.1.0.0.UPF > Ti.wfc
```

## `xspectra.x did not produce xanes.dat`

Read the end of the output:

```bash
tail -80 xspectra.out
```

Common causes are wrong `xiabs`, missing `filecore`, missing SCF data in `outdir`, or an incompatible pseudopotential.

## MPI launcher fails

On Slurm clusters, prefer inside jobs:

```bash
export MPI_RUN="srun -n $NPROCS"
```

On other systems:

```bash
export MPI_RUN="mpirun -np $NPROCS"
```

If you see login-node policy errors, submit through the scheduler instead of running interactively.

## Job exceeded wall time

Use reference outputs during the tutorial, or ask the instructor to increase the wall time in the scheduler script.
