![logo](imgs/logo.png)

# Structural Bioinformatics (W2026)

Teaching materials for the course "Structural Bioinformatics" at [FHWN](https://tulln.fhwn.ac.at/studiengang/bio-data-science).

## Getting started

After some research, Google Colab is the best option.

### Google Colab

Google Colab is a free service that lets you run Jupyter notebooks in the cloud.

**No exercise requires a GPU.** A standard CPU runtime is enough throughout — you do not
need to spend your GPU allocation on this course.

### The guides: read these first

Each guide is a worked walkthrough on a fixed example. Nothing is graded here, and you do
not need your own protein to follow one.

| Day | Link | What it covers |
|-----|------|----------------|
| before | <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex00/scientific_python_crash_course.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Scientific Python crash course, the prerequisite |
| 1 | <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex01/ex01_guide.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Exploring structures in the PDB (worked on 1FSZ) |
| 2 | <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex02/ex02_guide.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | AlphaFold prediction and confidence (worked on p53 and 3D08) |
| 3 | <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex03/ex03_guide.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Molecular dynamics with OpenMM (worked on solvated 2JAC) |
| 4 | <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex04/ex04_guide.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Cheminformatics and docking (worked on 2IEN with darunavir) |

### Your project protein

Your group works on one protein for the capstone project, and it comes **paired with the
ligand to work with**. That pairing runs through the whole course: you record it on the
Character Sheet at the end of Exercise 01, predict its structure in Exercise 02, simulate
it in Exercise 03, and dock it in Exercise 04.

Browse the candidates and choose:

| Link | Description |
|------|-------------|
| <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/candidate_proteins.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Candidate proteins: browse them, then pick the one your group will carry through the whole course |

Nothing in that notebook needs to be run. Each entry has a picture, a short description,
its ligand code, and links to RCSB, UniProt and AlphaFold. Everything else about your
structure, the method it was solved by, its resolution, how many residues it has, how
confident AlphaFold is about it, you work out yourself. That is the exercise.

The protein and ligand pairing matters more than it might look. A great many PDB entries
contain small molecules that are **experimental artifacts** rather than biology: buffer
components, cryoprotectants, crystallisation additives. They appear in the file exactly the
same way a real substrate does. Every pairing in the list has been checked, so the ligand
named there is one with a genuine biological relationship to the protein. Exercise 01
teaches you to make that distinction yourself, on your own structure.

### The workbooks: what you hand in

Each workbook repeats its guide's analysis on **your own protein**, and these are the
graded artefacts. Do the matching guide first.

| Day | Link | What you produce |
|-----|------|------------------|
| 1 | <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex01/ex01_workbook.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Your protein's Character Sheet and a first look at its structure |
| 2 | <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex02/ex02_workbook.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | A predicted structure for your protein, read against its confidence |
| 3 | <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex03/ex03_workbook.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | A simulation of your protein and its ligand |
| 4 | <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex04/ex04_workbook.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Your ligand docked back into your protein |

### Conda

You are free to use the files

For Linux, Mac or Windows (via WSL).

1. **Create a new environment with conda:**

    ```bash
    conda env create -f environment.yml
    ```

    This will create an environment called `structbioinfo`.

2. **Activate the environment:**

    ```bash
    conda activate structbioinfo
    ```

3. **Update the environment for upcoming modifications:**

    ```bash
    conda activate structbioinfo
    conda env update --file environment.yml --prune
    ```

4. In VSCode, select the interpreter to the one you just created.


### License
[![BY-NC-SA](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)


This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).
