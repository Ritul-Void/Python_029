import json
from flask import Flask, jsonify
from random import choice

app = Flask(__name__)


with open("Projects\Day-8-QuotesFlaskApi\quotes.json", "r", encoding="utf-8") as f:
    data = json.load(f)

@app.route("/quotes", methods=["GET"])
def all_quotes():
    return jsonify(data)

@app.route("/quotes/random", methods=["GET"])
def random_quote():
    return jsonify(choice(data["quotes"]))

if __name__ == "__main__":
    app.run(debug=True)



# All quotes
# 👉 http://127.0.0.1:5000/quotes

# Random quote
# 👉 http://127.0.0.1:5000/quotes/random