from Encryption import encrypt_file, decrypt_file
from Database import log_action, view_logs
import os

def print_banner():
    print("""
╔══════════════════════════════════════╗
║       FILE ENCRYPTION SYSTEM        ║
║     Ethical Hacking - Semester 1    ║
╚══════════════════════════════════════╝
    """)

def main():
    print_banner()

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Encrypt a File")
        print("2. Decrypt a File")
        print("3. View Encryption Logs")
        print("4. Exit")
        print("================================")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            filepath = input("Enter the full path of the file to encrypt: ").strip()
            if not os.path.exists(filepath):
                print("[ERROR] File not found!")
                log_action(filepath, "ENCRYPT", "FAILED - File not found")
            else:
                password = input("Enter encryption password: ")
                result = encrypt_file(filepath, password)
                if result:
                    log_action(os.path.basename(filepath), "ENCRYPT", "SUCCESS")

        elif choice == "2":
            filepath = input("Enter the full path of the .enc file to decrypt: ").strip()
            if not os.path.exists(filepath):
                print("[ERROR] File not found!")
                log_action(filepath, "DECRYPT", "FAILED - File not found")
            else:
                password = input("Enter decryption password: ")
                result = decrypt_file(filepath, password)
                if result:
                    log_action(os.path.basename(filepath), "DECRYPT", "SUCCESS")
                else:
                    log_action(os.path.basename(filepath), "DECRYPT", "FAILED - Wrong password")

        elif choice == "3":
            view_logs()

        elif choice == "4":
            print("Goodbye! Stay secure 🔐")
            break

        else:
            print("[ERROR] Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()