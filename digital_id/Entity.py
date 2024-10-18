from .EntityAbstract import EntityAbstract
from .ID import ID 
import os 

class VoterData():

    data_path = EntityAbstract.data_path

    def __init__(self, data):
        self.data = data
    
    @staticmethod
    def read_data(fname):
        # read user data from file 
        data = {}
        with open(fname, "r") as f:
            for line in f:
                line = line.strip("\n").split(":")
                data[line[0]] = line[1]
        d = VoterData(None)
        d.data = data
        return d 
    
    @staticmethod
    def load_data(data_fname):
        data = VoterData.read_data(data_fname)
        return data
    
    def save_data(self, fname):
        with open(fname, "w") as f:
            for d in self.data:
                f.write(f"{d}:{self.data[d]}\n")

class Entity(EntityAbstract):

    def __init__(self, pub_key=None, priv_key=None, data:VoterData=None, id = None):
        super().__init__(pub_key, priv_key)
        self.data = None 
        self.id = None
        if data is not None:
            self.data = data
        if id is not None:
            self.id = ID.load_id(id)
    
    def get_data(self):
        return self.data 
    
    def get_id(self, gov):
        self.id = gov.generate_id(self)
        return self.id
    
    def generate_id(self, individual):
        #verifies identity and signs public key of individual

        #get data from individual
        data = individual.get_data()
        if self.verify_data(data):
            #alternatively could sign pub_key with data for 
            # identity verification 
            #this assumes you only want to know if an indidual is a citizen
            #and not their identity
            ind_pub_key = individual.get_pub_key()
            pub_key_bytes = self.get_public_bytes(ind_pub_key)
            sig = self.sign(pub_key_bytes)
            ind_id = ID(ind_pub_key, sig)
            return ind_id
        
        return None

    def save_entity(self, path):
        super().save_entity(path)
        if self.data:
            self.data.save_data(path + "/voter.dat") 
        if self.id:
            self.id.save_id(path + "/id")
    
    def load_entity(self, fname):
        super().load_entity(fname)
        if os.path.exists(fname + "/voter.dat"):
            self.data = VoterData.load_data(fname + "/voter.dat")
        
        self.id = ID.load_id(fname + "/id")
    
    @staticmethod
    def load_voter(fname):
        v = Entity(None, None, None, None)
        v.load_entity(fname)
        return v

    def verify_data(self, data):
        #verifies the accuracy of an individuals data
        #for proof of concenpt assume data is valid 
        return True
        
    @staticmethod
    def get_org(path):
        return Entity(path + "/key.pub", path + "/key.priv", None, None)

def main():
    path = EntityAbstract.data_path
    data = VoterData({"name":"ryan", "ssn":"555-55-5555"})
    ind = Entity(path + "ryan/ryan.pub",path +"ryan/ryan.priv",data,None)
    gov = Entity.get_org("gov/")
    gov.save_entity(path + "gov/")
    ind.get_id(gov)
    ind.save_entity(path+ "ryan")
    ind.load_voter(path + "ryan")

if __name__ == "__main__":
    main()
        