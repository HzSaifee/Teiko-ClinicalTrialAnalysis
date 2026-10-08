# Loblaw Bio: Clinical Trial Analysis

This repository contains a complete data pipeline, statistical analysis suite, and interactive web dashboard designed to evaluate immune cell populations for Loblaw Bio's clinical trials. 

## Reproducibility & Execution

This project is configured for automated execution via GitHub Codespaces using the included `Makefile`. To reproduce the analysis and view the dashboard, execute the following commands in the terminal sequentially:

### 1. Install Dependencies
```bash
make setup
```

*Installs required packages (`pandas`, `scipy`, `streamlit`, `jupyter`, `plotly`) from `requirements.txt`.*

### 2. Run the Data Pipeline

```bash
make pipeline
```

*Executes `load_data.py`. This script parses the raw `cell-count.csv`, normalizes the data into a two-table relational schema (`samples` metadata and `cell_counts` long-format measurements), and initializes the `cell-count.db` SQLite database.*

### 3. Launch the Dashboard

```bash
make dashboard
```

*Starts the interactive Streamlit dashboard. If executing within GitHub Codespaces, a notification will appear in the bottom-right corner prompting you to "Open in Browser". The dashboard is served locally at `http://localhost:8501`.*

## Project Structure

* **`load_data.py`**: The primary ETL script that handles database generation and schema normalization.
* **`dashboard.py`**: The Streamlit web application. It connects to the SQLite database to perform live calculations, render Plotly boxplots, and compute Mann-Whitney U tests for statistical significance between responder groups.
* **`analysis_notebook.ipynb`**: An exploratory Jupyter Notebook containing the initial data wrangling, ad-hoc queries, and proof-of-logic for the statistical testing.
* **`Makefile`**: Contains the `setup`, `pipeline`, and `dashboard` targets required for automated grading.
* **`requirements.txt`**: Environment dependencies.
* **`cell-count.csv`**: The raw data file (expected in the root directory).
