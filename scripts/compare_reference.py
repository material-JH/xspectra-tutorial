#!/usr/bin/env python3
"""Compare a generated XSpectra data file with a reference output."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np


def load(path: Path) -> np.ndarray:
    if not path.exists():
        raise FileNotFoundError(path)
    data = np.loadtxt(path)
    if data.ndim != 2 or data.shape[1] < 2:
        raise ValueError(f"{path} does not look like a two-column spectrum")
    return data[:, :2]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("generated", type=Path)
    parser.add_argument("reference", type=Path)
    parser.add_argument("--rtol", type=float, default=1.0e-5)
    parser.add_argument("--atol", type=float, default=1.0e-8)
    args = parser.parse_args()

    generated = load(args.generated)
    reference = load(args.reference)

    print(f"Generated: {args.generated} ({len(generated)} points)")
    print(f"Reference: {args.reference} ({len(reference)} points)")

    if generated.shape != reference.shape:
        print("FAIL shape mismatch")
        return 1

    energy_diff = np.max(np.abs(generated[:, 0] - reference[:, 0]))
    intensity_diff = np.max(np.abs(generated[:, 1] - reference[:, 1]))
    print(f"Max |energy difference|:    {energy_diff:.6e} eV")
    print(f"Max |intensity difference|: {intensity_diff:.6e}")

    if np.allclose(generated, reference, rtol=args.rtol, atol=args.atol):
        print("PASS spectra match within tolerance")
        return 0

    print("WARN spectra differ beyond tolerance")
    print("This can happen across QE/MPI/compiler versions; inspect an overlay plot.")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        raise SystemExit(1)
