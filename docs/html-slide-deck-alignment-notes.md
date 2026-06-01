# HTML Slide Deck Alignment Notes

Reviewed on 2026-06-01 against:

- `README.md`
- `docs/00_*.md` through `docs/10_troubleshooting.md`
- `docs/xspectra_tutorial_presentation.html`

## Summary

At review time, the HTML slide deck was broadly aligned with the tutorial's main story: cluster setup, Diamond first, SrTiO3 O K-edge, core-hole comparison, EELS comparison, Ti L-edge, output reading, and troubleshooting.

The review found it was not fully aligned with the current Markdown tutorial sequence and setup guidance, and recommended updating the deck or explicitly labeling it as a condensed half-day overview.

## Update Status

Patched on 2026-06-01 in `docs/xspectra_tutorial_presentation.html`.

- Setup wording now emphasizes module-first editing and auto-detection of `pw.x`, `xspectra.x`, `BIN_DIR`, and `QE_ROOT`.
- The deck now has a dedicated QE source/pseudopotential slide covering bundled Diamond/SrTiO3 UPF files, optional `~/q-e`, and the warning not to clone `q-e/` inside this tutorial repository.
- A document-map slide now explains the README order and labels the deck as a live-session compression/reordering.
- The output-reading slide now enters `SrTiO3/O_Kedge` before reading local output and returns to the repository root before running `scripts/compare_reference.py`.
- The scheduler slide now points PBS/Torque users to `scheduler/pbs_examples.md`.
- A dedicated Supercell/MPI slide now includes HCH supercell, `tot_charge = +0.5`, `-nk 4`, `-nd 1`, and scheduler-only execution guidance.
- Screen footer alignment now uses shared slide constants. The footer bar extends by its horizontal padding so the footer text/count align to the same slide grid as the header/body text.
- Follow-up screen cleanup hides the right-side header context label and the footer title/count text in browser presentation mode. The footer now keeps only the progress bar, so labels like `학생용 실습 가이드`, `시작`, and `1 / 23` no longer create a visible header/footer alignment mismatch.
- Header typography now uses a Korean-first font stack with normal case and tighter letter spacing so mixed labels like `XSpectra 튜토리얼` do not look like two different font sizes.
- Print/PDF CSS now defines a 16:9 page with `@page { size: 16in 9in; margin: 0; }`, exact color printing, `zoom: .8`, and a final-slide `last-of-type` page-break rule.

The notes below are kept as the original review record.

## Visual / Export Status

1. Footer alignment is patched for screen presentation.
   - The deck now defines `--slide-margin-x` and `--footer-pad-x` once.
   - The footer bar starts at `slide margin - footer padding`, so the padded footer text/count land on the same visual grid as the slide header/body.
   - After the follow-up cleanup, the footer title/count are hidden in screen mode and the footer is still hidden in print/PDF, matching the previous print behavior.

2. 16:9 print/PDF export is patched.
   - Verified on 2026-06-01 with Chromium through Playwright's Python API using `prefer_css_page_size=True`.
   - Result: 23 pages, `1152 x 648 pt`, no extra blank page.
   - The generic `playwright pdf` CLI still defaults to Letter unless the API/browser honors CSS page size; use browser print/Save to PDF with CSS page size, or Playwright API with `preferCSSPageSize` enabled.

## Original Gaps Reviewed

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

## Original Suggested Next Deck Patch

- Update slides 7-8 for current `env.sh.example` auto-detection behavior.
- Add a setup slide for bundled pseudopotentials and optional QE source tree.
- Align or explain the Ti L-edge/core-hole/EELS order.
- Fix the slide 16 working-directory assumption.
- Add a PBS pointer and, if needed, one Supercell/MPI slide.
