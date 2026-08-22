"""
Worked-example artifact generator — ex01 (Explore, Block A) — PDB 1FSZ.

Downloads the real 1FSZ crystal structure from RCSB and reports, using only
values parsed from the downloaded file (nothing invented):
  - chains present
  - HETATM residues (expect GDP)
  - modeled residue ranges per chain vs. gaps (unmodeled residues)
  - mean B-factor per chain and per rough domain split (N-terminal GTPase-like
    vs. C-terminal domain), using the residue numbering actually present

Requires: biopython, pandas (both available in this sandbox venv).
"""

import warnings
from pathlib import Path

import pandas as pd
from Bio import BiopythonWarning
from Bio.PDB import PDBParser, PPBuilder

warnings.simplefilter("ignore", BiopythonWarning)

PDB_PATH = Path(__file__).parent / "1FSZ.pdb"
OUT_DIR = Path(__file__).parent

parser = PDBParser(QUIET=True)
structure = parser.get_structure("1FSZ", str(PDB_PATH))
model = structure[0]

print("=" * 70)
print("1FSZ — real downloaded PDB, parsed with Biopython")
print("=" * 70)

# --- Chains present ---
chains = list(model.get_chains())
print(f"\nChains present: {[c.id for c in chains]}")

# --- HETATM residues (non-standard residues, includes waters) ---
het_records = []
for chain in chains:
    for residue in chain:
        hetflag, resseq, icode = residue.id
        if hetflag != " ":
            het_records.append(
                {
                    "chain": chain.id,
                    "resname": residue.resname,
                    "resseq": resseq,
                    "hetflag": hetflag.strip(),
                }
            )
het_df = pd.DataFrame(het_records)
print("\nHETATM residue composition (raw counts by resname):")
print(het_df["resname"].value_counts().to_string())

non_water_het = het_df[het_df["resname"] != "HOH"]
print("\nNon-water HETATM entries (the real cofactor(s)):")
print(non_water_het.to_string(index=False))

# --- Modeled residue ranges vs. gaps ---
print("\n" + "-" * 70)
print("Modeled residue ranges per chain (standard amino acids only)")
print("-" * 70)

for chain in chains:
    aa_resseqs = sorted(
        residue.id[1]
        for residue in chain
        if residue.id[0] == " "  # standard amino acid, not HETATM/water
    )
    if not aa_resseqs:
        continue
    first, last = aa_resseqs[0], aa_resseqs[-1]
    full_span = set(range(first, last + 1))
    modeled = set(aa_resseqs)
    missing = sorted(full_span - modeled)

    # collapse missing into contiguous ranges for readability
    ranges = []
    if missing:
        start = prev = missing[0]
        for r in missing[1:]:
            if r == prev + 1:
                prev = r
            else:
                ranges.append((start, prev))
                start = prev = r
        ranges.append((start, prev))

    print(f"\nChain {chain.id}:")
    print(f"  Modeled span in file: {first}-{last} ({len(modeled)} residues actually present)")
    print(f"  Full nominal span:    {first}-{last} ({len(full_span)} positions)")
    print(f"  Unmodeled positions within that span: {len(missing)}")
    print(f"  Gap ranges: {ranges}")

# --- SEQRES vs ATOM record comparison (construct length) ---
print("\n" + "-" * 70)
print("SEQRES (construct) length vs. ATOM-modeled length, from the raw file")
print("-" * 70)
seqres_lengths = {}
with open(PDB_PATH) as fh:
    seqres_counts = {}
    for line in fh:
        if line.startswith("SEQRES"):
            chain_id = line[11]
            n_res = int(line[13:17])
            seqres_counts[chain_id] = n_res  # last one wins; same value repeated per line
for cid, n in seqres_counts.items():
    print(f"  SEQRES chain {cid}: {n} residues in the construct")

# The gap-detection above only finds INTERNAL gaps within the modeled span.
# 1FSZ's real 38 missing residues are at the TERMINI (SEQRES numbers the
# construct 1..372; ATOM records only start at 23 and end at 356) — compute
# that explicitly here so the number is traceable to the file, not asserted.
print("\n" + "-" * 70)
print("Terminal (N-/C-term) unmodeled residues: SEQRES construct vs ATOM span")
print("-" * 70)
for chain in chains:
    aa_resseqs = sorted(r.id[1] for r in chain if r.id[0] == " ")
    if not aa_resseqs or chain.id not in seqres_counts:
        continue
    construct_n = seqres_counts[chain.id]
    modeled_first, modeled_last = aa_resseqs[0], aa_resseqs[-1]
    n_term_missing = modeled_first - 1  # assumes SEQRES numbering starts at 1
    c_term_missing = construct_n - modeled_last
    total_missing = n_term_missing + c_term_missing
    print(f"  Chain {chain.id}: construct = {construct_n} res (SEQRES); "
          f"modeled = {modeled_first}-{modeled_last} ({len(aa_resseqs)} res)")
    print(f"    N-terminal residues never modeled: 1-{n_term_missing} ({n_term_missing} res)")
    print(f"    C-terminal residues never modeled: {modeled_last+1}-{construct_n} ({c_term_missing} res)")
    print(f"    TOTAL unmodeled residues (termini only, no internal gaps found): {total_missing}")

# --- B-factor analysis ---
print("\n" + "-" * 70)
print("Mean B-factor per chain, and per crude N-/C-terminal split")
print("-" * 70)

bfactor_records = []
for chain in chains:
    for residue in chain:
        if residue.id[0] != " ":
            continue
        for atom in residue:
            bfactor_records.append(
                {
                    "chain": chain.id,
                    "resseq": residue.id[1],
                    "resname": residue.resname,
                    "atom": atom.get_name(),
                    "bfactor": atom.get_bfactor(),
                }
            )
bdf = pd.DataFrame(bfactor_records)

print("\nMean B-factor per chain (all atoms):")
print(bdf.groupby("chain")["bfactor"].agg(["mean", "std", "count"]).to_string())

# Per-residue mean, then split at the midpoint of the modeled range as a crude
# N-terminal (GTPase domain) vs C-terminal domain proxy — NOTE: this midpoint
# split is a simple heuristic for this artifact, not a validated domain
# boundary; a real domain boundary would need to be taken from the literature
# or a domain-annotation tool (e.g. CATH/SCOP), which we do not invent here.
per_res = bdf.groupby(["chain", "resseq"])["bfactor"].mean().reset_index()
for chain_id in per_res["chain"].unique():
    sub = per_res[per_res["chain"] == chain_id]
    mid = (sub["resseq"].min() + sub["resseq"].max()) / 2
    n_term = sub[sub["resseq"] <= mid]
    c_term = sub[sub["resseq"] > mid]
    print(f"\nChain {chain_id} — crude midpoint split at residue {mid:.0f}:")
    print(f"  N-terminal half ({sub['resseq'].min()}-{int(mid)}): mean B-factor = {n_term['bfactor'].mean():.2f}")
    print(f"  C-terminal half ({int(mid)+1}-{sub['resseq'].max()}): mean B-factor = {c_term['bfactor'].mean():.2f}")

# --- Save tables to disk ---
het_df.to_csv(OUT_DIR / "1FSZ_hetatm_residues.csv", index=False)
per_res.to_csv(OUT_DIR / "1FSZ_per_residue_bfactor.csv", index=False)
print(f"\nSaved: 1FSZ_hetatm_residues.csv, 1FSZ_per_residue_bfactor.csv in {OUT_DIR}")

# --- Sequence via Biopython (for reference) ---
ppb = PPBuilder()
for chain in chains:
    peptides = ppb.build_peptides(chain)
    seq = "".join(str(pp.get_sequence()) for pp in peptides)
    if seq:
        print(f"\nChain {chain.id} modeled sequence length (Biopython PPBuilder): {len(seq)}")
