import os
#using hazmat for proof of concept
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import hashlib

class EntityAbstract():
    
    data_path = "./election/data/"

    def __init__(self, pub_key, priv_key):

        if pub_key and priv_key and not os.path.exists(pub_key) and not os.path.exists(priv_key):
            self.generate_key(pub_key, priv_key)
        else:
            self.load_keys(pub_key, priv_key)
        # if self.pub_key:
        #     print(hashlib.sha256(self.get_public_bytes(self.pub_key)).hexdigest())
        
    def sign(self, message):
        # sign message with key
        # returns sig
        if self.priv_key == None:
            print("No Private Key Loaded")
            exit(1)
        signature = self.priv_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature


    def verify(self, message, sig):
        # verify the digital signature of a message using a key
        # determines whether or not sig is valid for message 
        if self.pub_key == None:
            print("No Pubkey Loaded")
            exit(1)
        try:
            self.pub_key.verify(
                sig,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except InvalidSignature:
            return False
        return True
    
    def load_keys(self, pub_key, priv_key):

        #load keys from file
        if type(pub_key) == str and pub_key is not None:
            self.pub_key = self.load_pub_key(pub_key)
        else:
            self.pub_key = pub_key 
        if type(priv_key) == str and priv_key is not None:
            self.priv_key = self.load_priv_key(priv_key)
        else:
            self.priv_key = priv_key

    def save_entity(self, path):
        os.makedirs(path, exist_ok=True)
        fname = f"{path}/key"
        self.save_priv_key(fname+".priv", self.priv_key)
        self.save_pub_key(fname+".pub", self.pub_key)

    def load_entity(self, fname):
        self.__init__(fname + "/key.pub", fname + "/key.priv")
        return self

    def generate_key(self, pub_key, priv_key):

        if pub_key is None or priv_key is None:
            print("Please Provide A Filename for public and private key")
            exit(1)

        self.priv_key = private_key = rsa.generate_private_key(
            public_exponent=65537,  # Commonly used value for public exponent
            key_size=4096           # Key size in bits (2048 is a standard size)
        )

        self.pub_key = self.priv_key.public_key()
        
    
    @staticmethod
    def save_priv_key(fname, priv_key):
        # Serialize private key to PEM format (unencrypted)
        private_bytes = priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open(fname, "wb") as f:
            f.write(private_bytes)

    @staticmethod
    def get_public_bytes(pub_key):
        public_bytes = pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return public_bytes
    
    @staticmethod 
    def save_pub_key(fname, pub_key):
        # Serialize public key to PEM format
        public_bytes = EntityAbstract.get_public_bytes(pub_key)

        with open(fname, "wb") as f:
            f.write(public_bytes)

    @staticmethod
    def load_priv_key(fname):

        if fname is None:
            return None
        # Load private key from PEM file
        with open(fname, "rb") as f:
            priv_key = serialization.load_pem_private_key(
                f.read(),
                password=None  # If the key is encrypted, provide the password here
            )
        return priv_key

    @staticmethod
    def load_pub_key(fname):
        
        if fname is None:
            return None
        # Load public key from PEM file
        with open(fname, "rb") as f:
            pub_key = serialization.load_pem_public_key(f.read())
        return pub_key

    def get_pub_key(self):
        if self.pub_key is None:
            print("Public Key Not Loaded")
            exit(2)
        #return public key of 
        return self.pub_key