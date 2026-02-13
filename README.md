# Contactless Employee Authentication Using Gait Analysis

## Project Overview

This project implements a **contactless employee authentication system** based on **gait analysis** using data collected from smartphone sensors. The system identifies employees by analyzing their walking patterns using accelerometer and gyroscope signals.

The motivation behind this project is to explore **behavioral biometrics** as an alternative to traditional authentication methods such as ID cards, passwords, or fingerprints. Since gait is difficult to imitate and can be captured without explicit user interaction, it provides a promising approach for continuous and contactless authentication.

---

## Key Objectives

- Build a real-world gait-based identification system using smartphone sensors  
- Train a machine learning model on real-world accelerometer and gyroscope data  
- Identify enrolled employees based on their walking patterns  
- Reject unknown or unenrolled users using confidence-based decision logic  
- Provide human-readable explanations for access decisions using an LLM-based explainability layer  

---

## System Architecture

The system is designed with a clear separation of responsibilities:

1. **Sensor Data Collection**
   - Accelerometer and gyroscope data collected using a smartphone  
   - Data stored in CSV format with time, x, y, and z axes  

2. **Preprocessing and Feature Engineering**
   - Noise filtering and gravity removal  
   - Sliding window segmentation of gait signals  
   - Statistical feature extraction from each window  

3. **Machine Learning Model**
   - Trained on real-world data collected from enrolled employees  
   - Multi-class classification where each class represents one employee  
   - Produces predicted identity and confidence score  

4. **Decision Logic**
   - Confidence-based thresholding  
   - Access granted or denied based on model confidence  

5. **LLM-Based Explainability Layer**
   - Converts numerical decisions into human-readable explanations  
   - Improves interpretability and auditability of the system  

![System Architecture](https://github.com/user-attachments/assets/239db9ad-795b-4673-80dc-be5f012ccc02)

---

## Dataset Description

### Real-World Data

The system is trained primarily on **real-world data** collected from individuals using smartphones.

Each person’s data is stored separately as:

```
data/real_world/raw/person_xx/
├── acc.csv
└── gyro.csv
```

Each CSV file contains:

- time  
- x-axis  
- y-axis  
- z-axis  

An additional `unknown/` folder is used to test authentication for users who are not enrolled in the system.

---

### UCI HAR Dataset (Reference Dataset)

The Human Activity Recognition (HAR) Using Smartphones dataset from the UCI Machine Learning Repository was referenced to understand standard preprocessing techniques and sensor-based activity recognition pipelines.

Dataset details:

- Collected from 30 subjects  
- Smartphone accelerometer and gyroscope sensors  
- Sampling frequency: 50 Hz  
- 3-axial linear acceleration and 3-axial angular velocity  
- Data segmented into fixed-size windows of 2.56 seconds (128 samples) with 50% overlap  

The dataset includes multiple activities; however, for gait-based authentication, only walking-related activities were considered:

- Walking  
- Walking Upstairs  
- Walking Downstairs  

The UCI HAR dataset was used as a reference for understanding windowing strategy, signal processing techniques, and feature extraction methodology.

Official Dataset Link:  
https://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones

---

## Feature Engineering

The raw sensor data is converted into fixed-length feature vectors using the following steps:

- Gravity removal from accelerometer signals  
- Sliding window segmentation (2.56 seconds with overlap)  
- Statistical feature extraction per window, including:
  - Mean  
  - Standard deviation  
  - Minimum and maximum values  
  - Signal energy  
  - Entropy  

Accelerometer and gyroscope features are combined to form the final feature vector used for classification.

---

## Machine Learning Model

- A Random Forest classifier is used for gait-based identification  
- The model is trained only on data from enrolled employees  
- Cross-validation is used to estimate identification accuracy  
- The final trained model is saved and reused for authentication  

When a new employee joins, their data is added to the dataset and the model is retrained to include the new identity.

---

## Authentication Workflow

1. An individual walks while carrying a smartphone  
2. Sensor data is collected and preprocessed  
3. Gait features are extracted  
4. The trained model predicts the most likely employee identity  
5. A confidence score is computed  
6. If confidence exceeds a predefined threshold:
   - Access is granted  
7. Otherwise:
   - Access is denied  

---

## LLM Integration

A Large Language Model (LLM) is integrated as an **explainability layer**, not as a decision-making component.

The LLM:

- Receives a structured summary of the ML decision  
- Generates a clear, human-readable explanation  
- Helps security staff and reviewers understand why access was granted or denied  

The LLM does not:

- Train the model  
- Predict identities  
- Process sensor data  
- Override access decisions  

Further details are documented in `llm_usage.md`.

---

## Project Structure
```
contactless-gait-auth/
├── data/
│ └── real_world/
│ └── raw/
├── models/
│ ├── gait_model.pkl
│ ├── gait_model2.pkl
│ └── label_map_realworld.pkl
├── ml_pipeline.py
├── llm_explainer.py
├── authenticate.py
├── llm_usage.md
├── requirements.txt
└── README.md
```


---

## Results and Evaluation

- The model achieves reliable identification accuracy on enrolled employees using cross-validation  
- Unknown users are effectively rejected using confidence-based thresholds  
- Confidence plots are used to visualize separation between known and unknown users  

---

## Limitations

- The system requires retraining when a new employee is enrolled  
- Performance may vary based on phone placement and walking conditions  
- The dataset size is limited and can be improved with more samples  

---

## Conclusion

This project demonstrates a practical implementation of a gait-based authentication system using real-world sensor data. By combining traditional machine learning with an LLM-based explainability layer, the system achieves both technical effectiveness and interpretability, which are critical for real-world security applications.

---

## Future Work

- Support incremental learning for large-scale deployments  
- Add continuous authentication over longer time periods  
- Improve robustness to different phone placements  
- Integrate a user interface for real-time monitoring  

