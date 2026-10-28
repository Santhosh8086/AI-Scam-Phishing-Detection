import unittest

from app import app, keyword_analysis, analyze_url


class TestScamPhishingDetector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    # -----------------------------
    # Home Page Test
    # -----------------------------
    def test_home_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    # -----------------------------
    # Scam Message Test
    # -----------------------------
    def test_scam_message(self):
        response = self.client.post(
            "/predict",
            json={
                "message": "Congratulations! You won Rs 50000. Claim your prize now."
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["prediction"], "scam")
        self.assertEqual(data["risk_level"], "HIGH RISK")
        self.assertGreaterEqual(data["risk_score"], 70)

    # -----------------------------
    # Phishing Message Test
    # -----------------------------
    def test_phishing_message(self):
        response = self.client.post(
            "/predict",
            json={
                "message": "Your bank account is blocked. Verify your password immediately."
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["prediction"], "phishing")
        self.assertEqual(data["risk_level"], "HIGH RISK")
        self.assertGreaterEqual(data["risk_score"], 70)

    # -----------------------------
    # Empty Message Test
    # -----------------------------
    def test_empty_message(self):
        response = self.client.post(
            "/predict",
            json={"message": ""}
        )

        self.assertEqual(response.status_code, 400)

        data = response.get_json()

        self.assertIn("error", data)

    # -----------------------------
    # Missing Message Test
    # -----------------------------
    def test_missing_message(self):
        response = self.client.post(
            "/predict",
            json={}
        )

        self.assertEqual(response.status_code, 400)

        data = response.get_json()

        self.assertIn("error", data)

    # -----------------------------
    # Invalid JSON Test
    # -----------------------------
    def test_invalid_json(self):
        response = self.client.post(
            "/predict",
            data="This is not JSON",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

        data = response.get_json()

        self.assertIn("error", data)

    # -----------------------------
    # Invalid Message Type Test
    # -----------------------------
    def test_invalid_message_type(self):
        response = self.client.post(
            "/predict",
            json={"message": 12345}
        )

        self.assertEqual(response.status_code, 400)

        data = response.get_json()

        self.assertIn("error", data)

    # -----------------------------
    # No URL Test
    # -----------------------------
    def test_no_url(self):
        result = analyze_url(
            "Hello, please attend the meeting tomorrow."
        )

        self.assertFalse(result["detected"])

    # -----------------------------
    # Suspicious URL Test
    # -----------------------------
    def test_suspicious_url(self):
        result = analyze_url(
            "Verify your account at https://example.com/login"
        )

        self.assertTrue(result["detected"])
        self.assertEqual(result["status"], "Suspicious")

    # -----------------------------
    # Scam Keyword Test
    # -----------------------------
    def test_scam_keywords(self):
        scam, phishing = keyword_analysis(
            "Congratulations! You won a prize. Claim your reward now."
        )

        self.assertTrue(len(scam) > 0)

    # -----------------------------
    # Phishing Keyword Test
    # -----------------------------
    def test_phishing_keywords(self):
        scam, phishing = keyword_analysis(
            "Verify your bank account and OTP immediately."
        )

        self.assertTrue(len(phishing) > 0)


if __name__ == "__main__":
    unittest.main()