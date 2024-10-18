from ..digital_id import Entity, ID
import time
import struct
import os

class VoteData():

    def __init__(self, candidate):
        self.candidate = candidate
        #other vote data to collect 
        self.timestamp = time.time()
    
    def get_bytes(self):
        
        cand = self.candidate.encode("utf-8")
        time = struct.pack('d', self.timestamp)

        return cand + time
    
    @staticmethod
    def get_data_from_bytes(bs):

        vd = VoteData(None)
        vd.candidate = bs[:-8].decode("utf-8")
        vd.timestamp = struct.unpack('d', bs[-8:])[0]
        return vd
    
    def save(self, fname):

        with open(fname, "wb") as f:
            f.write(self.get_bytes())
    
    @staticmethod
    def load(fname):

        bs = None 
        with open(fname, "rb") as f:
            bs = f.read()
        return VoteData.get_data_from_bytes(bs)
    


class Vote():

    def __init__(self, vd:VoteData, id, sig):
        
        self.vd = vd
        self.id = id
        self.sig = sig

    def to_bytes(self):
        if self.vd == None or self.id == None or self.sig == None:
            print("Vote is Empty")
            exit(6)
        m = bytes()
        m += self.vd.get_bytes()
        m += self.sig 
        m += Entity.get_public_bytes(self.id.pub_key)
        m += self.id.sig
        return m 
    
    @staticmethod
    def create_vote(vote_data:VoteData, individual):

        id = individual.id 
        sig = individual.sign(vote_data.get_bytes())
        return Vote(vote_data, id, sig)
    
    def save_vote(self, path):
        os.makedirs(path, exist_ok=True)
        self.id.save_id(path + "/vote.id")
        self.vd.save(path+ "/vote.vd")
        with open(path+ "/vote.sig", "wb") as f:
            f.write(self.sig)
        
        
    @staticmethod
    def load_vote(fname):
        vote = Vote(None, None, None)
        vote.id = ID.load_id(fname + "/vote.id")
        vote.vd = VoteData.load(fname+ "/vote.vd")
        with open(fname + "/vote.sig", "rb") as f:
            vote.sig = f.read()
        return vote

    def verify(self, gov:Entity):
        
        #verify id 
        pub_key_bytes = Entity.get_public_bytes(self.id.pub_key)
        if not gov.verify(pub_key_bytes,self.id.sig):
            return False 
        
        #verify vote
        ind = Entity(self.id.pub_key, None)
        if not ind.verify(self.vd.get_bytes(), self.sig):
            return False 
        
        #verified by ind and gov
        return True 
    
        
def main():
    path = Entity.data_path 
    voter = Entity.load_voter(path + "/ryan")
    vote_data = VoteData("bob")
    vote = Vote.create_vote(vote_data,voter)
    gov = Entity.get_org(path + "gov/")
    print(vote.verify(gov))
    vote.save_vote(path + "votes/ryan")
    vote = Vote.load_vote(path + "votes/ryan")
    print(vote.verify(gov))

if __name__ == "__main__":
    main()
        
        
