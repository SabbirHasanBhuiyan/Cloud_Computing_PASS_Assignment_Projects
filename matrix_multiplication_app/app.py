from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Process input (placeholder)
        data = request.form.get("input_data")
        result = f"Processed: {data}"
        return render_template_string(open("index.html").read(), result=result)
    return render_template_string(open("index.html").read())

if __name__ == "__main__":
    app.run(debug=True)
