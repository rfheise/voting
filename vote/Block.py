from ..digital_id import ID 

class Block():

    def __init__(self, children):
        self.children = children
        self.sig = None 
        self.id = None
    
    def generate_block_bytes(self):
        message = bytearray()
        self.children.sort(key = lambda child: child.sig)
        for child in self.children:
            if child.sig is None:
                print("Child sig doesn't exist")
                exit(3)
            message += child.sig
        return message 
    
    def sign_block(self, gov):
        # only sign block if all ids are valid 
        if not self.check(gov):
            print("Invalid ID/Vote")
            exit(9)
        self.sig = gov.sign(self.generate_block_bytes())
        return self.sig 

    def save_sig(self, path):
        if self.sig is None:
            print("sig is none")
            exit(4)
        with open(path + "/election.sig", "wb") as f:
            f.write(self.sig)
    
    def load_sig(self, path):
        with open(path + "/election.sig", "rb") as f:
            self.sig = f.read()
    
    def load_id(self,path):
        self.id = ID.load_id(path)
    
    def check(self, gov):
        for child in self.children:
            #it's okay to trust the child sig as long as the id is valid
            if not child.id.verify(gov):
                return False 
        return True

    def verify_sig(self, gov):
        if not self.check(gov):
            print("Invalid ID/Vote")
            exit(9)
        m = self.generate_block_bytes() 
        return gov.verify(m, self.sig)


    
class VoteBlock(Block):
    
    def __init__(self, votes):
        self.votes = votes 
    
    def generate_block_bytes(self):
        message = bytearray()
        self.votes.sort(key = lambda vote: vote.vd.timestamp)
        for vote in self.votes:
            message += vote.to_bytes()
        return message
    
    def sign_block(self, gov):
        
        #verify children
        for vote in self.votes:
            if not vote.verify(gov):
                return None 
        self.sig = gov.sign(self.generate_block_bytes())
        return self.sig 

    def check(self, gov):
        #verify children
        for vote in self.votes:
            if not vote.verify(gov):
                return False
        return True
        
    
