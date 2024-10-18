from .EntityAbstract import EntityAbstract
import os

class ID():


    def __init__(self, pub_key, sig):

       self.pub_key = pub_key
       self.sig = sig 

    
    @staticmethod 
    def load_id(fname):
        id = ID(None, None)
        if not os.path.exists(fname + ".sig") or not os.path.exists(fname + ".pub"):
            return id
        id.pub_key = EntityAbstract.load_pub_key(fname + ".pub")

        with open(fname + ".sig", "rb") as f:
            id.sig = f.read()
        return id

    def save_id(self, fname):
        EntityAbstract.save_pub_key(fname+".pub",self.pub_key)

        with open(fname+'.sig', 'wb') as f:
            f.write(self.sig)
    
    def verify(self, gov):

        pub_key_bytes = EntityAbstract.get_public_bytes(self.pub_key)
        return gov.verify(pub_key_bytes, self.sig)
        
