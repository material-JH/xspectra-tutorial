# Linux Basics for This Tutorial

Only a small set of Linux commands is needed.

## Navigation

```bash
pwd                 # show current directory
ls                  # list files
ls -lh              # list files with sizes
cd xspectra-tutorial    # enter a directory
cd ..               # go up one directory
```

## Files

```bash
cp env.sh.example env.sh
vim env.sh          # edit a text file
more xspectra.out   # view a long file; press q to quit
tail -40 xspectra.out
mkdir -p tmp
rm -rf tmp          # be careful: recursive delete
```

## Searching output

```bash
grep "WALL" scf.out
grep "error" xspectra.out
```

## Cluster commands

Slurm:

```bash
module list
module avail quantum
sbatch scheduler/slurm_diamond.sbatch
squeue -u "$USER"
scancel <jobid>
```

PBS/Torque:

```bash
qsub job.pbs
qstat -u "$USER"
qdel <jobid>
```

## Good habits

- Keep one terminal in the project root.
- Read `*.out` files when something fails.
- Do not run large calculations on login nodes.
- Ask the instructor before deleting shared files.
