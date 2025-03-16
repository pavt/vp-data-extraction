# Predicting Vulnerability-Proneness in GitHub Actions using Contextual Metadata**  

## 📌 **Overview**  
This repository provides a **complete pipeline for extracting, processing, and modeling the vulnerability-proneness of GitHub Actions** based on contextual metadata from GitHub repositories. The project directly addresses **RQ3** from the study *Shadows on the Spotless Workflow: The Vulnerability Proneness of GitHub Actions*, investigating how repository-level metadata (e.g., repository activity, contributor engagement, and update frequency) can predict security risks in third-party Actions.  

## 🚀 **Pipeline Overview**  
The project follows a structured pipeline to **predict the vulnerability-proneness of GitHub Actions** using multiple data processing steps:

### **1️⃣ Data Extraction & Processing (`src/`)**  
- Extracts repository metadata from GitHub API (`github_api.py`).  
- Cleans and structures raw repository data (`data_manager.py`).  
- Computes various repository metrics (`repo_metrics.py`).  
- Processes dependencies and security indicators (`dependency_analyzer.py`).  
- Generates the **layered datasets (`datos_capa_0.csv` to `datos_capa_7.csv`)**.  

### **2️⃣ Feature Engineering & Model Training (`docs/experimental_setup/`)**  
- **Feature selection & transformation** (`02_feature_engineering.ipynb`).  
- **Training machine learning models** to predict vulnerability-proneness (`03_model_training.ipynb`).  
- Evaluates model performance using **Random Forest, XGBoost**, and other classifiers.  

## 🔧 **Installation & Usage**
### **1️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

### **2️⃣ Run the data processing pipeline**
```bash
python main.py
```
This will **extract repository metadata, process dependencies, and generate all processed datasets** in `data/processed/`.  

### **3️⃣ View Results**  
- All outputs from the pipeline, including processed datasets and model evaluation metrics, are stored as **text and CSV files**.  
- The final results can be found in **`docs/experimental_setup/datasets/`**, including:  
  - **Processed datasets** (`final_cv_results.csv`, `final_xgb_results.csv`).  
  - **Model performance metrics** (`final_cv_results_all_metrics.csv`).  
  - **Trained machine learning models** (`RandomForest.joblib`, `XGBoost.joblib`).  

### **4️⃣ Optional: Run the Notebooks for Further Analysis**  
If you want to explore or modify the feature engineering and modeling steps, navigate to `docs/experimental_setup/` and execute:  
```bash
jupyter notebook
```
Then open and run the following:  
- `02_feature_engineering.ipynb` (Feature Engineering)  
- `03_model_training.ipynb` (Model Training & Evaluation)  

While **running the notebooks is optional**, they allow you to inspect and modify the **feature engineering and model training process**.  

## 📊 **Experiment & Results**
- The experiment evaluates **how well contextual metadata predicts vulnerability risks**.  
- Trained models are stored in **`docs/experimental_setup/models/`** (Random Forest, XGBoost, etc.).  
- Key results and performance comparisons are available in **CSV and text format**.  

---

## 📂 **Repository Structure**
```
pavt-vp-data-extraction/
├── main.py                        # Entry point for data extraction & processing
├── requirements.txt               # Project dependencies
├── data/
│   ├── raw/                       # Raw repository data
│   │   ├── repositories_raw_data.csv
│   │   ├── repositories_raw_data_test.csv
│   ├── processed/                  # Processed datasets by layers
│   │   ├── datos_capa_0.csv
│   │   ├── ...
│   │   ├── datos_capa_7.csv
├── docs/                          # Documentation & experiment results
│   ├── README.md
│   ├── rq3-approach.md             # Methodology for RQ3
│   ├── vp-distribution.ipynb       # Vulnerability-proneness analysis
│   ├── experimental_setup/         # ML model training & evaluation
│   │   ├── 01_data_preprocessing.ipynb
│   │   ├── 02_feature_engineering.ipynb
│   │   ├── 03_model_training.ipynb
│   │   ├── datasets/               # Processed datasets & trained models
│   │   │   ├── final_cv_results.csv
│   │   │   ├── final_xgb_results.csv
│   │   │   ├── RandomForest.joblib
│   │   │   ├── XGBoost.joblib
├── src/                           # Source code for data extraction & processing
│   ├── core/                      # Core pipeline components
│   │   ├── pipeline_manager.py
│   │   ├── github_api.py
│   ├── processing/                 # Data processing & dependency analysis
│   │   ├── dependency_analyzer.py
│   │   ├── language_processor.py
│   │   ├── pipeline_steps/
│   │   │   ├── feature_engineering_step.py
│   ├── utils/                      # Utility scripts
│   │   ├── repo_metrics.py
│   │   ├── transform_data.py
```

This repository provides a **complete framework for predicting the vulnerability-proneness of GitHub Actions using contextual metadata**, supporting the findings of *Shadows on the Spotless Workflow: The Vulnerability Proneness of GitHub Actions*.