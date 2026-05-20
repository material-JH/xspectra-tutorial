# Instructor Checklist

Before the tutorial session:

- Confirm all students have cluster accounts and can log in.
- Confirm the QE module includes `pw.x`, `xspectra.x`, and `ld1.x`.
- Confirm `upf2plotcore.sh` is available.
- Prepare the correct `env.sh` for the local cluster.
- Run `bash check_setup.sh` from a fresh clone.
- Submit the Diamond Slurm/PBS test job.
- Submit at least one SrTiO3 test job.
- Confirm Python plotting works or prepare pre-generated plots.
- Decide whether students run core-hole and supercell jobs live or inspect reference outputs.
- Prepare fallback output files in case the queue is slow.
- Remind students not to run large MPI jobs on login nodes.
- Open `docs/xspectra_tutorial_presentation.html` locally in a browser for the tutorial introduction.

During the session:

1. Start with Diamond.
2. Use SrTiO3 O K-edge for the main EELS-relevant example.
3. Use Ti L-edge as a qualitative white-line interpretation example.
4. Show reference outputs if jobs are still queued.
5. Leave supercell and benchmarking as advanced material.
