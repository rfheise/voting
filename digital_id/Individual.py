from Entity import Entity
from Organization import Organization
from ID import ID 

class Individual(Entity):

    def __init__(self, pub_key=None, priv_key=None, data_fname = None, id = None):
        super().__init__(pub_key, priv_key)
        if data_fname is not None:
            self.data = self.load_data(data_fname)
        if id is not None:
            self.id = ID.load_id(id)
    
    def get_data(self):
        return self.data 
    
    def load_data(self, data_fname):
        data = self.read_data(data_fname)
        return data

    @staticmethod
    def read_data(fname):
        # read user data from file 
        data = {}
        with open(fname, "r") as f:
            for line in f:
                line = line.strip("\n").split(":")
                data[line[0]] = line[1]
        return data 
    
    def get_id(self, Organization):
        self.id = Organization.generate_id(self)
        return self.id
    
    def get_pub_key(self):
        if self.pub_key is None:
            print("Public Key Not Loaded")
            exit(2)

        return self.pub_key

def main():
    ind = Individual("./individual/ryan.pub","individual/ryan.priv","./individual/ryan.txt",None)
    gov = Organization()
    id = ind.get_id(gov)
    id.save_id("./individual/ryan-id")

if __name__ == "__main__":
    main()
        