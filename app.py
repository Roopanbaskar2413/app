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

    # filter 
def apply_filters(items, filters):
    if filters.get('category'):
        items = [item for item in items if item['category'].lower() == filters['category'].lower()]
    
    if filters.get('price_min') is not None:
        items = [item for item in items if item['price'] >= float(filters['price_min'])]
    
    if filters.get('price_max') is not None:
        items = [item for item in items if item['price'] <= float(filters['price_max'])]
    
    if filters.get('size'):
        items = [item for item in items if item['size'].lower() == filters['size'].lower()]
    
    if filters.get('color'):
        items = [item for item in items if item['color'].lower() == filters['color'].lower()]
    
    if filters.get('brand'):
        items = [item for item in items if item['brand'].lower() == filters['brand'].lower()]
    
    if filters.get('rating'):
        items = [item for item in items if item['rating'] == int(filters['rating'])]

    # Sorting
    if filters.get('sort_by'):
        if filters['sort_by'] == 'price':
            items = sorted(items, key=lambda x: x['price'])
        elif filters['sort_by'] == 'rating':
            items = sorted(items, key=lambda x: x['rating'], reverse=True)
    
    return items

# Pagination
def paginate(items, page, limit):
    start = (page - 1) * limit
    end = start + limit
    return items[start:end]

@app.route('/api/v1/items', methods=['GET'])
def get_items():
    filters = {
        'category': request.args.get('category'),
        'price_min': request.args.get('price_min'),
        'price_max': request.args.get('price_max'),
        'size': request.args.get('size'),
        'color': request.args.get('color'),
        'brand': request.args.get('brand'),
        'rating': request.args.get('rating'),
        'sort_by': request.args.get('sort_by')
    }

    # Validation for price and rating
    if filters.get('price_min') and not filters['price_min'].replace('.', '', 1).isdigit():
        return jsonify({"error": "Invalid price_min value"}), 400
    if filters.get('price_max') and not filters['price_max'].replace('.', '', 1).isdigit():
        return jsonify({"error": "Invalid price_max value"}), 400
    if filters.get('rating') and not filters['rating'].isdigit():
        return jsonify({"error": "Invalid rating value"}), 400
    
    # Apply filters
    filtered_items = apply_filters(fashion_items, filters)

    # Pagination
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    paginated_items = paginate(filtered_items, page, limit)

    return jsonify({
        'items': paginated_items,
        'total': len(filtered_items),
        'page': page,
        'limit': limit
    })


if __name__ == '__main__':
    app.run(debug=True)
