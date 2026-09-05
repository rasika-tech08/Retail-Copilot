from flask import Flask, jsonify, request, send_from_directory
import csv
import os

app = Flask(__name__, static_folder="frontend")


# -----------------------------
# Load products from CSV
# -----------------------------
def load_products():
    products = []

    file_path = os.path.join("data", "products.csv")

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            products.append(row)

    return products


# -----------------------------
# Home page
# -----------------------------
@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


# -----------------------------
# Serve CSS and JavaScript
# -----------------------------
@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory("frontend", filename)


# -----------------------------
# Products API
# -----------------------------
@app.route("/api/products")
def products():
    try:
        data = load_products()
        return jsonify(data)

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


# -----------------------------
# Copilot API
# -----------------------------
@app.route("/api/ask", methods=["POST"])
def ask_copilot():

    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "error": "Question is required"
        }), 400

    products = load_products()

    # Simple local product search
    matching_products = []

    for product in products:

        product_text = (
            product["product_name"]
            + " "
            + product["category"]
        ).lower()

        if any(word in product_text for word in question.lower().split()):
            matching_products.append(product)

    # If matching products are found
    if matching_products:

        answer = "Here are the relevant products:\n\n"

        for product in matching_products:
            answer += (
                f"• {product['product_name']} - "
                f"₹{product['price']} "
                f"({product['category']})\n"
            )

    else:

        answer = (
            "I could not find a matching product in the "
            "available inventory."
        )

    return jsonify({
        "answer": answer
    })


# -----------------------------
# Start application
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )