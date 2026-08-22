# %% [markdown]
# # structural-bioinformatics-exercises: Colab compatibility check (instructor tool)
#
# Checks whether each exercise's dependencies still install/import/work on the CURRENT
# Colab runtime. Built from each notebook's OWN real Colab install cell (the `if
# 'google.colab' in ...: !pip install ...` branch each notebook already runs), not from
# `environment.yml` (that file pins the SEPARATE local-conda-reproduction env, which is
# not necessarily what a live Colab session actually gets).
#
# This file lives in `scripts/` (instructor tooling), not in any `exN/` folder --
# students never see this. It contains no reference to any other repo's internals; it
# only re-runs, standalone, exactly what each notebook's own setup cell already does.
#
# Cells are `# %%`-marked (VS Code/Jupytext convention) -- run cell-by-cell in VS Code's
# Interactive Window, convert to a real notebook (`pip install jupytext && jupytext
# --to notebook colab_compatibility_check.py`) and upload to Colab, or copy each block
# into its own Colab cell.
#
# ex02 (AlphaFold) is checked at the IMPORT level only -- its real setup downloads a
# ~3.5GB parameter file and compiles a real model, deliberately too heavy for a
# compatibility smoke test. Run the real `ex02/ex02.ipynb` for that.
#
# ex04's PyMOL/DockingPie step is a **manual desktop install** ("Follow the instruction
# to download and install PyMOL from moodle" -- ex04.ipynb, "Step 0: Install PyMOL") --
# it never runs inside Colab at all, so there is nothing for this script to test there.

# %%
import importlib
import subprocess
import sys


def pip_install(*pkgs: str) -> None:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs], check=False)


def check_import(label: str, module: str) -> bool:
    try:
        importlib.import_module(module)
        print(f"  [OK]   {label}")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"  [FAIL] {label}: {type(exc).__name__}: {exc}")
        return False


# %% [markdown]
# ## ex00 -- Scientific Python crash course (prerequisite, no Frontier section)

# %%
pip_install("numpy", "pandas", "matplotlib")
check_import("numpy", "numpy")
check_import("pandas", "pandas")
check_import("matplotlib", "matplotlib")

# %% [markdown]
# ## ex01 -- PDB/structures/databases (Block A)
#
# Exact pins from `ex01.ipynb`'s own Colab branch:
# `numpy==2.0.2 scipy==1.16.2 pandas==2.2.2 plotly==5.24.1 biopandas==0.4.1 pypdb==2.4
# tqdm==4.67.1 py3dmol==2.4.0`

# %%
pip_install(
    "numpy==2.0.2", "scipy==1.16.2", "pandas==2.2.2", "plotly==5.24.1",
    "biopandas==0.4.1", "pypdb==2.4", "tqdm==4.67.1", "py3dmol==2.4.0",
)
for label, mod in [
    ("numpy", "numpy"), ("scipy", "scipy"), ("pandas", "pandas"), ("plotly", "plotly"),
    ("biopandas", "biopandas"), ("pypdb", "pypdb"), ("tqdm", "tqdm"), ("py3Dmol", "py3Dmol"),
]:
    check_import(label, mod)

# %% [markdown]
# ### ex01 functional check: fetch a real PDB entry and parse it (not just import)

# %%
try:
    import pypdb
    from biopandas.pdb import PandasPdb

    # A real, well-known small entry -- same reference structure this course already uses.
    pdb_id = "1UBQ"
    pdb_text = pypdb.get_pdb_file(pdb_id, filetype="pdb")
    if not pdb_text:
        print(f"  [FAIL] pypdb.get_pdb_file({pdb_id}) returned nothing")
    else:
        tmp_path = f"/tmp/{pdb_id}.pdb"
        with open(tmp_path, "w") as fh:
            fh.write(pdb_text)
        parsed = PandasPdb().read_pdb(tmp_path)
        n_atoms = len(parsed.df["ATOM"])
        print(f"  [OK]   fetched {pdb_id} live via pypdb, biopandas parsed {n_atoms} ATOM records")
except Exception as exc:  # noqa: BLE001
    print(f"  [FAIL] ex01 functional check: {type(exc).__name__}: {exc}")

# %% [markdown]
# ## ex02 -- AlphaFold (Block B) -- IMPORT-ONLY, no real prediction run here
#
# Exact packages from `ex02.ipynb`'s own setup cell: `jax[cuda12]==0.5.3 jaxlib==0.5.3`
# (Colab-specific JAX version fix) plus `biopython dm-haiku ml-collections py3Dmol`
# (installed alongside the `af_backprop` clone). `tensorflow` is imported but not
# `pip install`ed in that cell -- it relies on whatever Colab's base image ships.

# %%
pip_install("jax[cuda12]==0.5.3", "jaxlib==0.5.3")
pip_install("biopython", "dm-haiku", "ml-collections", "py3Dmol")
for label, mod in [
    ("jax", "jax"), ("tensorflow (Colab base image, not pip-installed by this cell)", "tensorflow"),
    ("Bio (biopython)", "Bio"), ("dm-haiku", "haiku"), ("ml_collections", "ml_collections"),
    ("py3Dmol", "py3Dmol"),
]:
    check_import(label, mod)
print(
    "  [SKIPPED] real AlphaFold parameter download (~3.5GB) + model compilation -- "
    "run ex02.ipynb itself for that; this is an import-level smoke test only."
)

# %% [markdown]
# ## ex03 -- Molecular dynamics, OpenMM/MDAnalysis (Block C)
#
# Exact pins from `ex03.ipynb`'s own Colab branch: `openmm==8.2.0 mdanalysis==2.10.0
# py3dmol==2.4.0`. Note `pdbfixer` is NOT in that install cell -- the notebook only uses
# it later as an optional CLI (`!pdbfixer YOURPROTEIN.pdb`, in the "For the project"
# section), not as a Python import, so it is not required for the graded portion.

# %%
pip_install("openmm==8.2.0", "mdanalysis==2.10.0", "py3dmol==2.4.0")
check_import("openmm", "openmm")
check_import("MDAnalysis", "MDAnalysis")
check_import("py3Dmol", "py3Dmol")

# %% [markdown]
# ### ex03 functional check: a REAL short OpenMM run on the notebook's own villin.pdb
#
# Uses `ex03/villin.pdb`, the exact structure the real exercise teaches on -- not a
# synthetic fixture. Requires this script to run from within a checkout that has
# `ex03/villin.pdb` alongside it (true for both a local run and an uploaded/cloned repo
# on Colab).

# %%
from pathlib import Path

villin_candidates = [Path("../ex03/villin.pdb"), Path("ex03/villin.pdb"), Path("villin.pdb")]
villin_path = next((p for p in villin_candidates if p.exists()), None)

if villin_path is None:
    print(f"  [SKIPPED] villin.pdb not found (tried {villin_candidates}) -- run from within the repo checkout")
else:
    try:
        import openmm
        import openmm.app as app
        import openmm.unit as unit

        pdb = app.PDBFile(str(villin_path))
        forcefield = app.ForceField("amber14-all.xml", "amber14/tip3pfb.xml")
        system = forcefield.createSystem(pdb.topology, nonbondedMethod=app.NoCutoff)
        integrator = openmm.LangevinMiddleIntegrator(
            300 * unit.kelvin, 1 / unit.picosecond, 0.002 * unit.picoseconds
        )
        simulation = app.Simulation(pdb.topology, system, integrator)
        simulation.context.setPositions(pdb.positions)
        simulation.minimizeEnergy(maxIterations=50)
        state = simulation.context.getState(getEnergy=True)
        energy = state.getPotentialEnergy()
        print(f"  [OK]   real OpenMM minimization on villin.pdb converged, potential energy = {energy}")
    except Exception as exc:  # noqa: BLE001
        print(f"  [FAIL] ex03 functional check: {type(exc).__name__}: {exc}")

# %% [markdown]
# ## ex04 -- Cheminformatics (RDKit) + docking (Block D)
#
# Exact install from `ex04.ipynb`'s own Colab branch: `rdkit pandas matplotlib`
# (unpinned, as written in the notebook).
#
# **PyMOL/DockingPie is explicitly OUT OF SCOPE here** -- `ex04.ipynb`'s "Step 0: Install
# PyMOL" tells students to download a desktop PyMOL build from Moodle and install
# DockingPie as a PyMOL plugin by hand; none of that runs inside the Colab session, so
# there is nothing for a Colab script to install or verify.

# %%
pip_install("rdkit", "pandas", "matplotlib")
check_import("rdkit", "rdkit")
check_import("pandas", "pandas")
check_import("matplotlib", "matplotlib")

# %% [markdown]
# ### ex04 functional check: RDKit parses real data (ex04's own bundled dataset)

# %%
dataset_candidates = [Path("../ex04/chembl_drugs.txt.gz"), Path("ex04/chembl_drugs.txt.gz")]
dataset_path = next((p for p in dataset_candidates if p.exists()), None)

if dataset_path is None:
    print(f"  [SKIPPED] chembl_drugs.txt.gz not found (tried {dataset_candidates})")
else:
    try:
        import gzip

        from rdkit import Chem

        n_parsed, n_total = 0, 0
        with gzip.open(dataset_path, "rt") as fh:
            for line in fh:
                n_total += 1
                if n_total > 200:  # smoke test, not a full-dataset pass
                    break
                smiles = line.strip().split()[0] if line.strip() else ""
                if smiles and Chem.MolFromSmiles(smiles) is not None:
                    n_parsed += 1
        print(f"  [OK]   RDKit parsed {n_parsed}/{n_total} real molecules from ex04's own dataset")
    except Exception as exc:  # noqa: BLE001
        print(f"  [FAIL] ex04 functional check: {type(exc).__name__}: {exc}")

# %% [markdown]
# ## Optional, instructor-only: is a Colab-native PyMOL (`cealign`) even possible here?
#
# Not part of any graded exercise -- ex04 deliberately uses a DESKTOP PyMOL install
# instead. This cell only answers the standalone question "could a Colab session run
# PyMOL at all, in principle" via a plain `apt-get install pymol` (works because Colab's
# notebook VM runs as root). Skip this cell entirely if that question isn't relevant.

# %%
RUN_OPTIONAL_PYMOL_CHECK = False  # flip to True to actually try this

if RUN_OPTIONAL_PYMOL_CHECK:
    subprocess.run(["apt-get", "update", "-qq"], check=False)
    subprocess.run(["apt-get", "install", "-y", "-qq", "pymol"], check=False)
    result = subprocess.run(["python3", "-c", "import pymol; print('pymol import OK')"], capture_output=True, text=True)
    print(f"  {'[OK]' if result.returncode == 0 else '[FAIL]'} system pymol via apt-get: {result.stdout or result.stderr}")
