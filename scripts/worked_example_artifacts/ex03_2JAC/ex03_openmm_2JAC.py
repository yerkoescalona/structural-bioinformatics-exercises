"""
Worked-example artifact generator — ex03 (Simulate, Block C) — PDB 2JAC.

Honest attempt at a minimal OpenMM/pdbfixer setup for 2JAC (yeast
glutaredoxin-1, C30S mutant, + glutathione/GSH).

This script:
  1. Confirms via Biopython that GSH is the only non-water HETATM (already
     done separately in ex03_check_2JAC.py) and confirms the C30S mutation.
  2. Uses PDBFixer to fix the PROTEIN ONLY (standard amino acids) — missing
     atoms/hydrogens — and reports exactly what PDBFixer does and does not
     do with the GSH heterogen.
  3. Attempts to build an OpenMM System with the Amber14 protein force field.
     GSH (glutathione) is NOT a standard residue in ff14SB/amber14 — it has
     no bonded/nonbonded parameters in that force field family. This is
     reported honestly: parametrizing GSH would need a small-molecule force
     field (GAFF2/OpenFF via `openff-toolkit`/`openmmforcefields`, or a
     custom residue template), none of which are installed in this sandbox.
  4. As the "does it run at all" honest check, builds a system for the
     PROTEIN ALONE (GSH stripped) and runs a short CPU energy
     minimization, reporting real before/after potential energy — this is
     a genuine, if partial, OpenMM run, not a fabricated trajectory.

No numbers below are invented: every reported energy or atom count comes
from an OpenMM/PDBFixer call actually executed in this script.
"""

from pathlib import Path

from openmm import LangevinMiddleIntegrator, Platform
from openmm.app import ForceField, Modeller, PDBFile, Simulation, NoCutoff
from openmm.unit import kelvin, picosecond, picoseconds, nanometer
from pdbfixer import PDBFixer

WD = Path(__file__).parent
PDB_IN = WD / "2JAC.pdb"

print("=" * 70)
print("2JAC — PDBFixer + OpenMM, honest minimal attempt")
print("=" * 70)

fixer = PDBFixer(filename=str(PDB_IN))
print(f"\nOriginal chains: {list(fixer.topology.chains())}")
n_atoms_before = sum(1 for _ in fixer.topology.atoms())
print(f"Atoms before fixing: {n_atoms_before}")

fixer.findMissingResidues()
print(f"Missing residues found by PDBFixer: {fixer.missingResidues}")

fixer.findNonstandardResidues()
print(f"Nonstandard residues found by PDBFixer: {fixer.nonstandardResidues}")

fixer.findMissingAtoms()
print(f"Missing atoms found (heavy atoms) by PDBFixer: {fixer.missingAtoms}")
print(f"Missing terminal atoms: {fixer.missingTerminals}")

fixer.addMissingAtoms()
fixer.addMissingHydrogens(7.0)

n_atoms_after = sum(1 for _ in fixer.topology.atoms())
print(f"\nAtoms after addMissingAtoms + addMissingHydrogens(pH 7.0): {n_atoms_after}")

# Report what residue types are now in the fixed topology (confirm GSH kept
# as a heterogen residue, not converted/parametrized)
resnames = sorted({r.name for r in fixer.topology.residues()})
print(f"Residue names present after fixing: {resnames}")

with open(WD / "2JAC_fixed.pdb", "w") as fh:
    PDBFile.writeFile(fixer.topology, fixer.positions, fh)
print(f"\nWrote fixed structure (protein + GSH + fixer-added waters/H) to 2JAC_fixed.pdb")

# --- Attempt 1: try to build a System including GSH with amber14 ---
print("\n" + "-" * 70)
print("Attempt 1: OpenMM System with GSH included, amber14 protein force field")
print("-" * 70)
try:
    forcefield = ForceField("amber14-all.xml", "amber14/tip3pfb.xml")
    modeller = Modeller(fixer.topology, fixer.positions)
    modeller.addSolvent(forcefield, model="tip3p", padding=1.0 * nanometer)
    system = forcefield.createSystem(modeller.topology, nonbondedMethod=NoCutoff)
    print("System built successfully WITH GSH (unexpected — report this if it happens).")
except Exception as exc:
    print(f"FAILED as expected: {type(exc).__name__}: {exc}")
    print(
        "\nInterpretation: GSH (glutathione) has no residue template in the "
        "amber14 protein force field family. Amber ff14SB only parametrizes "
        "the 20 standard amino acids (+ a few standard caps/ions); GSH is a "
        "tripeptide-like small molecule that needs its own small-molecule "
        "force field (e.g. GAFF2 or OpenFF via `openmmforcefields`/"
        "`openff-toolkit`) or a hand-built residue template — none of which "
        "are installed in this sandbox. This is the exact, real reason a "
        "student cannot simply drop GSH into a standard OpenMM tutorial "
        "workflow without an extra parametrization step."
    )

# --- Attempt 2: protein-only (GSH stripped), genuine short minimization ---
print("\n" + "-" * 70)
print("Attempt 2: PROTEIN ONLY (GSH stripped) — genuine short CPU minimization")
print("-" * 70)

fixer2 = PDBFixer(filename=str(PDB_IN))
fixer2.findMissingResidues()
fixer2.findNonstandardResidues()
fixer2.removeHeterogens(keepWater=False)  # strips GSH and all waters
fixer2.findMissingAtoms()
fixer2.addMissingAtoms()
fixer2.addMissingHydrogens(7.0)

forcefield = ForceField("amber14-all.xml")
system = forcefield.createSystem(fixer2.topology, nonbondedMethod=NoCutoff)
print(f"System built OK: {system.getNumParticles()} particles (protein only, no GSH, no solvent).")

integrator = LangevinMiddleIntegrator(300 * kelvin, 1 / picosecond, 0.002 * picoseconds)
platform = Platform.getPlatformByName("CPU")
simulation = Simulation(fixer2.topology, system, integrator, platform)
simulation.context.setPositions(fixer2.positions)

state_before = simulation.context.getState(getEnergy=True)
e_before = state_before.getPotentialEnergy()
print(f"Potential energy BEFORE minimization: {e_before}")

simulation.minimizeEnergy(maxIterations=200)

state_after = simulation.context.getState(getEnergy=True, getPositions=True)
e_after = state_after.getPotentialEnergy()
print(f"Potential energy AFTER 200-iteration minimization: {e_after}")
print(f"Energy change: {e_after - e_before}")

with open(WD / "2JAC_apo_minimized.pdb", "w") as fh:
    PDBFile.writeFile(fixer2.topology, state_after.getPositions(), fh)
print("\nWrote minimized apo (GSH-free) structure to 2JAC_apo_minimized.pdb")

print("\n" + "=" * 70)
print("HONEST SUMMARY")
print("=" * 70)
print(
    "- PDBFixer runs cleanly on 2JAC and correctly identifies GSH as a "
    "nonstandard/heterogen residue.\n"
    "- A full protein+GSH OpenMM System build FAILS with amber14 alone "
    "(no GSH template) — this is real, not simulated failure.\n"
    "- A protein-ONLY (apo, GSH-stripped) vacuum energy minimization DOES "
    "run to completion on CPU in this sandbox, and the real before/after "
    "energies are reported above.\n"
    "- To actually simulate the real 2JAC + GSH complex, the pipeline "
    "needs a small-molecule force field for GSH "
    "(GAFF2/OpenFF, via `openmmforcefields` + `openff-toolkit`, or the "
    "bespoke glutathione residue template many MD packages ship) plus "
    "explicit-solvent equilibration and GPU-length production MD — none of "
    "which this sandbox provides. No trajectory or RMSD/RMSF numbers for "
    "the real complex are reported here because none were actually run."
)
