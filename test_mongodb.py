from mongodb import products_collection

product = {
    "name": "Rice",
    "category": "Grocery",
    "price": 60,
    "stock": 50
}

result = products_collection.insert_one(product)

print("Product inserted with ID:", result.inserted_id)