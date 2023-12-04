import tkinter as tk
from tkinter import messagebox
import threading
import rsa

class RSAApp:
    def __init__(self):
        # Generate keys
        p, q, e = rsa.make_p_q_e()
        self.public_key, self.private_key = rsa.make_key(p, q, e)

        # Create the application window
        self.window = tk.Tk()
        self.window.title("RSA Encryption/Decryption App")
        self.window.geometry()

        # Create the labels
        plaintext_label = tk.Label(self.window, text="Plaintext:")
        plaintext_label.grid(row=0, column=0, sticky="w")

        ciphertext_label = tk.Label(self.window, text="Ciphertext:")
        ciphertext_label.grid(row=2, column=0, sticky="w")

        # Create the entry fields
        self.plaintext_entry = tk.Text(self.window, font=('Arial', 12), height=10, width=30)
        self.plaintext_entry.grid(row=1, column=0, padx=10, pady=5)
        self.plaintext_entry.bind("<Control-a>", self.select_all_text)  # Bind Ctrl+A to select all text

        self.ciphertext_entry = tk.Text(self.window, font=('Arial', 12), height=10, width=30)
        self.ciphertext_entry.grid(row=3, column=0, padx=10, pady=5)
        self.ciphertext_entry.bind("<Control-a>", self.select_all_text)  # Bind Ctrl+A to select all text

        # Create the scrollbars
        plaintext_scrollbar = tk.Scrollbar(self.window, command=self.plaintext_entry.yview)
        plaintext_scrollbar.grid(row=1, column=1, sticky='ns')
        self.plaintext_entry.configure(yscrollcommand=plaintext_scrollbar.set)

        ciphertext_scrollbar = tk.Scrollbar(self.window, command=self.ciphertext_entry.yview)
        ciphertext_scrollbar.grid(row=3, column=1, sticky='ns')
        self.ciphertext_entry.configure(yscrollcommand=ciphertext_scrollbar.set)

        # Create the buttons
        encrypt_button = tk.Button(self.window, text="Encrypt", command=self.encrypt_data)
        encrypt_button.grid(row=1, column=2, padx=10, pady=5)

        decrypt_button = tk.Button(self.window, text="Decrypt", command=self.decrypt_data)
        decrypt_button.grid(row=3, column=2, padx=10, pady=5)

        clear_button = tk.Button(self.window, text="Clear", command=self.clear_data)
        clear_button.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    def encrypt_data(self):
        plaintext = self.plaintext_entry.get("1.0", tk.END)  # Update get method
        if plaintext:
            self.ciphertext_entry.delete("1.0", tk.END)  # Update delete method
            threading.Thread(target=self.perform_encryption, args=(plaintext,)).start()
        else:
            messagebox.showwarning("Empty Field", "Please enter some plaintext data.")

    def perform_encryption(self, plaintext):
        try:
            ciphertext = rsa.encryption(self.public_key, plaintext)
            self.ciphertext_entry.insert(tk.END, str(ciphertext))
            messagebox.showinfo("Encryption Success", "Encryption successful.")
        except:
            messagebox.showerror("Encryption Error", "Encryption failed. Please check the input data.")

    def decrypt_data(self):
        ciphertext = self.ciphertext_entry.get("1.0", tk.END)  # Update get method
        if ciphertext:
            self.plaintext_entry.delete("1.0", tk.END)  # Update delete method
            threading.Thread(target=self.perform_decryption, args=(ciphertext,)).start()
        else:
            messagebox.showwarning("Empty Field", "Please enter some ciphertext data.")

    def perform_decryption(self, ciphertext):
        try:
            plaintext = rsa.decrypt(self.private_key, eval(ciphertext))
            self.plaintext_entry.insert(tk.END, plaintext)
            messagebox.showinfo("Decryption Success", "Decryption successful.")
        except:
            messagebox.showerror("Decryption Error", "Decryption failed. Please check the input data.")

    def clear_data(self):
        self.plaintext_entry.delete("1.0", tk.END)
        self.ciphertext_entry.delete("1.0", tk.END)
        messagebox.showinfo("Clear Success", "Clear all data in the fields.")

    def select_all_text(self, event):
        event.widget.tag_add("sel", "1.0", "end-1c")
        return "break"

    def start(self):
        # Start the application
        self.window.mainloop()

# Create an instance of the RSAApp class and start the application
app = RSAApp()
app.start()