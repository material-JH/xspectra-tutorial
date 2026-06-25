#!/usr/bin/env python3
"""Plot SrTiO3 O K-edge XANES spectra.

Run from the SrTiO3 directory:

    python3 plot_spectra.py

The script plots generated files in O_Kedge*/ when they exist. If the
calculation has not been run yet, it falls back to reference_output/.
"""
from pathlib import Path
import os
import sys
import subprocess


def _filter_cluster_loader_warning(stderr: str) -> str:
    lines = []
    for line in stderr.splitlines():
        if "libuuid.so.1: no version information available" in line:
            continue
        lines.append(line)
    return "\n".join(lines)


def _reexec_with_plot_python_if_needed() -> None:
    if os.environ.get("XSPECTRA_PLOT_PYTHON_REEXEC") == "1":
        return
    try:
        import importlib.util
        if importlib.util.find_spec("matplotlib") and importlib.util.find_spec("numpy"):
            return
    except ImportError:
        pass
    candidates = [
        os.environ.get("XSPECTRA_PLOT_PYTHON"),
        "/apps/applications/PYTHON/3.7/bin/python3",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        candidate_path = Path(candidate)
        if not candidate_path.exists() or not os.access(str(candidate_path), os.X_OK):
            continue
        if candidate_path.resolve() == Path(sys.executable).resolve():
            continue
        completed = subprocess.run(
            [str(candidate_path), "-c", "import matplotlib, numpy"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
        )
        if completed.returncode == 0:
            child_env = os.environ.copy()
            child_env["XSPECTRA_PLOT_PYTHON_REEXEC"] = "1"
            os.execve(str(candidate_path), [str(candidate_path)] + sys.argv, child_env)
    raise SystemExit(
        "ERROR: matplotlib/numpy are not available in this Python.\n"
        "Fix: load the plotting Python module first, e.g. 'module load python/3.7',\n"
        "or set XSPECTRA_PLOT_PYTHON=/path/to/python3."
    )


def _prefer_python_shared_libs() -> None:
    python_lib = Path(sys.executable).resolve().parent.parent / "lib"
    if os.environ.get("XSPECTRA_PLOT_LD_REEXEC") == "1":
        return
    if not (python_lib / "libz.so.1").exists():
        return
    current_paths = [path for path in os.environ.get("LD_LIBRARY_PATH", "").split(":") if path]
    python_lib_path = str(python_lib)
    if current_paths[:1] == [python_lib_path]:
        return
    child_env = os.environ.copy()
    child_env["LD_LIBRARY_PATH"] = ":".join(
        [python_lib_path] + [path for path in current_paths if path != python_lib_path]
    )
    child_env["XSPECTRA_PLOT_LD_REEXEC"] = "1"
    completed = subprocess.run(
        [sys.executable] + sys.argv, env=child_env, stderr=subprocess.PIPE, universal_newlines=True,
    )
    filtered_stderr = _filter_cluster_loader_warning(completed.stderr)
    if filtered_stderr:
        print(filtered_stderr, file=sys.stderr)
    raise SystemExit(completed.returncode)


_reexec_with_plot_python_if_needed()
_prefer_python_shared_libs()
import matplotlib

if "--show" not in sys.argv:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent

SPECTRA = {
    "O K-edge (initial state)": ("O_Kedge/O_Kedge.dat", "b-"),
    "O K-edge FCH": ("O_Kedge_FCH/O_Kedge_FCH.dat", "r-"),
    "O K-edge HCH": ("O_Kedge_HCH/O_Kedge_HCH.dat", "g-"),
}


def load_xanes(filepath: Path) -> np.ndarray:
    if not filepath.exists():
        raise FileNotFoundError(
            f"Missing {filepath}. Run the O K-edge example first."
        )
    return np.loadtxt(filepath)


def main() -> None:
    fig, ax = plt.subplots(1, 1, figsize=(8, 4.8), constrained_layout=True)

    for label, (rel_path, style) in SPECTRA.items():
        gen = BASE / rel_path
        ref = BASE / ".." / "reference_output" / "SrTiO3" / rel_path
        source = gen if gen.exists() else ref
        data = load_xanes(source)
        ax.plot(data[:, 0], data[:, 1], style, linewidth=1.5, label=label)
        print(f"Using: {source}")

    ax.set_xlabel("Energy (eV)")
    ax.set_ylabel("Absorption (arb. units)")
    ax.set_title("SrTiO3 — O K-edge XANES")
    ax.set_xlim(-5, 35)
    ax.axvline(0, color="gray", linestyle="--", alpha=0.5, label="Fermi level")
    ax.legend(fontsize=8, frameon=False)
    ax.grid(True, alpha=0.3)

    fig.suptitle("SrTiO3 Cubic Perovskite — O K-edge XANES", fontsize=14, fontweight="bold")
    outpath = BASE / "SrTiO3_spectra.png"
    fig.savefig(outpath, dpi=150, bbox_inches="tight")
    print(f"Saved: {outpath}")

    if "--show" in sys.argv:
        plt.show()


if __name__ == "__main__":
    main()
