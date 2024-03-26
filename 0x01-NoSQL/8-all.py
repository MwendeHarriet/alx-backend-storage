#!/usr/bin/env python3
"""Module lists all documents in a collection:
    Prototype: def list_all(mongo_collection):
    Return an empty list if no document in the collection
    mongo_collection will be the pymongo collection object."""


from pymongo import MongoClient

client = MongoClient("localhost", 27017)
collection = client.my_db.mongo_collection


def list_all(mongo_collection):
    """Function lists all documents in a collection."""
    docs = mongo_collection.find()
    if docs:
        return list(docs)
    else:
        return []


client.close()
