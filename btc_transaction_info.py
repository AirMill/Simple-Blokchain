import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import datetime

# Replace with your BlockCypher API Key
API_KEY = 'your_blockcypher_api_key'  # Sign up at BlockCypher to get a free API key
BASE_URL = "https://api.blockcypher.com/v1/btc/main"

# Function to get transaction details
def get_transaction(tx_hash):
    url = f"{BASE_URL}/txs/{tx_hash}?token={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to fetch and display transaction details
def display_transaction_details(tx_hash):
    output_textbox.delete(1.0, tk.END)  # Clear the output box
    transaction = get_transaction(tx_hash)
    
    if not transaction:
        messagebox.showerror("Error", "Transaction not found or API limit exceeded.")
        return

    # Display transaction hash and date
    output_textbox.insert(tk.END, f"Transaction Hash (TXID): {transaction['hash']}\n")
    if 'confirmed' in transaction:
        transaction_date = datetime.datetime.fromtimestamp(transaction['confirmed']).strftime('%Y-%m-%d %H:%M:%S')
        output_textbox.insert(tk.END, f"Date: {transaction_date}\n")
    else:
        output_textbox.insert(tk.END, "Date: Pending / Unconfirmed\n")
    
    # Display the total BTC sent
    total_btc = transaction['total'] / 10**8
    output_textbox.insert(tk.END, f"Total BTC Sent: {total_btc} BTC\n")
    
    # Display transaction fee
    fees = transaction.get('fees', 0) / 10**8
    output_textbox.insert(tk.END, f"Transaction Fee: {fees} BTC\n")
    
    # Display number of confirmations
    if 'confirmations' in transaction:
        output_textbox.insert(tk.END, f"Confirmations: {transaction['confirmations']}\n")
    else:
        output_textbox.insert(tk.END, "Confirmations: 0 (Unconfirmed)\n")
    
    # Block information
    if 'block_height' in transaction:
        output_textbox.insert(tk.END, f"Block Height: {transaction['block_height']}\n")
        output_textbox.insert(tk.END, f"Block Hash: {transaction.get('block_hash', 'N/A')}\n")
    else:
        output_textbox.insert(tk.END, "Block Height: N/A (Pending)\n")

    output_textbox.insert(tk.END, "-"*50 + "\n")
    
    # Inputs (sending addresses)
    output_textbox.insert(tk.END, "Inputs (Sending Addresses):\n")
    for input_data in transaction['inputs']:
        if 'addresses' in input_data:
            for address in input_data['addresses']:
                output_textbox.insert(tk.END, f" - {address}\n")
        if 'output_value' in input_data:
            sent_amount = input_data['output_value'] / 10**8
            output_textbox.insert(tk.END, f"   Amount Sent: {sent_amount} BTC\n")
    
    output_textbox.insert(tk.END, "-"*50 + "\n")
    
    # Outputs (receiving addresses)
    output_textbox.insert(tk.END, "Outputs (Receiving Addresses):\n")
    for output in transaction['outputs']:
        if 'addresses' in output:
            for address in output['addresses']:
                output_textbox.insert(tk.END, f" - {address}\n")
        output_amount = output['value'] / 10**8
        output_textbox.insert(tk.END, f"   Amount Received: {output_amount} BTC\n")
    
    output_textbox.insert(tk.END, "-"*50 + "\n")

# Function to handle the button click and start fetching transaction details
def fetch_transaction():
    tx_hash = tx_hash_entry.get().strip()
    if tx_hash:
        display_transaction_details(tx_hash)
    else:
        messagebox.showwarning("Input Error", "Please enter a valid transaction hash.")

# Tkinter GUI setup
root = tk.Tk()
root.title("Bitcoin Transaction Viewer")

# Label and input for the transaction hash
tx_hash_label = tk.Label(root, text="Enter Bitcoin Transaction Hash:")
tx_hash_label.pack(pady=5)

tx_hash_entry = tk.Entry(root, width=60)
tx_hash_entry.pack(pady=5)

# Button to start fetching the transaction details
fetch_button = tk.Button(root, text="Fetch Transaction Details", command=fetch_transaction)
fetch_button.pack(pady=10)

# Scrollable text box to display the transaction details
output_textbox = scrolledtext.ScrolledText(root, height=25, width=80)
output_textbox.pack(pady=10)

# Main loop for the GUI
root.mainloop()
