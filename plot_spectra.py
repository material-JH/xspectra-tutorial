#!/usr/bin/env python3
"""Plot the Diamond XSpectra output.

Run from the repository root:

    python3 plot_spectra.py

The script plots generated files in diamond/ when they exist. If the Diamond
calculation has not been run yet, it falls back to reference_output/diamond/.

The SrTiO3 plots are generated separately with:

    cd SrTiO3 && python3 plot_spectra.py
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
    """Restart with a Python that has the plotting packages installed.

    Login shells on some clusters start with /usr/bin/python3, while the
    matplotlib/numpy stack lives in the python/3.7 module. Make the beginner
    command `python3 plot_spectra.py` work by finding that module Python.
    """
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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
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
    """Restart with Python's shared libraries first on module-based HPC Python.

    Some clusters put /usr/lib64 before the Python module's lib directory in
    LD_LIBRARY_PATH. Matplotlib's libpng can then load the system zlib, which is
    too old for the wheel. Put the active Python installation's lib directory
    first before importing matplotlib. The child stderr is filtered only for the
    known non-fatal cluster libuuid loader warning; real errors still print.
    """
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
        [sys.executable] + sys.argv,
        env=child_env,
        stderr=subprocess.PIPE,
        universal_newlines=True,
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

DIAMOND_FILES = (
    "diamond.xspectra.dat",
    "diamond.xspectra_replot.dat",
    "diamondh.xspectra.dat",
)


def load_xanes(filepath: Path) -> np.ndarray:
    if not filepath.exists():
        raise FileNotFoundError(
            f"Missing {filepath}. Run the Diamond example or keep reference_output/diamond/."
        )
    return np.loadtxt(filepath)


def main() -> None:
    generated = BASE / "diamond"
    ref = BASE / "reference_output" / "diamond"
    source = generated if all((generated / name).exists() for name in DIAMOND_FILES) else ref
    print(f"Using Diamond spectra from: {source}")

    raw = load_xanes(source / "diamond.xspectra.dat")
    no_hole = load_xanes(source / "diamond.xspectra_replot.dat")
    full_hole = load_xanes(source / "diamondh.xspectra.dat")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)

    ax1.plot(raw[:, 0], raw[:, 1], color="0.55", alpha=0.65, label="No core-hole, occupied states included")
    ax1.plot(no_hole[:, 0], no_hole[:, 1], color="C0", label="No core-hole, occupied states cut")
    ax1.plot(full_hole[:, 0], full_hole[:, 1], color="C3", label="Full core-hole, occupied states cut")
    ax1.set_title("Diamond C K-edge")
    ax1.set_xlabel("Energy (eV)")
    ax1.set_ylabel("Absorption cross-section (arb. units)")
    ax1.set_xlim(-5, 30)
    ax1.legend(fontsize=8)

    common_energy = no_hole[:, 0]
    full_hole_interp = np.interp(common_energy, full_hole[:, 0], full_hole[:, 1])
    diff = full_hole_interp - no_hole[:, 1]
    ax2.plot(common_energy, diff, color="k", label="Core-hole – no core-hole")
    ax2.axhline(0, color="gray", linewidth=0.5)
    ax2.set_title("Difference (core-hole – no core-hole)")
    ax2.set_xlabel("Energy (eV)")
    ax2.set_ylabel("Δ absorption (arb. units)")
    ax2.set_xlim(-2, 25)
    ax2.legend(fontsize=8)

    outpath = BASE / "xanes_spectra.png"
    fig.savefig(outpath, dpi=180, facecolor="white")
    print(f"Saved: {outpath}")

    if "--show" in sys.argv:
        plt.show()


if __name__ == "__main__":
    main()
