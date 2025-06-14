
import difflib
import idna
import joblib
import re

# Load known domains
with open("../data/legitimate_domains.txt") as f:
    legit_domains = [line.strip() for line in f.readlines()]

# Load pre-trained ML model
model = joblib.load("../backend/phishing_model.pkl")

def extract_features(domain):
    try:
        decoded = idna.decode(domain)
    except Exception:
        decoded = domain
    features = []
    features.append(len(decoded))
    features.append(sum(1 for c in decoded if not c.isascii()))
    features.append(len(decoded.split('.')))
    closest = difflib.get_close_matches(decoded, legit_domains, n=1)
    features.append(len(closest[0]) if closest else 0)
    return [features]

def detect_homoglyph(domain):
    features = extract_features(domain)
    pred = model.predict(features)
    matched = difflib.get_close_matches(domain, legit_domains, n=1, cutoff=0.75)
    return bool(pred[0]), matched[0] if matched else None

def generate_homoglyphs(domain):
    mapping = {'o': ['ο', 'օ'], 'a': ['а'], 'e': ['е'], 'i': ['і'], 'c': ['с'], 'l': ['ӏ'], 'd': ['ԁ']}
    variants = set()
    for i, char in enumerate(domain):
        if char in mapping:
            for homoglyph in mapping[char]:
                variant = domain[:i] + homoglyph + domain[i+1:]
                variants.add(variant)
    return list(variants)
