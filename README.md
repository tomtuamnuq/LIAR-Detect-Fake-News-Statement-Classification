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
   - Deploy the model as a web service using Flask.
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

3. Activate the Pipenv shell in the project root:
   ```bash
   pipenv shell
   ```

4. Launch the Jupyter Notebook (if needed) with the correct working directory:
   ```bash
   jupyter lab --notebook-dir=notebooks
   ```

5. Execute at least the first cell of the Jupyter Notebook to load the dataset into the `data` directory.
---

### **Training the Model**

To train the model, use the `train.py` script located in the `src` directory. This will preprocess the data, train the model, and save the required pickle files (`feature_engineer.pkl` and `xgboost_model.pkl`) in the `models` directory. Ensure that the `train.tsv` and `test.tsv` files exist in the `data` directory before training!

Run the training script:
```bash
python src/train.py
```

Once complete, the `models/` directory will contain the following:
- `feature_engineer.pkl`: The pickled feature engineering pipeline.
- `xgboost_model.pkl`: The trained XGBoost model.

---

### **Testing the Python implementation**

To test the trained model inference implementation, use `pytest` to run the tests in the `tests` directory. These tests verify model inference, schema validation, and the prediction pipeline.

Run the tests:
```bash
pytest tests
```

Make sure that the trained model files (`feature_engineer.pkl` and `xgboost_model.pkl`) exist in the `models` directory before running the tests.

---
### **Running the Application in a Docker Container**

Follow these steps to build, run, and test the Flask application using Docker:

#### **Step 1: Build the Docker Image**
Ensure you are in the project root directory and run the following command to build the Docker image:
```bash
docker build -t liar-detect-app .
```

#### **Step 2: Run the Docker Container**
Start the container and expose it on port `5042`:
```bash
docker run -p 5042:5042 liar-detect-app
```

The application will now be accessible at `http://127.0.0.1:5042`.

#### **Step 3: Test the Flask API**
You can test the `/predict` endpoint using a test JSON file. For example, to test with `test_single_false.json`, run:
```bash
curl -X POST -H "Content-Type: application/json" -d @tests/test_single_false.json http://127.0.0.1:5042/predict
```

The API should respond with a JSON object containing the predicted label. For example:
```json
{
    "predicted_label": "pants-fire",
    "true_label": "pants-fire",
    "correct": true
}
```
### **Using the AWS CLI for Docker Image Management**

This subsection explains how to set up the AWS CLI on Arch Linux, push the Docker image to Amazon ECR Public, and retrieve the image locally.

#### **Step 1: Install the AWS CLI**
On Arch Linux, you can install the AWS CLI using the `aws-cli` package:
```bash
yay -S aws-cli
```

#### **Step 2: Configure the AWS CLI**
Set up the AWS CLI with your credentials and default region:
```bash
aws configure
```
You will be prompted to enter:
- **AWS Access Key ID**
- **AWS Secret Access Key**

Ensure that your AWS credentials are valid and the required permissions are assigned to your user account for ECR Public operations.

#### **Step 3: Upload the Docker Image**
Use the provided `upload_to_ecr.sh` script to push the Docker image to Amazon ECR Public:
```bash
./upload_to_ecr.sh
```
Ensure that the `upload_to_ecr.sh` script is executable:
```bash
chmod +x upload_to_ecr.sh
```

The image is publicly available and does not require authentication for pulling.

#### **Step 4: Retrieve the Docker Image**
To pull the Docker image from Amazon ECR Public to your local Docker installation, use the following command:
```bash
docker pull public.ecr.aws/t8q6o3x2/tuamnuq-liar-detect-app:latest
```

The image will now be available locally and can be verified using:
```bash
docker images
```

## **Project Structure**

```
LIAR-Detect/
│
├── data/                # Dataset directory
│   ├── train.tsv        # Training data
│   ├── test.tsv         # Test data
│
├── models/              # Model and pipeline directory
│   ├── feature_engineer.pkl
│   ├── xgboost_model.pkl
│
├── notebooks/
│   └── notebook.ipynb   # Main notebook for data preparation, EDA, and model selection
│
├── src/                 # Source code directory
│   ├── common_feature.py # Shared utilities and paths
│   ├── train.py         # Script to train the final model
│   ├── predict.py       # Script to serve predictions via a web service
│
├── tests/               # Test suite directory
│   ├── test_inference.py # Pytest for inference pipeline
│   ├── test_single_false.json  # Test input JSON with false label
│   ├── test_single_mtrue.json  # Test input JSON with mostly-true label
│
├── Dockerfile           # Docker configuration
├── Pipfile              # Dependency management using Pipenv
├── Pipfile.lock         # Lockfile for reproducibility
├── pyproject.toml       # Pytest configuration
├── README.md            # Project documentation
└── .gitignore           # Ignored files and directories
```

---

## **Results**

- **Best Model**: XGBoost
- **Accuracy on Test Data**: 0.4301 (Default Parameters)
- Detailed performance metrics can be found in the project notebook (`notebook.ipynb`).

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.
