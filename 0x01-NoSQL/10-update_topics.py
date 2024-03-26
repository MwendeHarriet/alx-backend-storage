#!/usr/bin/env python3
"""Module that changes all topics of a school document based on the name:
    Prototype: def update_topics(mongo_collection, name, topics):
    mongo_collection will be the pymongo collection object
    name (string) will be the school name to update
    topics (list of strings) will be the list of topics approached
    in the school."""


from pymongo import MongoClient


client = MongoClient("localhost", 27017)
collection = client.my_db.mongo_collection


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})


client.close()
