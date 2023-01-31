import pprint
import pymongo as pym

# running client access
client = pym.MongoClient("mongodb+srv://danrlei:password@cluster0.fljsqsv.mongodb.net/?retryWrites=true&w=majority")

db = client.test
posts = db.posts

for post in posts.find():
    pprint.pprint(post)

print(posts.count_documents({}))
print(posts.count_documents({"author": "Mike"}))
print(posts.count_documents({"tags": "insert"}))

pprint.pprint(posts.find_one({"tags": "insert"}))

# retrieving information in an orderly manner
for post in posts.find({}).sort("date"):
    pprint.pprint(post)

result = db.profiles.create_index(['author', pym.ASCENDING], unique=True)

print(sorted(list(db.profiles.index_information)))

user_profile = [
    {'user_id': 211, 'name': 'luke'},
    {'user_id': 212, 'name': 'Joao'}
]

results = db.profiles.insert_many(user_profile)

# removing documents
collections = db.list_collection_names()

db['profiles'].drop()

for collection in collections:
    print(collection)

for post in posts.find():
    pprint.pprint(post)

print(posts.delete_one({'author': 'Mike'}))

# deleting database
client.drop_database('test')

print(db.list_collection_names())
