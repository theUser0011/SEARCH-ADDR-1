from pymongo import MongoClient
import os

# Load MongoDB URI from environment variable
mongo_url = 'mongodb+srv://afg154005:gnLhPlgHpuQaFjvh@cluster0.0yvn2uk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client['START_DB']
collection = db['start_one']

# Define the document
doc = {
    "doc_num": 1,
    "start_point": 0  # or any initial value you want
}

# Insert the document (only if not already present)
if not collection.find_one({"doc_num": 1}):
    collection.insert_one(doc)
    print("✅ Document inserted.")
else:
    print("⚠️ Document with doc_num=1 already exists.")
