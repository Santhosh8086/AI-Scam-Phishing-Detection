from flask import Flask, render_template, request, jsonify
import joblib
import re

app = Flask(__name__)

# Load trained ML model
model = joblib.load("model/scam_phishing_model.pkl")


# ==========================================
# URL ANALYSIS
# ==========================================

def analyze_url(message):

    url_pattern = r"https?://\S+|www\.\S+"
    urls = re.findall(url_pattern, message)

    if not urls:
        return {
            "detected": False,
            "message": "No URL detected."
        }

    suspicious_words = [
        "login",
        "verify",
        "secure",
        "update",
        "account",
        "bank",
        "claim",
        "reward",
        "free"
    ]

    suspicious = False

    for url in urls:
        url_lower = url.lower()

        for word in suspicious_words:
            if word in url_lower:
                suspicious = True
                break

    if suspicious:
        return {
            "detected": True,
            "message": "Suspicious URL detected.",
            "urls": urls,
            "status": "Suspicious"
        }

    return {
        "detected": True,
        "message": "URL detected. No obvious suspicious keyword found.",
        "urls": urls,
        "status": "Check Carefully"
    }


# ==========================================
# KEYWORD ANALYSIS
# ==========================================

def keyword_analysis(message):

    scam_keywords = [
        "won",
        "winner",
        "prize",
        "reward",
        "lottery",
        "cashback",
        "free gift",
        "claim",
        "investment",
        "profit",
        "loan",
        "urgent payment"
    ]

    phishing_keywords = [
        "verify",
        "verification",
        "kyc",
        "password",
        "otp",
        "bank account",
        "card details",
        "login",
        "suspended",
        "blocked",
        "account security",
        "upi pin"
    ]

    text = message.lower()

    scam_matches = [
        word for word in scam_keywords
        if word in text
    ]

    phishing_matches = [
        word for word in phishing_keywords
        if word in text
    ]

    return scam_matches, phishing_matches


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# PREDICTION
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Please enter a message."
        })

    # ML prediction
    prediction = model.predict([message])[0]

    # Keyword analysis
    scam_matches, phishing_matches = keyword_analysis(message)

    # URL analysis
    url_result = analyze_url(message)

    # ======================================
    # RISK SCORE
    # ======================================

    risk_score = 0

    if prediction in ["scam", "phishing"]:
        risk_score += 60

    if scam_matches:
        risk_score += 20

    if phishing_matches:
        risk_score += 20

    if url_result["detected"]:
        if url_result.get("status") == "Suspicious":
            risk_score += 20
        else:
            risk_score += 5

    risk_score = min(risk_score, 100)

    # ======================================
    # RISK LEVEL
    # ======================================

    if risk_score >= 70:
        risk_level = "HIGH RISK"
    elif risk_score >= 40:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "LOW RISK"

    # ======================================
    # REASON
    # ======================================

    reasons = []

    if prediction == "scam":
        reasons.append("Machine learning model detected scam-like content.")

    elif prediction == "phishing":
        reasons.append("Machine learning model detected phishing-like content.")

    else:
        reasons.append("Machine learning model classified the message as safe.")

    if scam_matches:
        reasons.append(
            "Scam keywords detected: " +
            ", ".join(scam_matches)
        )

    if phishing_matches:
        reasons.append(
            "Phishing keywords detected: " +
            ", ".join(phishing_matches)
        )

    if url_result["detected"]:
        reasons.append(url_result["message"])

    return jsonify({
        "prediction": prediction,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reason": " ".join(reasons),
        "url_analysis": url_result,
        "message": message
    })


# ==========================================
# RUN FLASK APP
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)