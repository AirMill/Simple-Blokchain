import hashlib
import time

# Define the Block structure
class Block:
    def __init__(self, index, previous_hash, transactions, timestamp, nonce=0):
        self.index = index  # Block number in the chain
        self.previous_hash = previous_hash  # Hash of the previous block
        self.transactions = transactions  # List of transactions
        self.timestamp = timestamp  # Time of block creation
        self.nonce = nonce  # Used for mining (Proof of Work)
        self.hash = self.calculate_hash()  # Current block's hash

    def calculate_hash(self):
        # Concatenate block data and hash it using SHA256
        block_data = (str(self.index) + str(self.previous_hash) + str(self.transactions) + 
                      str(self.timestamp) + str(self.nonce))
        return hashlib.sha256(block_data.encode()).hexdigest()

    def __str__(self):
        return f"Block #{self.index} [Hash: {self.hash}]"

# Define the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]  # Initialize the chain with the genesis block
        self.difficulty = 2  # Number of leading zeros required in hash for proof of work

    def create_genesis_block(self):
        # The first block of the blockchain
        return Block(0, "0", "Genesis Block", time.time())

    def get_latest_block(self):
        return self.chain[-1]  # Return the latest block in the chain

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash  # Set the previous block's hash
        new_block.hash = self.mine_block(new_block)  # Mine the block before adding
        self.chain.append(new_block)

    def mine_block(self, block):
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()
        print(f"Block mined: {block.hash}")
        return block.hash

    def is_chain_valid(self):
        # Validate the chain's integrity
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                print("Current block's hash is not valid")
                return False

            if current_block.previous_hash != previous_block.hash:
                print("Previous block's hash does not match")
                return False

        return True

# Example usage of the blockchain
if __name__ == "__main__":
    blockchain = Blockchain()

    # Add some blocks with mock transactions
    blockchain.add_block(Block(1, "", ["Transaction 1", "Transaction 2"], time.time()))
    blockchain.add_block(Block(2, "", ["Transaction 3", "Transaction 4"], time.time()))

    print("Blockchain validity:", blockchain.is_chain_valid())

    # Output all the blocks
    for block in blockchain.chain:
        print(block)
