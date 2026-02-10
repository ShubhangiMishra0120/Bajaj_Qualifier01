from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

EMAIL = "shubhangi3934.beai23@chitkara.edu.in"


# ---------- Helper Functions ----------
def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)

def lcm(a, b):
    return (a * b) // gcd(a, b)


# ---------- Health API ----------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "is_success": True,
        "official_email": EMAIL
    }), 200


# ---------- Main BFHL API ----------
@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        data = request.get_json()

        # Validation: exactly one key
        if not data or len(data.keys()) != 1:
            return jsonify({
                "is_success": False,
                "error": "Exactly one key is required"
            }), 400

        key = list(data.keys())[0]
        value = data[key]

        # ---------- Fibonacci ----------
        if key == "fibonacci":
            if not isinstance(value, int) or value < 0:
                raise ValueError("Invalid fibonacci input")

            fib = [0, 1]
            for i in range(2, value):
                fib.append(fib[i - 1] + fib[i - 2])

            return jsonify({
                "is_success": True,
                "official_email": EMAIL,
                "data": fib[:value]
            }), 200

        # ---------- Prime ----------
        if key == "prime":
            primes = []
            for n in value:
                if n < 2:
                    continue
                is_prime = True
                for i in range(2, int(n ** 0.5) + 1):
                    if n % i == 0:
                        is_prime = False
                        break
                if is_prime:
                    primes.append(n)

            return jsonify({
                "is_success": True,
                "official_email": EMAIL,
                "data": primes
            }), 200

        # ---------- LCM ----------
        if key == "lcm":
            result = value[0]
            for v in value[1:]:
                result = lcm(result, v)

            return jsonify({
                "is_success": True,
                "official_email": EMAIL,
                "data": result
            }), 200

        # ---------- HCF ----------
        if key == "hcf":
            result = value[0]
            for v in value[1:]:
                result = gcd(result, v)

            return jsonify({
                "is_success": True,
                "official_email": EMAIL,
                "data": result
            }), 200

        # ---------- AI ----------
        if key == "AI":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={os.getenv('GEMINI_API_KEY')}"
            payload = {
                "contents": [
                    {"parts": [{"text": value}]}
                ]
            }

            response = requests.post(url, json=payload)
            result = response.json()

            answer = result["candidates"][0]["content"]["parts"][0]["text"].split()[0]

            return jsonify({
                "is_success": True,
                "official_email": EMAIL,
                "data": answer
            }), 200

        # ---------- Invalid Key ----------
        return jsonify({
            "is_success": False,
            "error": "Invalid key"
        }), 400

    except Exception as e:
        return jsonify({
            "is_success": False,
            "error": str(e)
        }), 500


# ---------- Run App ----------
if __name__ == "__main__":
    app.run(debug=True)
