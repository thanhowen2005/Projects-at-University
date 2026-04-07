# Adult Census Income Analysis Project

## 1. Project Overview

This project analyzes the **1994 U.S. Census (Adult) dataset** to identify key drivers of income. Beyond standard prediction (`<=50K` vs `>50K`), we investigate deeper socioeconomic patterns—specifically how **passive income, marriage, education, and immigrant status** impact financial success.

**Key Objectives:**

- Perform exploratory data analysis (EDA)
- Test hypotheses related to social and economic assumptions.
- Build predictive models to classify income levels.

## 2. Team Information

**University:** University of Science, VNU-HCM
**Course:** CSC17104 - PROGRAMING FOR DATA SCIENCE

| Student ID | Full Name         |
| ---------- | ----------------- |
| 23127118   | Lê Nguyên Thảo    |
| 23127447   | Nguyễn Thanh Owen |
| 23127464   | Trần Minh Quang   |

## 3. Dataset Description

- **Source:** [Kaggle - Adult Dataset](https://www.kaggle.com/datasets/uciml/adult-census-income)
- **Description:** This data was extracted from the 1994 Census bureau database by Ronny Kohavi and Barry Becker (Data Mining and Visualization, Silicon Graphics). A set of reasonably clean records was extracted using the following conditions: ((AAGE>16) && (AGI>100) && (AFNLWGT>1) && (HRSWK>0)). The prediction task is to determine whether a person makes over $50K a year.

- **Size:** ~32,561 records.
- **Features:**

  `age`: continuous.

  `workclass`: Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.

  `fnlwgt`: final weight, continuous.

  `education`: Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool.

  `education-num`: continuous.

  `marital-status`: Represents the responding unit’s role in the family. Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.

  `occupation`: Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.

  `relationship`: Represents the responding unit’s role in the family. Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.

  `race`: White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.

  `sex`: Female, Male.

  `capital-gain`: income from investment sources, apart from wages/salary, continuous.

  `capital-loss`: losses from investment sources, apart from wages/salary, continuous.

  `hours-per-week`: continuous.

  `native-country`: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.

- **Target:** `income` (Binary classification: `<=50K` vs `>50K`).

## 4. Research Questions

We formulated 6 key questions to guide our analysis, split into three specific notebooks:

- **Q1:** To what extent does the income-prediction model rely on passive income features (Capital Gain/Loss) compared with active income derived from labor? Specifically, if we completely remove investment-related attributes, by how much will the Random Forest model’s ability to detect high-income individuals (Recall for the >50K class) decline?

- **Q2:** Does the raw survey data accurately reflect the likelihood of being wealthy for specific demographic groups? Specifically, if we correct for sampling bias using population weights (`fnlwgt`), do minority groups turn out to be richer or poorer than the raw sample suggests?

- **Q3:** Is the strong correlation between _Marital Status (Married)_ and _High Income (>50K)_ causal, or is it explained by _Age_?

- **Q4:** Does the current 'Education' ranking really show who earns more? Or will using 'Weight of Evidence' (WoE) reveal that some degrees are valued incorrectly (like Vocational School vs. Unfinished College)?

- **Q5:** Does national origin significantly determine income potential in the 1994 US census? Specifically, if we move beyond geographical boundaries and group countries based on economic performance, can we identify a 'High-Success' immigrant class that statistically outperforms US-natives?

- **Q6:** Is the relationship between 'Hours-per-week' and high-income probability linear, or does a 'diminishing returns' pattern emerge when working excessive hours?

## 5. Key Findings Summary

Based on our statistical analysis and modeling, here are the major insights:

- **Passive Income Matters:** Models rely heavily on Capital Gain/Loss to identify the "ultra-wealthy." Removing these features significantly drops the Recall for the >50K class.
- **Marriage > Age:** Marriage is a strong independent predictor of wealth. Even when controlling for age, married individuals consistently earn more than their unmarried peers.
- **The Bachelor Threshold:** Education has a non-linear effect. The "Bachelor's Degree" is the critical tipping point where the odds of earning >50K flip from negative to positive.
- **Immigrant Success:** Contrary to common belief, immigrants from "High-Success" regions (e.g., India, Taiwan, France) statistically outperform native-born Americans in income probability.
- **Bias Check:** The dataset is largely representative, though some minority groups (e.g., Amer-Indian-Eskimo Females) are slightly under-represented.
- **Diminishing Returns on Work Hours:** While working longer hours generally increases income probability, the benefit plateaus after ~60 hours/week. Extremely high working hours often indicate a "Survival Strategy" (low-wage workers working multiple jobs) rather than high-value productivity.

## 6. Project Structure

```text
├── data/                           # Contains dataset files
│   ├── adult.csv                   # Original raw data
│   ├── train.csv                   # Processed training set
│   └── test.csv                    # Processed testing set
├── notebooks/                      # Jupyter Notebooks for analysis
│   ├── data_exploration.ipynb      # EDA and preprocessing
│   ├── project_reflection.ipynb    # Personal reports
│   ├── question12.ipynb            # Analysis for Q1 & Q2
│   ├── question34.ipynb            # Analysis for Q3 & Q4
│   └── question56.ipynb            # Analysis for Q5 & Q6
├── README.md                       # Project documentation
└── requirements.txt                # List of dependencies
```

**File Organization Details:**

- **`data/`**: We separated the raw data (`adult.csv`) from the processed datasets (`train.csv`, `test.csv`) to ensure reproducibility.
- **`notebooks/`**: The analysis is modularized. `data_exploration.ipynb` handles the initial EDA. Specific research questions are grouped into separate notebooks (`question_*.ipynb`) to keep the logic focused and readable.

## 7. Dependencies

To reproduce the analysis, you need **Python 3.8+** and **Jupyter Notebook**. The project relies on the following key libraries:

### 7.1. Data Manipulation & Analysis

- **pandas** (`pd`): Core library for DataFrame manipulation, handling missing values (`Unknown`/`NaN`), and group-by aggregations.
- **numpy** (`np`): Used for numerical operations and array handling.

### 7.2. Visualization

- **matplotlib.pyplot** (`plt`): Base library for creating static charts (bar charts, histograms).
- **seaborn** (`sns`): High-level interface for drawing attractive statistical graphics (heatmap, count plots).

### 7.3. Statistical Analysis

- **scipy.stats**: Used for hypothesis testing, specifically:
  - `chi2_contingency`: For Chi-Square tests to determine relationships between categorical variables (e.g., Marriage vs. Income).
  - `ttest_ind`: For T-tests (if comparing means).

### 7.4. Machine Learning (scikit-learn)

- **sklearn.model_selection**: `train_test_split`, `cross_val_score` (for validating models).
- **sklearn.preprocessing**: `OneHotEncoder`, `StandardScaler`, `LabelEncoder` (for transforming data).
- **sklearn.ensemble**: `RandomForestClassifier` (Primary model for feature importance).
- **sklearn.linear_model**: `LogisticRegression` (Baseline model).
- **sklearn.metrics**: `accuracy_score`, `recall_score`, `confusion_matrix`, `classification_report`.

## 8. How to Run

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/thanhowen2005/CSC17104_DSProgramming_FinalProject.git
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd CSC17104_DSProgramming_FinalProject
    ```

3.  **Create a virtual environment (`venv`):**

    ```bash
    # Windows
    python -m venv venv
    ```

4.  **Activate the environment:**

    ```bash
    # Windows
    venv\Scripts\activate
    ```

    You should see `(venv)` in your terminal prompt

5.  **Install dependencies and setup Kernel:**
    Since `requirements.txt` contains standard libraries

    ```bash,
    # Install project dependencies
    pip install -r requirements.txt
    ```

6.  **Launch Jupyter Notebook:**

    ```bash
    jupyter notebook
    ```

    After Jupyter opens in your browser, navigate to the `notebooks/` folder and open the desired notebook (e.g., `question56.ipynb`) to run the analysis.
