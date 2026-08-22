"""
Worked-example artifact generator — ex02 (Predict, Block B) — PDB 3D08 vs
AlphaFold DB (UniProt P04637, human p53).

Two real, independently-verifiable data sources, no invented numbers:
  1. The 3D08 crystal structure downloaded from RCSB (p53 core domain,
     R249S hotspot mutant, resolved region + real Zn2+).
  2. The AlphaFold DB prediction for full-length human p53 (P04637),
     fetched live from the public AlphaFold DB REST API
     (https://alphafold.ebi.ac.uk/api/prediction/P04637) — the SAME source
     used to pick 3D08 as a worked example in the first place.

We report AlphaFold DB's own summary confidence metrics (mean pLDDT, and the
fraction of the model in each confidence bin) plus the per-residue pLDDT at
and around residue 249 (the R249S hotspot position) from the confidence
JSON, and the crystal's own resolved range + HETATM content for comparison.
Nothing here is a real, GPU-run AlphaFold prediction — that is out of scope
for this sandbox and would be dishonest to fake.
"""

import json
from pathlib import Path

import pandas as pd
from Bio import BiopythonWarning
from Bio.PDB import PDBParser
import warnings

warnings.simplefilter("ignore", BiopythonWarning)

WD = Path(__file__).parent

# --- Part 1: the 3D08 crystal, downloaded and parsed for real ---
print("=" * 70)
print("PART 1 — 3D08 crystal structure (RCSB), parsed with Biopython")
print("=" * 70)

parser = PDBParser(QUIET=True)
structure = parser.get_structure("3D08", str(WD / "3D08.pdb"))
model = structure[0]
chains = list(model.get_chains())
print(f"\nChains present: {[c.id for c in chains]}")

het_records = []
for chain in chains:
    for residue in chain:
        hetflag, resseq, icode = residue.id
        if hetflag != " ":
            het_records.append({"chain": chain.id, "resname": residue.resname, "resseq": resseq})
het_df = pd.DataFrame(het_records)
print("\nHETATM composition (raw counts):")
print(het_df["resname"].value_counts().to_string())
non_water = het_df[het_df["resname"] != "HOH"]
print("\nNon-water HETATM (expect a structural Zn2+, i.e. resname ZN):")
print(non_water.to_string(index=False))

print("\nResolved (modeled) residue range per chain:")
for chain in chains:
    aa = sorted(r.id[1] for r in chain if r.id[0] == " ")
    if aa:
        print(f"  Chain {chain.id}: {aa[0]}-{aa[-1]} ({len(aa)} residues modeled)")

# Confirm the R249S mutation is present in the crystal (SEQRES / ATOM at 249)
print("\nResidue identity at position 249 in each chain (expect SER = the R249S mutant):")
for chain in chains:
    for residue in chain:
        if residue.id[0] == " " and residue.id[1] == 249:
            print(f"  Chain {chain.id}, residue 249: {residue.resname}")

# --- Part 2: AlphaFold DB live API for the same protein, full-length ---
print("\n" + "=" * 70)
print("PART 2 — AlphaFold DB (live API), UniProt P04637 (human p53, full-length WT)")
print("=" * 70)
print("Source: https://alphafold.ebi.ac.uk/api/prediction/P04637 (fetched live, this session)")

with open(WD / "afdb_P04637.json") as fh:
    afdb = json.load(fh)

# The API can return multiple fragment entries for long proteins; take the
# primary full-length AF-P04637-F1 entry.
primary = next(e for e in afdb if e["modelEntityId"] == "AF-P04637-F1")

print(f"\nModel entity: {primary['modelEntityId']}  (tool: {primary['toolUsed']})")
print(f"Sequence length in this AF model: {primary['sequenceEnd'] - primary['sequenceStart'] + 1} residues")
print(f"Global mean pLDDT (globalMetricValue): {primary['globalMetricValue']}")
print("Confidence-bin fractions (as reported by AlphaFold DB):")
print(f"  Very low (pLDDT < 50):  {primary['fractionPlddtVeryLow']*100:.1f}%")
print(f"  Low      (50-70):       {primary['fractionPlddtLow']*100:.1f}%")
print(f"  Confident(70-90):       {primary['fractionPlddtConfident']*100:.1f}%")
print(f"  Very high(>90):         {primary['fractionPlddtVeryHigh']*100:.1f}%")
low_or_worse = primary["fractionPlddtVeryLow"] + primary["fractionPlddtLow"]
print(f"  --> Combined low + very-low: {low_or_worse*100:.1f}%")

# --- Part 3: per-residue pLDDT around residue 249 from the confidence JSON ---
print("\n" + "-" * 70)
print("Per-residue AlphaFold pLDDT around the R249 hotspot position (residues 240-260)")
print("(source: AF-P04637-F1-confidence_v6.json, fetched live)")
print("-" * 70)

with open(WD / "AF-P04637-F1-confidence.json") as fh:
    conf = json.load(fh)

conf_df = pd.DataFrame(
    {
        "residueNumber": conf["residueNumber"],
        "pLDDT": conf["confidenceScore"],
        "category": conf["confidenceCategory"],
    }
)
window = conf_df[(conf_df["residueNumber"] >= 240) & (conf_df["residueNumber"] <= 260)]
print(window.to_string(index=False))

# Core domain range roughly 94-312 in p53 (per UniProt domain annotation
# used implicitly by choosing 3D08's construct) — report mean pLDDT over the
# crystal's own resolved range for direct comparison.
resolved_ranges = {}
for chain in chains:
    aa = sorted(r.id[1] for r in chain if r.id[0] == " ")
    if aa:
        resolved_ranges[chain.id] = (aa[0], aa[-1])

for cid, (start, end) in resolved_ranges.items():
    sub = conf_df[(conf_df["residueNumber"] >= start) & (conf_df["residueNumber"] <= end)]
    print(f"\nAlphaFold mean pLDDT over 3D08 chain {cid}'s own resolved range ({start}-{end}): "
          f"{sub['pLDDT'].mean():.1f}")
    print(f"  Fraction of that range with pLDDT < 70 (AlphaFold's own low-confidence cutoff): "
          f"{(sub['pLDDT'] < 70).mean()*100:.1f}%")

conf_df.to_csv(WD / "P04637_AFDB_per_residue_pLDDT.csv", index=False)
print(f"\nSaved full per-residue pLDDT table to P04637_AFDB_per_residue_pLDDT.csv")
