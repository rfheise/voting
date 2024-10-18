from Entity import Entity
from ID import ID

class Organization(Entity):

    def __init__(self):
        pub_key = "./government_id/gov.pub"
        priv_key = "./government_id/gov.priv"
        super().__init__(pub_key, priv_key)

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

    def verify_data(self, data):
        #verifies the accuracy of an individuals data
        #for proof of concenpt assume data is valid 
        return True

    def get_pub_key(self):
        #return public key of 
        return self.pub_key