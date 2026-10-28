# AI-Based Scam Message and Phishing Detection System

## 📌 Project Overview

The **AI-Based Scam Message and Phishing Detection System** is a machine-learning-based web application designed to identify suspicious messages and classify them as:

- Scam
- Phishing
- Safe

The system combines **Machine Learning, keyword analysis, URL analysis, and risk scoring** to provide a simple and understandable security assessment.

---

## 🎯 Objectives

The main objectives of this project are:

1. Detect scam and phishing messages using Machine Learning.
2. Identify suspicious keywords in messages.
3. Detect URLs present in messages.
4. Identify suspicious URL patterns.
5. Calculate an overall risk score.
6. Display the result through a simple web interface.
7. Validate application functionality using automated unit tests.
8. Handle invalid inputs and unexpected errors safely.

---

## 🏗️ System Architecture

The system follows this workflow:

```text
User Message
     ↓
Flask Web Application
     ↓
Input Validation
     ↓
TF-IDF + Logistic Regression Model
     ↓
Keyword Analysis
     ↓
URL Analysis
     ↓
Risk Score Calculation
     ↓
Risk Level
     ↓
Result Display