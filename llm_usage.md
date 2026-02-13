# LLM Usage in the Project

## Overview

This project is primarily a **sensor-based machine learning system** for contactless employee authentication using gait analysis. The core functionality of identifying employees is handled entirely by a traditional machine learning model trained on real-world accelerometer and gyroscope data.

A Large Language Model (LLM) has been integrated only as a **supporting component** to improve the clarity and interpretability of system outputs. The LLM does not participate in the core prediction or decision-making process.

---

## Why an LLM Is Used

The machine learning model produces numerical outputs such as:
- predicted employee ID
- confidence score
- access granted or denied decision

While these outputs are suitable for machines, they are not easily understandable by non-technical users such as security staff or reviewers. The LLM is used to convert these numerical results into **clear, human-readable explanations**.

The goal is to make the system easier to interpret and audit, not to increase prediction accuracy.

---

## How the LLM Is Used

The LLM is used only **after** the machine learning model has completed its work.

### The process is as follows:

1. The ML model predicts the employee identity or rejects the user.
2. A confidence score is calculated based on gait similarity.
3. A final access decision is made using a predefined threshold.
4. A short, structured summary of this decision is created.
5. This summary is passed to the LLM.
6. The LLM generates a textual explanation describing why access was granted or denied.

At no point does the LLM influence or modify the ML output.

---

## Information Provided to the LLM

The LLM only receives high-level decision information, such as:
- final access decision
- predicted employee (if any)
- confidence score
- confidence threshold

Raw sensor data, extracted features, or any personally identifiable information are **never** shared with the LLM.

This design helps maintain privacy and avoids unnecessary complexity.

---

## What the LLM Does NOT Do

To keep the system reliable and secure, the LLM is explicitly not used for:

- training the gait recognition model
- predicting employee identity
- processing accelerometer or gyroscope signals
- adjusting confidence thresholds
- making or overriding access control decisions

All biometric decisions are made exclusively by the trained machine learning model.

---

## Validation and Reliability

The LLM output is validated by checking that:
- the explanation matches the actual ML decision
- no new or fabricated information is introduced
- access-granted explanations are only generated when access is actually granted

If an explanation does not align with the ML decision, the system always prioritizes the machine learning result.

---

## Design Rationale

This separation between machine learning and LLM functionality was chosen to ensure:
- clear responsibility boundaries
- easier debugging and testing
- better transparency for audits
- reduced risk of incorrect or misleading explanations

The LLM can be replaced, modified, or removed without affecting the core authentication system.

---

## Summary

In this project, the LLM acts as an **explainability layer** rather than an intelligence layer. The machine learning model performs all gait-based identification tasks, while the LLM helps present the results in a form that is easier for humans to understand.

This approach aligns with real-world practices where interpretability and trust are as important as model accuracy.
