# HTML Slide Deck Alignment Notes

Reviewed on 2026-06-01 against:

- `README.md`
- `docs/00_*.md` through `docs/10_troubleshooting.md`
- `docs/xspectra_tutorial_presentation.html`

## Summary

The HTML slide deck is broadly aligned with the tutorial's main story: cluster setup, Diamond first, SrTiO3 O K-edge, core-hole comparison, EELS comparison, Ti L-edge, output reading, and troubleshooting.

It is not fully aligned with the current Markdown tutorial sequence and setup guidance. Before the next tutorial, update the deck or explicitly label it as a condensed half-day overview.

## Gaps To Fix

1. Setup wording is slightly stale.
   - Current tutorial says most students should edit only the cluster module lines first; `pw.x`, `xspectra.x`, `BIN_DIR`, and `QE_ROOT` are auto-detected.
   - Deck slides 7-8 still frame `env.sh` as a place to enter module name and `TOOLS_DIR`.
   - Suggested update: say `TOOLS_DIR` is only needed when `upf2plotcore.sh` is missing from the module installation.

2. Dedicated QE source/pseudopotential guidance is missing.
   - Current tutorial has `docs/00_qe_source_and_pseudopotentials.md`.
   - Deck mentions pseudopotentials and `upf2plotcore.sh`, but does not clearly say that Diamond and SrTiO3 pseudopotentials are bundled, and that QE source is only needed for helper tools such as `XSpectra/tools/upf2plotcore.sh`.
   - Suggested update: add one setup/preflight card or slide: bundled pseudo, optional `~/q-e`, do not clone `q-e/` inside this tutorial repo.

3. Lesson order differs from the README.
   - README order: Ti L-edge -> Core-hole methods -> EELS comparison -> Supercell/MPI -> Troubleshooting.
   - Deck order: O K-edge -> Core-hole comparison -> EELS comparison -> Ti L-edge -> Output/Troubleshooting -> Advanced topics.
   - Suggested update: either match the README order or keep the current order but label it as an instructional reordering for a short live session.

4. Linux/QE input basics are compressed out of the deck.
   - Current tutorial has explicit chapters for Linux basics, QE namelists/cards, and XSpectra pipeline.
   - Deck includes the pipeline and `xiabs`, but not enough to cue students to read `docs/01_...`, `docs/02_...`, and `docs/03_...`.
   - Suggested update: add a "read before class" or "where this appears in the docs" slide.

5. Command context can become ambiguous.
   - Slide 12 ends with `cd SrTiO3` and `python3 plot_spectra.py`.
   - Slide 16 shows `python3 scripts/compare_reference.py SrTiO3/O_Kedge/O_Kedge.dat ...`, which assumes the repo root as the current directory.
   - Suggested update: add `cd ..` before the slide 16 comparison command, or rewrite the paths for running from `SrTiO3/`.

6. Slurm is prominent; PBS is only mentioned.
   - Current tutorial links `scheduler/pbs_examples.md` and notes `qsub` for PBS/Torque.
   - Deck gives a Slurm-first job submission slide.
   - Suggested update: add a short PBS note on the scheduler slide, or point non-Slurm users directly to `scheduler/pbs_examples.md`.

7. Supercell/MPI is underrepresented if it is part of the next tutorial.
   - Current `docs/09_supercell_and_mpi.md` includes concrete points: HCH supercell, `tot_charge=+0.5`, `-nk 4`, `-nd 1`, and scheduler-only execution.
   - Deck keeps this as one advanced-topic card.
   - Suggested update: if the next tutorial includes supercells, add a dedicated slide; otherwise label it as follow-up reading.

## Suggested Next Deck Patch

- Update slides 7-8 for current `env.sh.example` auto-detection behavior.
- Add a setup slide for bundled pseudopotentials and optional QE source tree.
- Align or explain the Ti L-edge/core-hole/EELS order.
- Fix the slide 16 working-directory assumption.
- Add a PBS pointer and, if needed, one Supercell/MPI slide.
