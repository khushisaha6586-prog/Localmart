from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["localmart_db"]

products_collection = db["products"]
orders_collection = db["orders"]
cart_collection = db["cart"]