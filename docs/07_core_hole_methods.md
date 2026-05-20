# Core-Hole Methods

Core-hole approximations model the interaction between the excited electron and the core hole left behind.

## Approaches

| Method | Pseudopotential | `tot_charge` | Use |
|---|---|---:|---|
| No core hole | standard pseudo | 0 | fastest starting point |
| Full core hole (FCH) | one core electron removed | +1.0 | strong final-state effect |
| Half core hole (HCH) | half core electron removed | +0.5 | common compromise |

## Important rules

1. The absorber must be its own species label.
2. Only the absorber uses the core-hole pseudopotential.
3. `tot_charge` corresponds to one core hole and does not scale with supercell size.
4. `filecore` should be extracted from the original non-core-hole pseudopotential.
5. Core-hole pseudopotentials need GIPAW reconstruction for XSpectra.

## Generate pseudopotentials

The `ld1.x` inputs are in:

```text
SrTiO3/pseudo/gen_*.in
```

Run them only if the instructor wants to demonstrate pseudopotential generation. Most tutorial sessions should use the provided pseudopotentials to save time.
