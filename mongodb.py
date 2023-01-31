import pprint
from datetime import datetime
import pymongo as pym

# running client access
client = pym.MongoClient("mongodb+srv://danrlei:password@cluster0.fljsqsv.mongodb.net/?retryWrites=true&w=majority")

# defining a database
db = client.test
collection = db.test_connection

# retrieving information
print(db.test_collection)

# creating a document
post = dict(author="Mike", text="My first MongoDB application",
            tags=["mongodb", "python3", "pymongo"], date=datetime.utcnow())

# preparing to submit the information
posts = db.posts
post_id = posts.insert_one(post).inserted_id

print(post_id)
print(db.posts)
print(db.posts.find_one())

# viewing indented
pprint.pprint(db.posts.find_one())

# creating new document - bulk inserts
new_posts = [{
        "author": "Mike",
        "text": "Another post",
        "tags": ["bulk", "post", "insert"],
        "date": datetime.utcnow()
    },
    {
        "author": "Joao",
        "text": "Post from Joao. New post available",
        "title": "Mongo is fun",
        "date": datetime.utcnow()
    }
]

result = posts.insert_many(new_posts)
print(result.inserted_ids)

# final recovery
pprint.pprint(db.posts.find_one())

# search
pprint.pprint(db.posts.find_one({"author": "Mike"}))

# handling all documents
print(posts.find())

for post in posts.find():
    pprint.pprint(post)
