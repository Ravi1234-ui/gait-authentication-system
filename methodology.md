# Methodology

## 1. Problem Definition

The objective of this project is to design a **contactless employee authentication system** based on **gait analysis**. The system aims to identify employees using their walking patterns captured through smartphone accelerometer and gyroscope sensors.

This is treated as a **multi-class classification problem**, where each enrolled employee represents one class. The system must also be capable of rejecting users who are not enrolled.

---

## 2. Data Collection Strategy

### 2.1 Sensor Selection

Two smartphone sensors were used:
- Accelerometer (linear motion)
- Gyroscope (rotational motion)

These sensors were selected because:
- they are available on all modern smartphones
- they capture complementary motion characteristics
- they are commonly used in gait analysis research

### 2.2 Data Format

For each individual, sensor data is stored in CSV format:

```
time, x, y, z
```

Separate files are maintained for:
- `acc.csv` (accelerometer)
- `gyro.csv` (gyroscope)

Each person’s data is stored in a separate folder to maintain clear identity separation during training.

---

## 3. Preprocessing

Raw sensor data is noisy and cannot be used directly for modeling. The following preprocessing steps were applied.

### 3.1 Noise Filtering

A low-pass Butterworth filter was applied to remove high-frequency noise caused by:
- hand movement
- sensor jitter
- environmental disturbances

### 3.2 Gravity Removal

Accelerometer signals contain both body motion and gravity components.  
To isolate body movement:
- a low-frequency filter was used to estimate gravity
- the gravity component was subtracted from the raw signal

This step improves gait pattern consistency.

### 3.3 Windowing

Continuous sensor data was segmented into fixed-length windows:
- Window size: 2.56 seconds (128 samples at ~50 Hz)
- Overlap: 50%

This approach captures complete gait cycles while increasing the number of training samples.

---

## 4. Feature Engineering

Instead of using raw signals directly, statistical features were extracted from each window.

### 4.1 Extracted Features

For each axis (x, y, z) of both accelerometer and gyroscope, the following features were computed:
- Mean
- Standard deviation
- Minimum value
- Maximum value
- Signal energy
- Entropy

This results in a fixed-length feature vector that represents the motion characteristics of a gait window.

### 4.2 Feature Vector Construction

Features from all axes and sensors are concatenated to form the final feature vector.  
This ensures that both linear and rotational gait dynamics are captured.

---

## 5. Dataset Construction

- Each windowed feature vector is labeled with the corresponding employee ID
- Data from all enrolled employees is combined to form the final dataset
- Users in the `unknown` category are excluded from training and used only for testing

This ensures a clear separation between training and authentication scenarios.

---

## 6. Model Selection

A **Random Forest classifier** was selected for this project due to:
- robustness to noise
- ability to handle non-linear patterns
- good performance on small to medium-sized datasets
- minimal preprocessing requirements

Random Forests also provide stable performance without extensive hyperparameter tuning.

---

## 7. Model Training and Evaluation

### 7.1 Training

The model was trained using feature vectors extracted from real-world data collected from enrolled employees.

### 7.2 Evaluation

Model performance was evaluated using **stratified cross-validation** to ensure:
- balanced representation of all employees
- reliable estimation of identification accuracy

Accuracy was chosen as the primary evaluation metric since the task involves correct identity classification among known users.

---

## 8. Authentication Logic

During authentication:
1. Sensor data is collected from the user
2. The same preprocessing and feature extraction pipeline is applied
3. The trained model predicts the most likely employee identity
4. A confidence score is computed for each prediction

A confidence threshold is applied:
- If confidence ≥ threshold → Access Granted
- If confidence < threshold → Access Denied

This mechanism enables rejection of unknown or unenrolled users.

---

## 9. LLM-Based Explainability Layer

A Large Language Model (LLM) was integrated as an **explainability component**.

### 9.1 Purpose

The LLM converts numerical outputs such as confidence scores and access decisions into clear, human-readable explanations.

### 9.2 Design Constraints

The LLM:
- operates only after the ML decision is made
- does not access raw sensor data
- does not modify predictions or thresholds

This separation ensures reliability and prevents unintended influence on security decisions.

---

## 10. Model Retraining and Enrollment

Since gait-based identification is a closed-set problem:
- new employees must be enrolled explicitly
- their data is added to the dataset
- the model is retrained to include the new identity

This retraining process ensures that the system remains accurate as the employee set evolves.

---

## 11. Limitations

- The system requires retraining when new employees are added
- Performance may vary with phone placement and walking speed
- The dataset size is limited by data collection constraints

These limitations are acknowledged and provide directions for future improvement.

---

## 12. Summary

This methodology outlines a complete pipeline for gait-based employee authentication using real-world sensor data. The approach combines robust signal processing, classical machine learning, and LLM-based explainability to create a system that is both technically effective and practically interpretable.
