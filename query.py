from pymongo import MongoClient
import pprint

client = MongoClient("mongodb://localhost:27017")
db = client.map

def find():
    count = db.vancouver.find().count()
    print count
    nodes = db.vancouver.find({"type" : "node"}).count()
    print nodes
    way = db.vancouver.find({"type" : "way"}).count()
    print way
    unique_users = len(db.vancouver.distinct("created_by"))
    print unique_users
    unique_sources = len(db.vancouver.distinct("source"))
    print unique_sources
    top_contributor = db.vancouver.aggregate([{"$match" : {"created_by" : {"$exists" : 1}}},
                                          {"$group" : {"_id" : "$created_by", "count" : {"$sum" : 1}}},
                                          {"$sort" : {"count" : -1}},{"$limit" : 1}])
    for a in top_contributor:
        pprint.pprint(a)
   
    top_sources = db.vancouver.aggregate([{"$match" : {"created_by" : {"$exists" : 1}}},
                                          {"$group" : {"_id" : "$created_by", "count" : {"$sum" : 1}}},
                                          {"$sort" : {"count" : -1}}])
    for a in top_sources:
        pprint.pprint(a)     
        
    top_amenity = db.vancouver.aggregate([{"$match" : {"amenity" : {"$exists" : 1}}},
                                      {"$group" : {"_id" : "$amenity", "count" : {"$sum" : 1}}},
                                      {"$sort" : {"count" : -1}},{"$limit" : 10}])
    for a in top_amenity:
        pprint.pprint(a)
        
    
    top_restaurant = db.vancouver.aggregate([{"$match" : {"amenity" : "restaurant"}},
                                      {"$group" : {"_id" : "$name", "count" : {"$sum" : 1}}},
                                      {"$sort" : {"count" : -1}},{"$limit" : 11}])
    for a in top_restaurant:
        pprint.pprint(a)
        

if __name__ == '__main__':
    find()