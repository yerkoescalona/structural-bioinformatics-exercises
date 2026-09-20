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

| Link | What it covers |
|------|----------------|
| <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex00/scientific_python_crash_course.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | **ex00** Scientific Python crash course |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex01/ex01_guide.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | **ex01** Exploring structures in the PDB, worked on 1FSZ |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex02/ex02_guide.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | **ex02** AlphaFold prediction and confidence, worked on p53 and 3D08 |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex03/ex03_guide.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | **ex03** Molecular dynamics with OpenMM, worked on solvated 2JAC |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex04/ex04_guide.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | **ex04** Cheminformatics and docking, worked on 2IEN with darunavir |

### Your project protein

Your group **chooses** one protein, and **the ligand comes with it**. That pairing carries
through **all four workbooks**, each covering a different area: exploring the structure
(ex01), predicting it with AlphaFold (ex02), simulating it (ex03) and docking its ligand
(ex04). It is also the protein of your final project.

Browse the candidates and choose:

| Link | Description |
|------|-------------|
| <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/candidate_proteins.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Candidate proteins: browse them, then pick the one your group will carry through the whole course |

**The protein is yours to pick. The ligand is not.** Each candidate is listed with the one
ligand that has already been run end to end with that protein: molecular dynamics, docking,
and a simulation of the two together.

### The workbooks: what you hand in

Each workbook repeats its guide's analysis on **your own protein**, and these are the
graded artefacts. Do the matching guide first.

| Link | What you produce |
|------|------------------|
| <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex01/ex01_workbook.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | **ex01** Your protein's Character Sheet and a first look at its structure |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex02/ex02_workbook.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | **ex02** A predicted structure for your protein, read against its confidence |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex03/ex03_workbook.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | **ex03** A simulation of your protein and its ligand |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural-bioinformatics-exercises/blob/main/ex04/ex04_workbook.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | **ex04** Your ligand docked back into your protein |

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
