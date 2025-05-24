
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    numbers = []
    if request.method == "POST":
        try:
            n = int(request.form["n"])
            numbers = [i for i in range(2, 2*n + 1, 2)]
        except:
            numbers = ["Invalid input"]
    return render_template("index.html", numbers=numbers)

if __name__ == "__main__":
    app.run(debug=True)
