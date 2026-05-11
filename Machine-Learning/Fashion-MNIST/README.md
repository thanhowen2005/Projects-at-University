# CSC14005-Lab3: Fashion-MNIST Classification Pipeline

This repository contains the workflow for Lab 3 in CSC14005, focused on classifying Fashion-MNIST images using multiple model families and a structured experiment pipeline.

## Overview

The project is organized into two main phases:

1. Exploratory data analysis (EDA) and data preparation.
2. Model training and evaluation with several approaches:
	 - Logistic Regression (with HOG features)
	 - Support Vector Machine (SVM)
	 - Random Forest
	 - Multi-Layer Perceptron (MLP)

The dataset is stored in CSV format and follows the common Fashion-MNIST split:

- Training set: 60,000 samples
- Test set: 10,000 samples
- 10 target classes

## Repository Structure

```text
.
|-- eda.ipynb
|-- README.md
|-- data/
|   |-- fashion_mnist_train_60k.csv
|   |-- fashion_mnist_test_10k.csv
|   `-- labels.csv
`-- model/
		|-- logistic_regression.ipynb
		|-- svm.ipynb
		|-- random-forest.ipynb
		`-- mlp.ipynb
```

## Notebook Roles

- `eda.ipynb`
	- Data ingestion and structural checks.
	- Data quality checks (missing values, duplicates, bounds checks).
	- Descriptive analysis and visualization.
	- Dimensionality reduction analysis (PCA, t-SNE, UMAP, PyMDE).
	- Final train/test export and label mapping.

- `model/logistic_regression.ipynb`
	- HOG feature extraction.
	- Standardization and anti-leakage preprocessing.
	- Multinomial logistic regression (cuML).
	- Optuna hyperparameter optimization.

- `model/svm.ipynb`
	- StandardScaler + PCA preprocessing.
	- cuML SVC (RBF kernel).
	- Optuna tuning ($C$, $\gamma$).
	- Stability checks and ablation analysis.

- `model/random-forest.ipynb`
	- Random Forest pipeline with sanity checks.
	- Optuna search (TPE + MedianPruner).
	- 5-seed stability evaluation.
	- Final report with quantitative and qualitative diagnostics.

- `model/mlp.ipynb`
	- PyTorch MLP baseline.
	- Stratified split + standard scaling.
	- Optuna tuning and convergence/stability analysis.
	- Final hold-out test evaluation.

## Requirements

This project is notebook-based. Use Python 3.10+ (3.11 recommended).

### cuML / RAPIDS Environment Requirement (Important)

Several model notebooks use `cuml` (`model/logistic_regression.ipynb`, `model/svm.ipynb`, and parts of `model/random-forest.ipynb`).

- `cuml` is a RAPIDS GPU library and is generally expected to run in a Linux-based CUDA environment.
- The easiest way to run these GPU cells is on Kaggle (Linux) or another Linux machine/container with a compatible NVIDIA CUDA stack.
- On Windows, these `cuml` cells typically do not run natively. Use Kaggle/Linux, WSL2 with a supported CUDA setup.

Core dependencies:

- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `optuna`

Additional dependencies used by specific notebooks:

- `torch` (MLP notebook)
- `scikit-image` (HOG features)
- `joblib` (parallel HOG extraction)
- `umap-learn` and `pymde` (EDA notebook)
- `plotly` and `kaleido` (Random Forest diagnostics)

GPU acceleration dependencies (used in several model notebooks):

- `cuml`
- `cudf`
- `cupy`

## Setup

1. Create and activate a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Open the notebooks in VS Code or Jupyter.

Example (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Note: `requirements.txt` covers Python packages needed by the notebooks in a standard environment. RAPIDS libraries (`cuml`, `cudf`, `cupy`) are intentionally not pinned there because they are environment-specific and typically installed separately in Linux/CUDA setups (for example, Kaggle).

## How To Run

Suggested execution order:

1. `eda.ipynb`
2. Any notebook in `model/` depending on your experiment target.

Inside each model notebook, run cells from top to bottom.

## Data Format

- `fashion_mnist_train_60k.csv` and `fashion_mnist_test_10k.csv`
	- One row per image.
	- `label` column + pixel columns.
- `labels.csv`
	- Class ID to class name mapping.

## Reproducibility Notes

- Most notebooks use fixed random seeds (for example, `42`).
- Validation strategies include stratified splits and repeated multi-seed evaluation.
- Final test evaluation is treated as hold-out reporting in the modeling notebooks.

## Important Path Note

Some notebook cells reference Kaggle-style dataset paths (for example, `/kaggle/input/...`).
When running locally, replace those paths with local paths under `data/`.

The `model/random-forest.ipynb` notebook includes automatic data directory detection and is more portable by default.