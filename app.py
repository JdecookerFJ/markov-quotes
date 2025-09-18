from flask import Flask, render_template
import pandas as pd
import markovify
import os

app = Flask(__name__)
try:
    df = pd.read_csv("quotes.csv", sep=";")
    print("✅ CSV ingelezen:", df.shape)
    quotes = df["Quote"].dropna().astype(str).str.strip()
except Exception as e:
    print("❌ Fout bij lezen van CSV:", e)
    quotes = ["(geen quotes beschikbaar)"]

import markovify
model = markovify.NewlineText("\n".join(quotes), state_size=5)

def generate_quote(max_words=40, tries=100):
    for _ in range(tries):
        sentence = model.make_sentence(tries=tries)
        if sentence and len(sentence.split()) <= max_words:
            return sentence
    return "Kon geen quote genereren."

@app.route("/")
def index():
    quote = generate_quote()
    return render_template("index.html", quote=quote)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
