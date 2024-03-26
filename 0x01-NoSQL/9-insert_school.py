#!/usr/bin/env python3
"""Module inserts a new document in a collection based on kwargs:
    Prototype: def insert_school(mongo_collection, **kwargs):
    mongo_collection will be the pymongo collection object
    Returns the new _id."""


from pymongo import MongoClient


client = MongoClient("localhost", 27017)
collection = client.my_db.mongo_collection


def insert_school(mongo_collection, **kwargs):
    """Function inserts a new document in a collection based on kwargs."""

    result = mongo_collection.insert_one(kwargs)

    return result.inserted_id


client.close()
