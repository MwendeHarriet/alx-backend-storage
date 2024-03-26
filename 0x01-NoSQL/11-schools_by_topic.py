#!/usr/bin/env python3
"""Module returns the list of school having a specific topic:
    Prototype: def schools_by_topic(mongo_collection, topic):
    mongo_collection will be the pymongo collection object
    topic (string) will be topic searched."""


from pymongo import MongoClient


client = MongoClient("localhost", 27017)
collection = client.my_db.mongo_collection


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic
    """
    return mongo_collection.find({"topics": topic})


client.close()
