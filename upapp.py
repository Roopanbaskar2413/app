from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Mock dataset of 50 fashion items
fashion_items = [
    {
        "id": i,
        "category": random.choice(["dresses", "shoes", "accessories"]),
        "price": round(random.uniform(10, 500), 2),
        "size": random.choice(["S", "M", "L", "XL"]),
        "color": random.choice(["red", "blue", "green", "black", "white"]),
        "brand": random.choice(["BrandA", "BrandB", "BrandC"]),
        "rating": random.randint(1, 5)
    }
    for i in range(1, 51)
]

# Filters, pagination, and existing endpoints omitted for brevity.

# Add a new item
@app.route('/api/v1/items', methods=['POST'])
def add_item():
    new_item = request.get_json()

    # Validate required fields
    required_fields = ["category", "price", "size", "color", "brand", "rating"]
    for field in required_fields:
        if field not in new_item:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Validate data types
    if not isinstance(new_item['price'], (int, float)):
        return jsonify({"error": "'price' must be a number"}), 400
    if new_item['rating'] not in range(1, 6):
        return jsonify({"error": "'rating' must be an integer between 1 and 5"}), 400

    # Assign a unique ID
    new_item['id'] = len(fashion_items) + 1

    # Add the item to the dataset
    fashion_items.append(new_item)

    return jsonify({"message": "Item added successfully", "item": new_item}), 201


if __name__ == '__main__':
    app.run(debug=True)
