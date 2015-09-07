from pymongo import MongoClient
import pprint

client = MongoClient("mongodb://localhost:27017")
db = client.map

def find():
    count = db.vancouver.find({"type" : "node"})
    
    for a in count:
        pprint.pprint(a)
        
    street = len(db.vancouver.distinct("address.street"))
    print(street)                                      
    #for a in street:
    #    pprint.pprint(a)
        
        

if __name__ == '__main__':
    find()