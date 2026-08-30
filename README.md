![logo](imgs/logo.png)

# Structural Bioinformatics (W2025)

Teaching materials for the course "Structural Bioinformatics" at [FHWN](https://tulln.fhwn.ac.at/studiengang/bio-data-science).

## Getting started

After some research, Google Colab is the best option.

### Google Colab

Google colab is a free service that allows you to run jupyter notebooks in the cloud.

| Link                                                                                                                               | Description                          |
|------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|
| <a href="https://colab.research.google.com/github/yerkoescalona/structural_bioinformatics/blob/main/ex00/scientific_python_crash_course.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Exercise 00: Scientific Python Crash Course for Structural Bioinformatics |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural_bioinformatics/blob/main/ex01/ex01_guide.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Exercise 01 — Guide: Exploring and Analyzing Protein Structures in the PDB Database (worked walkthrough on 1FSZ; read this first) |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural_bioinformatics/blob/main/ex01/ex01_workbook.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Exercise 01 — Workbook: rebuild the analysis on your own protein (graded) |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural_bioinformatics/blob/main/ex02/ex02_guide.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Exercise 02 — Guide: AlphaFold prediction and confidence (worked example on p53/3D08; read this first. No GPU needed) |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural_bioinformatics/blob/main/ex02/ex02_workbook.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Exercise 02 — Workbook: analyse your own protein (graded; no GPU needed) |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural_bioinformatics/blob/main/ex03/ex03_guide.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Exercise 03 — Guide: molecular dynamics with OpenMM (worked example on 2JAC, solvated; read this first) |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural_bioinformatics/blob/main/ex03/ex03_workbook.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Exercise 03 — Workbook: simulate your own protein (graded) |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural_bioinformatics/blob/main/ex04/ex04_guide.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Exercise 04 — Guide: cheminformatics and docking (worked: RDKit debugging + 2IEN; read this first) |
| <a href="https://colab.research.google.com/github/yerkoescalona/structural_bioinformatics/blob/main/ex04/ex04_workbook.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Exercise 04 — Workbook: dock your own protein (graded) |


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


## Your project protein

Each student is **assigned** a protein for the capstone project, and the assignment names
**the ligand to work with**. That pairing runs through the whole course: you record it on
the Character Sheet at the end of Exercise 01, predict its structure in Exercise 02,
simulate it in Exercise 03, and dock it in Exercise 04.

The assignment is distributed separately — you do not need to choose one yourself.

The pairing matters more than it might look. A great many PDB entries contain small
molecules that are **experimental artifacts** rather than biology: buffer components,
cryoprotectants, crystallisation additives. They appear in the file exactly the same way a
real substrate does. Assigned pairs have been checked, so the ligand you are given is one
with a genuine biological relationship to the protein. Exercise 01 teaches you to make
that distinction yourself, on your own structure.

### License
[![BY-NC-SA](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)


This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).
