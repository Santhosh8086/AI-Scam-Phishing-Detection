from flask import Flask, render_template, request, jsonify
import joblib
import re

app = Flask(__name__)

# -----------------------------
# Load Machine Learning Model
# -----------------------------
model = None
model_load_error = None

try:
    model = joblib.load("model/scam_phishing_model.pkl")
except Exception as e:
    model_load_error = str(e)


# -----------------------------
# URL Analysis
# -----------------------------
def analyze_url(message):
    url_pattern = r"https?://\S+|www\.\S+"
    urls = re.findall(url_pattern, message)

    if not urls:
        return {
            "detected": False,
            "message": "No URL detected."
        }

    suspicious_words = [
        "login", "verify", "secure", "update",
        "account", "bank", "claim", "reward", "free"
    ]

    suspicious = False

    for url in urls:
        url_lower = url.lower()

        for word in suspicious_words:
            if word in url_lower:
                suspicious = True
                break

        if suspicious:
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


# -----------------------------
# Keyword Analysis
# -----------------------------
def keyword_analysis(message):

    scam_keywords = [
        "won", "winner", "prize", "reward", "lottery",
        "cashback", "free gift", "claim", "investment",
        "profit", "loan", "urgent payment"
    ]

    phishing_keywords = [
        "verify", "verification", "kyc", "password", "otp",
        "bank account", "card details", "login", "suspended",
        "blocked", "account security", "upi pin"
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


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Prediction API
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    # Check whether model loaded successfully
    if model is None:
        return jsonify({
            "error": "Machine learning model could not be loaded.",
            "details": model_load_error
        }), 503

    try:

        # Safely read JSON request
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({
                "error": "Invalid or missing JSON data."
            }), 400

        # Check message field
        message = data.get("message")

        if message is None:
            return jsonify({
                "error": "Message field is required."
            }), 400

        # Check message type
        if not isinstance(message, str):
            return jsonify({
                "error": "Message must be a text value."
            }), 400

        message = message.strip()

        # Check empty message
        if not message:
            return jsonify({
                "error": "Please enter a message."
            }), 400

        # -----------------------------
        # Machine Learning Prediction
        # -----------------------------
        prediction = model.predict([message])[0]

        # -----------------------------
        # Additional Analysis
        # -----------------------------
        scam_matches, phishing_matches = keyword_analysis(message)

        url_result = analyze_url(message)

        # -----------------------------
        # Risk Score Calculation
        # -----------------------------
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

        # -----------------------------
        # Risk Level
        # -----------------------------
        if risk_score >= 70:
            risk_level = "HIGH RISK"

        elif risk_score >= 40:
            risk_level = "MEDIUM RISK"

        else:
            risk_level = "LOW RISK"

        # -----------------------------
        # Generate Reasons
        # -----------------------------
        reasons = []

        if prediction == "scam":
            reasons.append(
                "Machine learning model detected scam-like content."
            )

        elif prediction == "phishing":
            reasons.append(
                "Machine learning model detected phishing-like content."
            )

        else:
            reasons.append(
                "Machine learning model classified the message as safe."
            )

        if scam_matches:
            reasons.append(
                "Scam keywords detected: "
                + ", ".join(scam_matches)
            )

        if phishing_matches:
            reasons.append(
                "Phishing keywords detected: "
                + ", ".join(phishing_matches)
            )

        if url_result["detected"]:
            reasons.append(url_result["message"])

        # -----------------------------
        # Successful Response
        # -----------------------------
        return jsonify({
            "prediction": prediction,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "reason": " ".join(reasons),
            "url_analysis": url_result,
            "message": message
        }), 200

    except Exception as e:

        # Unexpected error handling
        return jsonify({
            "error": "An unexpected error occurred while analyzing the message.",
            "details": str(e)
        }), 500


# -----------------------------
# Global Error Handlers
# -----------------------------
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "error": "Bad request.",
        "message": "Please check the submitted data."
    }), 400


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "error": "Page not found.",
        "message": "The requested endpoint does not exist."
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "error": "Internal server error.",
        "message": "Something went wrong on the server."
    }), 500


# -----------------------------
# Run Flask Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)