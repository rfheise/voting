from Entity import Entity

class ID():


    def __init__(self, pub_key, sig):

       self.pub_key = pub_key
       self.sig = sig 

    
    @staticmethod 
    def load_id(fname):
        id = ID(None, None)
        id.pub_key = Entity.load_pub_key(fname + ".pub")

        with open(fname + ".sig", "rb") as f:
            id.sig = f.read()
        return id

    def save_id(self, fname):
        Entity.save_pub_key(fname+".pub",self.pub_key)

        with open(fname+'.sig', 'wb') as f:
            f.write(self.sig)
