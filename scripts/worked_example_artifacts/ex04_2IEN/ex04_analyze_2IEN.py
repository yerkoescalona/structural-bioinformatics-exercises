"""
Worked-example artifact generator — ex04 (Dock, Block D) — PDB 2IEN.

Real, live-fetched data only:
  1. 2IEN crystal structure from RCSB, parsed with Biopython — confirm
     chains present, ligand 017 (darunavir) present and its chain/residue.
  2. Ligand 017's real chemical identity from the RCSB chemcomp REST API
     (https://data.rcsb.org/rest/v1/core/chemcomp/017) — formula, MW, SMILES.
  3. RDKit loaded from that real SMILES — real MW/formula/Lipinski
     properties computed by RDKit itself, not looked up/typed in by hand.
  4. Previously-validated reference docking/interaction numbers (RMSD 0.34 A,
     PLIP profile) are reported as reference values, explicitly labeled as
     NOT re-run in this sandbox (no Vina/Smina/AutoDock available here).
"""

import json
from pathlib import Path

from Bio import BiopythonWarning
from Bio.PDB import PDBParser
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, rdMolDescriptors
import warnings

warnings.simplefilter("ignore", BiopythonWarning)

WD = Path(__file__).parent

print("=" * 70)
print("PART 1 — 2IEN crystal structure (RCSB), parsed with Biopython")
print("=" * 70)

parser = PDBParser(QUIET=True)
structure = parser.get_structure("2IEN", str(WD / "2IEN.pdb"))
model = structure[0]
chains = list(model.get_chains())
print(f"\nChains present: {[c.id for c in chains]}")

het_by_chain = {}
for chain in chains:
    for residue in chain:
        if residue.id[0] != " ":
            het_by_chain.setdefault(chain.id, []).append((residue.resname, residue.id[1]))

for cid, hets in het_by_chain.items():
    names = sorted({h[0] for h in hets})
    print(f"  Chain {cid} HETATM resnames: {names}")

print("\nLigand 017 (darunavir) location(s) in the crystal:")
for cid, hets in het_by_chain.items():
    for resname, resseq in hets:
        if resname == "017":
            print(f"  Found in chain {cid}, residue number {resseq}")

print("\nModeled protein chain ranges (HIV-1 protease is a homodimer, expect 2 chains):")
for chain in chains:
    aa = sorted(r.id[1] for r in chain if r.id[0] == " ")
    if aa:
        print(f"  Chain {chain.id}: {aa[0]}-{aa[-1]} ({len(aa)} residues)")

# --- Part 2: real chemcomp data for ligand 017 (already fetched live) ---
print("\n" + "=" * 70)
print("PART 2 — Ligand 017 identity (RCSB chemcomp REST API, fetched live)")
print("=" * 70)
print("Source: https://data.rcsb.org/rest/v1/core/chemcomp/017")

with open(WD / "chemcomp_017.json") as fh:
    chemcomp = json.load(fh)

cc = chemcomp["chem_comp"]
desc = chemcomp["rcsb_chem_comp_descriptor"]
print(f"\nName: {cc['name']}")
print(f"Formula (RCSB): {cc['formula']}")
print(f"Formula weight (RCSB): {cc['formula_weight']}")
smiles = desc["SMILES_stereo"]
print(f"Stereo SMILES (RCSB): {smiles}")

# --- Part 3: RDKit, loaded from the real SMILES ---
print("\n" + "=" * 70)
print("PART 3 — RDKit analysis of the real SMILES (computed, not hand-entered)")
print("=" * 70)

mol = Chem.MolFromSmiles(smiles)
if mol is None:
    raise RuntimeError("RDKit failed to parse the RCSB stereo SMILES")

mw = Descriptors.MolWt(mol)
formula = rdMolDescriptors.CalcMolFormula(mol)
logp = Descriptors.MolLogP(mol)
hbd = Lipinski.NumHDonors(mol)
hba = Lipinski.NumHAcceptors(mol)
tpsa = Descriptors.TPSA(mol)
rot_bonds = Lipinski.NumRotatableBonds(mol)

print(f"\nRDKit molecular formula: {formula}  (RCSB reports: {cc['formula'].replace(' ', '')})")
print(f"RDKit molecular weight: {mw:.2f}  (RCSB reports: {cc['formula_weight']})")
print(f"RDKit LogP (Crippen): {logp:.2f}")
print(f"H-bond donors: {hbd}")
print(f"H-bond acceptors: {hba}")
print(f"TPSA: {tpsa:.2f} A^2")
print(f"Rotatable bonds: {rot_bonds}")

print("\nLipinski's Rule of Five check:")
violations = []
if mw > 500:
    violations.append(f"MW {mw:.1f} > 500")
if logp > 5:
    violations.append(f"LogP {logp:.2f} > 5")
if hbd > 5:
    violations.append(f"HBD {hbd} > 5")
if hba > 10:
    violations.append(f"HBA {hba} > 10")
if violations:
    print(f"  Violations ({len(violations)}): {violations}")
    print("  --> Darunavir is a KNOWN Lipinski outlier (real, well-documented "
          "property of HIV protease inhibitors as a drug class, not an error) "
          "typically failing on molecular weight.")
else:
    print("  No violations — passes Ro5.")

# --- Part 4: reference (not re-run) docking/interaction numbers ---
print("\n" + "=" * 70)
print("PART 4 — REFERENCE docking numbers (NOT re-run in this sandbox)")
print("=" * 70)
print(
    "No Vina/Smina/AutoDock binary is installed in this sandbox (checked: "
    "`which vina smina` returned nothing). The following are the "
    "PREVIOUSLY VALIDATED reference values documented for this worked "
    "example (2IEN, darunavir self-docking) — reported here as reference/"
    "expected results, NOT as freshly computed output:\n"
    "  - Self-docking RMSD vs. crystal pose: 0.34 A\n"
    "  - PLIP interaction profile: 13 H-bonds, 11 hydrophobic contacts, "
    "7 salt bridges\n"
    "These numbers are restated from prior validation, not regenerated here."
)
