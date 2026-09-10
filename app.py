from flask import Flask, render_template, request
import joblib
import re

app = Flask(__name__)

# Load trained AI model
model = joblib.load("model/scam_phishing_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    message = request.form["message"]

    # Convert message to lowercase
    text = message.lower()

    # -----------------------------------
    # 1. AI MODEL PREDICTION
    # -----------------------------------

    prediction = model.predict([message])[0]

    # Start risk score
    risk_score = 0

    # -----------------------------------
    # 2. AI DETECTION
    # -----------------------------------

    if prediction in ["scam", "phishing"]:
        risk_score += 60

    # -----------------------------------
    # 3. SCAM KEYWORD DETECTION
    # -----------------------------------

    scam_keywords = [
        "won",
        "winner",
        "lottery",
        "prize",
        "reward",
        "claim",
        "cash prize",
        "free gift",
        "lucky draw",
        "bonus",
        "selected",
        "voucher"
    ]

    found_scam_words = []

    for word in scam_keywords:
        if word in text:
            found_scam_words.append(word)

    if found_scam_words:
        risk_score += 30

    # -----------------------------------
    # 4. PHISHING KEYWORD DETECTION
    # -----------------------------------

    phishing_keywords = [
        "otp",
        "verify",
        "verification",
        "bank account",
        "account blocked",
        "account suspended",
        "login",
        "password",
        "username",
        "card details",
        "bank details",
        "security alert",
        "update your account",
        "confirm your account"
    ]

    found_phishing_words = []

    for word in phishing_keywords:
        if word in text:
            found_phishing_words.append(word)

    if found_phishing_words:
        risk_score += 30

    # -----------------------------------
    # 5. URL DETECTION
    # -----------------------------------

    url_found = re.search(
        r"https?://\S+|www\.\S+",
        message
    )

    if url_found:

        url = url_found.group()

        suspicious_url_words = [
            "login",
            "verify",
            "update",
            "claim",
            "reward",
            "prize",
            "free",
            "account",
            "secure",
            "bank"
        ]

        found_url_words = []

        for word in suspicious_url_words:

            if word in url.lower():
                found_url_words.append(word)

        if found_url_words:

            risk_score += 30

            url_warning = "🚨 Suspicious URL detected."

            url_reason = (
                "Suspicious keywords found: "
                + ", ".join(found_url_words)
            )

        else:

            risk_score += 10

            url_warning = "⚠️ URL detected."

            url_reason = (
                "A URL was found, but no suspicious "
                "keyword was detected in the URL."
            )

    else:

        url_warning = "✅ No URL detected."

        url_reason = (
            "The message does not contain a URL."
        )

    # -----------------------------------
    # 6. LIMIT SCORE TO 100
    # -----------------------------------

    if risk_score > 100:
        risk_score = 100

    # -----------------------------------
    # 7. FINAL RESULT
    # -----------------------------------

    if risk_score >= 70:

        risk = "HIGH RISK 🔴"

        result = "🚨 SCAM / PHISHING MESSAGE"

        reason = (
            "The message contains multiple suspicious "
            "patterns and may be unsafe."
        )

    elif risk_score >= 40:

        risk = "MEDIUM RISK 🟠"

        result = "⚠️ SUSPICIOUS MESSAGE"

        reason = (
            "The message contains some suspicious "
            "patterns. Please verify before responding."
        )

    else:

        risk = "LOW RISK 🟢"

        result = "✅ SAFE MESSAGE"

        reason = (
            "No major suspicious pattern was detected "
            "in this message."
        )

    # -----------------------------------
    # 8. SEND RESULT TO HTML
    # -----------------------------------

    return render_template(
        "index.html",
        result=result,
        risk=risk,
        risk_score=risk_score,
        reason=reason,
        url_warning=url_warning,
        url_reason=url_reason,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)