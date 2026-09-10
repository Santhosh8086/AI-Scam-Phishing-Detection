import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report


# 1. Load dataset
data = pd.read_csv("dataset/messages.csv")

print("Dataset loaded successfully!")
print(data)


# 2. Separate input and output
X = data["message"]
y = data["label"]


# 3. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# 4. Create AI/ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )),
    ("classifier", LogisticRegression(
        max_iter=1000
    ))
])


# 5. Train model
model.fit(X_train, y_train)

print("\nModel training completed!")


# 6. Test model
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# 7. Save trained model
joblib.dump(model, "model/scam_phishing_model.pkl")

print("\nModel saved successfully!")
print("File: model/scam_phishing_model.pkl")