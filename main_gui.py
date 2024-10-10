import hashlib
import time
import tkinter as tk
from tkinter import messagebox

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
        return f"Block #{self.index} [Hash: {self.hash}, Prev Hash: {self.previous_hash}, Data: {self.transactions}]"

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
        return block.hash

    def is_chain_valid(self):
        # Validate the chain's integrity
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# Tkinter GUI class
class BlockchainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Blockchain GUI")

        # Blockchain instance
        self.blockchain = Blockchain()

        # Title label
        self.label = tk.Label(root, text="Simple Blockchain", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Transaction entry
        self.transaction_label = tk.Label(root, text="Enter transactions (comma separated):")
        self.transaction_label.pack(pady=5)

        self.transaction_entry = tk.Entry(root, width=50)
        self.transaction_entry.pack(pady=5)

        # Add Block button
        self.add_block_button = tk.Button(root, text="Add Block", command=self.add_block)
        self.add_block_button.pack(pady=10)

        # Display Blockchain button
        self.display_button = tk.Button(root, text="Display Blockchain", command=self.display_blockchain)
        self.display_button.pack(pady=10)

        # Validate Chain button
        self.validate_button = tk.Button(root, text="Validate Blockchain", command=self.validate_blockchain)
        self.validate_button.pack(pady=10)

        # Output Text box
        self.output_text = tk.Text(root, height=15, width=80)
        self.output_text.pack(pady=10)

    def add_block(self):
        transactions = self.transaction_entry.get()
        if not transactions:
            messagebox.showwarning("Input Error", "Please enter some transactions.")
            return

        new_block = Block(len(self.blockchain.chain), self.blockchain.get_latest_block().hash,
                          transactions, time.time())
        self.blockchain.add_block(new_block)
        self.output_text.insert(tk.END, f"Block #{new_block.index} added!\n")
        self.transaction_entry.delete(0, tk.END)

    def display_blockchain(self):
        self.output_text.delete(1.0, tk.END)
        for block in self.blockchain.chain:
            self.output_text.insert(tk.END, str(block) + "\n")

    def validate_blockchain(self):
        is_valid = self.blockchain.is_chain_valid()
        if is_valid:
            messagebox.showinfo("Validation", "Blockchain is valid!")
        else:
            messagebox.showerror("Validation", "Blockchain is invalid!")

# Main loop for Tkinter GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainGUI(root)
    root.mainloop()
