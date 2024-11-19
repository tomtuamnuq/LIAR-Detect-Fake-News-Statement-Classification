# LIAR-Detect: Fake News Statement Classification

LIAR-Detect is a machine learning project focused on classifying political statements into categories such as `true`, `false`, `half-true`, and others. Leveraging the LIAR dataset, this project explores text-based fake news detection and provides insights into the credibility of statements made by public figures. The trained model is deployed as a web service, ready for integration into fact-checking workflows or other applications.

---

## **Problem Description**

The proliferation of misinformation and fake news, especially in the political domain, has made it challenging to discern credible statements. This project aims to develop a classification model capable of analyzing short political statements and categorizing them into truthfulness levels.

The dataset, **LIAR**, contains approximately 10,000 labeled statements with metadata such as the speaker, subject, and historical truthfulness records. By combining text analysis with metadata, the project aims to identify misinformation.

---

## **Dataset**

The dataset used for this project is the **LIAR Benchmark Dataset**, introduced in William Yang Wang's paper, _"Liar, Liar Pants on Fire: A New Benchmark Dataset for Fake News Detection."_

**Dataset Features:**

- **Text Data**: Short political statements.
- **Metadata**: Speaker, party affiliation, context, and historical truthfulness records.
- **Labels**: `true`, `mostly-true`, `half-true`, `false`, `barely-true`, and `pants-on-fire`.

Source: [ACL 2017 Paper](https://arxiv.org/abs/1705.00648)

The dataset is automatically downloaded at the start of the Jupyter Notebook.

---

## **Project Workflow**

1. **Data Preparation and Exploratory Data Analysis (EDA)**:

   - Handle missing values.
   - Analyze label and feature distribution as well as statement lengths, topics and important words.
   - Preprocess text data using TF-IDF vectorization and One-Hot encoding.
   - Engineer features from metadata for enhanced model performance.

2. **Model Training and Selection**:

   - Train and evaluate multiple models:
     - Logistic Regression
     - Random Forest Classifier
     - Linear SVM
     - Multinomial Naive Bayes
     - XGBoost
   - Perform hyperparameter tuning using GridSearchCV.
   - Select the best model based on cross-validation accuracy.

3. **Model Evaluation**:

   - Assess performance on the test dataset.
   - Generate classification reports and visualize confusion matrices.

4. **Deployment**:
   - Deploy the model as a web service using Flask (or BentoML).
   - Containerize the service using Docker for portability.
   - Optionally deploy the service to the cloud for public access.

---

## **Setup Instructions**

### **Prerequisites**

- Python 3.12 or higher
- `pipenv` for dependency management
- Docker (optional, for containerization)

### **Installation**

1. Clone the repository:

   ```bash
   git clone git@github.com:tomtuamnuq/LIAR-Detect-Fake-News-Statement-Classification.git
   cd LIAR-Detect-Fake-News-Statement-Classification
   ```

2. Install dependencies using `pipenv`:

   ```bash
   pipenv install
   ```

3. Launch the Jupyter Notebook with the correct working directory:
   ```bash
   pipenv run jupyter lab --notebook-dir=notebooks
   ```

---

## **Project Structure**

```
LIAR-Detect/
│
├── data/                # Auto-downloaded dataset
│
├── notebooks/
│   └── notebook.ipynb  # Main notebook for data preparation, EDA, and model selection
│
├── src/
│   ├── train.py        # Script to train the final model
│   ├── predict.py      # Script to serve predictions via a web service
│
├── Dockerfile          # Docker configuration
├── Pipfile             # Dependency management using Pipenv
├── Pipfile.lock        # Lockfile for reproducibility
├── README.md           # Project documentation
└── .gitignore          # Ignored files and directories

```

---

## **Results**

- **Best Model**: XGBoost
- **Accuracy on Test Data**: 0.4301 (Default Parameters)
- Detailed performance metrics can be found in the project notebook (`notebook.ipynb`).

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.
