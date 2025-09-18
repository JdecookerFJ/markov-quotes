from flask import Flask, render_template
import pandas as pd
import markovify

app = Flask(__name__)

# Quotes laden en Markov-model maken
df = pd.read_csv("quotes.csv", sep=";")
quotes = df["Quote"].dropna().astype(str).str.strip()
model = markovify.NewlineText("\n".join(quotes), state_size=3)

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
    app.run(host="0.0.0.0", port=5000)
