import json
import os

class Database(object):
    def __init__(self , location):
        self.location = os.path.expanduser(location)
        self.load(self.location)

    def load(self , location):
       if os.path.exists(location):
           self._load()
       else:
            raise Exception(f"File \"{self.location}\" could not be found")

    def _load(self):
        self.db = json.load(open(self.location , "r"))

    def dumpdb(self):
        json.dump(self.db , open(self.location, "w+"), indent=4)

    def set(self , key , value):
        self.db[str(key)] = value
        self.dumpdb()

    def get(self , key):
        return self.db[key]

    def delete(self , key):
        if not key in self.db:
            return
        del self.db[key]
        self.dumpdb()

    def resetdb(self):
        self.db = {}
        self.dumpdb()

    def pop(self, key):
        self.db.pop(key)
        self.dumpdb()
    
    def keys(self):
        return self.db.keys()