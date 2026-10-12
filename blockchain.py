import hashlib
import json
from time import time
from datetime import datetime


class Block:
    def __init__(self, index, certificate_data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time()
        self.certificate_data = certificate_data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "certificate_data": self.certificate_data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            "certificate_data": self.certificate_data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce
        }


class Blockchain:
    difficulty = 3  # Proof-of-work difficulty

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, {"info": "Genesis Block"}, "0")
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block.nonce = 0
        computed = block.compute_hash()
        while not computed.startswith('0' * self.difficulty):
            block.nonce += 1
            computed = block.compute_hash()
        return computed

    def add_block(self, certificate_data):
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            certificate_data=certificate_data,
            previous_hash=last_block.hash
        )
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
        return True

    def find_certificate(self, cert_id):
        for block in self.chain:
            if block.certificate_data.get("certificate_id") == cert_id:
                return block
        return None

    def to_list(self):
        return [block.to_dict() for block in self.chain]

    def tamper_block(self, index, new_student_name):
        """For demo - tampers data without re-mining to show invalidation."""
        if 0 <= index < len(self.chain):
            self.chain[index].certificate_data["student_name"] = new_student_name


certificate_chain = Blockchain()