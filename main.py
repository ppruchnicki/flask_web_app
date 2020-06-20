from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello? <h1>HELLO world<h1>"

if __name__ == "__main__":
    app.run(debug=True)