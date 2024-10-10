import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests

API_KEY = 'your_blockcypher_api_key'  # Replace with your BlockCypher API Key

# Define the API endpoints
BASE_URL = "https://api.blockcypher.com/v1/btc/main"

# Function to get transaction details
def get_transaction(tx_hash):
    url = f"{BASE_URL}/txs/{tx_hash}?token={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to trace a Bitcoin transaction and its inputs
def trace_transaction(tx_hash, depth=3):
    output_textbox.insert(tk.END, f"Tracing transaction: {tx_hash}\n")
    transaction = get_transaction(tx_hash)
    
    if not transaction:
        messagebox.showerror("Error", "Transaction not found or API limit exceeded.")
        return

    # Display basic transaction information
    output_textbox.insert(tk.END, f"Transaction Hash: {transaction['hash']}\n")
    output_textbox.insert(tk.END, f"Total BTC sent: {transaction['total']/10**8} BTC\n")
    output_textbox.insert(tk.END, f"Number of Inputs: {len(transaction['inputs'])}\n")
    output_textbox.insert(tk.END, f"Number of Outputs: {len(transaction['outputs'])}\n\n")

    # Trace previous transactions (inputs)
    if depth > 0:
        for input_data in transaction['inputs']:
            if 'prev_hash' in input_data:
                prev_tx_hash = input_data['prev_hash']
                output_textbox.insert(tk.END, f"Input from previous transaction: {prev_tx_hash}\n")
                # Recursive call to trace further transactions
                trace_transaction(prev_tx_hash, depth - 1)
            else:
                output_textbox.insert(tk.END, "No previous transaction (e.g., coinbase transaction)\n")
    
    output_textbox.insert(tk.END, "-"*50 + "\n")

# Function to handle GUI button click and start the tracing process
def start_trace():
    tx_hash = tx_hash_entry.get()
    if tx_hash:
        output_textbox.delete(1.0, tk.END)  # Clear the output box
        trace_transaction(tx_hash, depth=3)  # You can adjust the depth here
    else:
        messagebox.showwarning("Input Error", "Please enter a valid transaction hash.")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Bitcoin Transaction Tracer")

# Transaction hash label and input
tx_hash_label = tk.Label(root, text="Enter Bitcoin Transaction Hash:")
tx_hash_label.pack(pady=5)

tx_hash_entry = tk.Entry(root, width=50)
tx_hash_entry.pack(pady=5)

# Start tracing button
trace_button = tk.Button(root, text="Trace Transaction", command=start_trace)
trace_button.pack(pady=10)

# Output textbox to display tracing results
output_textbox = scrolledtext.ScrolledText(root, height=20, width=80)
output_textbox.pack(pady=10)

# Main loop for the GUI
root.mainloop()
