import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# ==========================================
# LOAD DATASET
# ==========================================

data = pd.read_csv("datasets/messages_review2_diverse_390.csv")

X = data["message"].astype(str)
y = data["label"]

print("Total messages:", len(data))
print("\nClass Distribution:")
print(y.value_counts())

# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ==========================================
# TF-IDF + LOGISTIC REGRESSION
# ==========================================

pipeline = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            ngram_range=(1, 2),
            lowercase=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])

# ==========================================
# 5-FOLD CROSS VALIDATION
# ==========================================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

cv_scores = cross_val_score(
    pipeline,
    X_train,
    y_train,
    cv=cv,
    scoring="accuracy"
)

print("\n======================================")
print("5-FOLD CROSS VALIDATION")
print("======================================")

print("CV Scores:", cv_scores)
print("Mean CV Accuracy:", cv_scores.mean())

# ==========================================
# TRAIN MODEL
# ==========================================

pipeline.fit(X_train, y_train)

# ==========================================
# TEST MODEL
# ==========================================

y_pred = pipeline.predict(X_test)

print("\n======================================")
print("CONFUSION MATRIX")
print("======================================")

print(
    confusion_matrix(
        y_test,
        y_pred,
        labels=["phishing", "safe", "scam"]
    )
)

# ==========================================
# ACCURACY
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)

# ==========================================
# CLASSIFICATION REPORT
# ==========================================

print("\n======================================")
print("CLASSIFICATION REPORT")
print("======================================")

print(
    classification_report(
        y_test,
        y_pred
    )
)

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    pipeline,
    "model/scam_phishing_model.pkl"
)

print("\n======================================")
print("MODEL TRAINING COMPLETED")
print("======================================")

print("Model saved successfully!")
print("File: model/scam_phishing_model.pkl")