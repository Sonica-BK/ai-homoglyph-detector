from flask import Flask, request, jsonify
from detect import detect_homoglyph, generate_homoglyphs
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    domain = data.get("domain")
    phishing, matched = detect_homoglyph(domain)
    return jsonify({"phishing": phishing, "matched": matched})

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    domain = data.get("domain")
    variants = generate_homoglyphs(domain)
    return jsonify({"variants": variants})

if __name__ == '__main__':
    app.run(port=5000)