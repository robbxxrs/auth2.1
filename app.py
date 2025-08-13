import os
import sys
import json
import socket
import random
import string
from colorama import Fore, Style, init
import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet

init(autoreset=True)

def load_key_from_enc_file(enc_filepath, master_key):
    try:
        cipher = Fernet(master_key.encode())
        with open(enc_filepath, 'rb') as f:
            encrypted_data = f.read()
        decrypted = cipher.decrypt(encrypted_data)
        return decrypted
    except Exception as e:
        print(f"{Fore.RED}Failed to decrypt {enc_filepath}: {e}{Style.RESET_ALL}")
        sys.exit(1)

def load_db_config():
    master_key = 'DHPVRS8-vivnViNBGE6J8ioP2DmNDSPJsiff1vRD4mA='
    if not master_key:
        print(f"{Fore.RED}Environment variable MASTER_KEY not set!{Style.RESET_ALL}")
        sys.exit(1)

    db_config_key_bytes = load_key_from_enc_file('data/key.enc', master_key)
    db_config_key = db_config_key_bytes.decode()

    try:
        cipher_db = Fernet(db_config_key.encode())
        with open('data/core.enc', 'rb') as f:
            encrypted_db_config = f.read()
        decrypted_db_config = cipher_db.decrypt(encrypted_db_config)
        db_config = json.loads(decrypted_db_config.decode())
        return db_config
    except Exception as e:
        print(f"{Fore.RED}Failed to decrypt core.enc: {e}{Style.RESET_ALL}")
        sys.exit(1)

DB_CONFIG = load_db_config()

def generate_private_key():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=15))

def get_ip_address():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except Exception:
        return 'Unknown'

def print_header():
    ascii_art = r"""
  _____       _     _                                             
 |  __ \     | |   | |                       /\                   
 | |__) |___ | |__ | |__   ___ _ __ ___     /  \   _ __ ___  __ _ 
 |  _  // _ \| '_ \| '_ \ / _ \ '__/ __|   / /\ \ | '__/ _ \/ _` |
 | | \ \ (_) | |_) | |_) |  __/ |  \__ \  / ____ \| | |  __/ (_| |
 |_|  \_\___/|_.__/|_.__/ \___|_|  |___/ /_/    \_\_|  \___|\__,_|
"""
    print(f"{Fore.CYAN}{Style.BRIGHT}{ascii_art}{Style.RESET_ALL}")
    print(f"")
    print(f"{Fore.WHITE}Licensed and Created by @{Fore.YELLOW}Robbers Area Foundations{Style.RESET_ALL}")
    print(f"{Fore.WHITE}© 2025 RobbersArea. All rights reserved.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'-'*50}{Style.RESET_ALL}")

def save_to_database(email, username, ip_address, private_key):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            cursor = conn.cursor()

            check_query = "SELECT COUNT(*) FROM user_keys WHERE email = %s OR username = %s"
            cursor.execute(check_query, (email, username))
            count = cursor.fetchone()[0]

            if count > 0:
                print(f"{Fore.RED}Email or Username already exists. Cannot create duplicate entry.{Style.RESET_ALL}")
                cursor.close()
                conn.close()
                return

            sql = """
                INSERT INTO user_keys (email, username, ip_address, private_key)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (email, username, ip_address, private_key))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"{Fore.GREEN}Data successfully saved to the database.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}(Debug) Failed to connect to the MySQL database.{Style.RESET_ALL}")
    except Error as e:
        print(f"{Fore.RED}Failed to save data to database: {e}{Style.RESET_ALL}")

def create_private_key_flow():
    print(f"\n{Fore.YELLOW}-- Create Private Key --{Style.RESET_ALL}")
    
    while True:
        email = input(f"{Fore.CYAN}Enter your email: {Style.RESET_ALL}").strip()
        if not email.endswith("@gmail.com"):
            print(f"{Fore.RED}Only @gmail.com addresses are allowed! Please try again.{Style.RESET_ALL}")
        else:
            break

    username = input(f"{Fore.CYAN}Enter your username: {Style.RESET_ALL}").strip()
    ip_address = get_ip_address()
    private_key = generate_private_key()

    print(f"\n{Fore.CYAN}{'='*20} User Data {'='*20}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Email: {Fore.GREEN}{email}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Username: {Fore.GREEN}{username}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}IP Address: {Fore.GREEN}{ip_address}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}Private Key (15 chars):{Style.RESET_ALL}\n")
    print(f"{Fore.WHITE}{private_key}{Style.RESET_ALL}")

    save_to_database(email, username, ip_address, private_key)

def check_valid_key_flow():
    print(f"\n{Fore.YELLOW}-- Check Stored Keys --{Style.RESET_ALL}")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print(f"{Fore.GREEN}[DEBUG] Connected to MySQL database successfully.{Style.RESET_ALL}")
            cursor = conn.cursor()
            cursor.execute("SELECT email, username, ip_address, private_key, created_at FROM user_keys")
            rows = cursor.fetchall()
            if not rows:
                print(f"{Fore.RED}No private key data found in the database.{Style.RESET_ALL}")
            else:
                for r in rows:
                    print(f"{Fore.WHITE}Email: {Fore.GREEN}{r[0]}{Style.RESET_ALL}, Username: {Fore.GREEN}{r[1]}{Style.RESET_ALL}, IP: {Fore.GREEN}{r[2]}{Style.RESET_ALL}, Private Key: {Fore.YELLOW}{r[3]}{Style.RESET_ALL}, Created At: {Fore.CYAN}{r[4]}{Style.RESET_ALL}")
            cursor.close()
            conn.close()
        else:
            print(f"{Fore.RED}[DEBUG] Failed to connect to the MySQL database.{Style.RESET_ALL}")
    except Error as e:
        print(f"{Fore.RED}Failed to read data from database: {e}{Style.RESET_ALL}")

def check_specific_key_flow():
    print(f"\n{Fore.YELLOW}-- Check Private Key --{Style.RESET_ALL}")
    key_input = input(f"{Fore.CYAN}Enter the private key to search: {Style.RESET_ALL}").strip()

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            cursor = conn.cursor()
            query = "SELECT email, username, created_at FROM user_keys WHERE private_key = %s"
            cursor.execute(query, (key_input,))
            result = cursor.fetchone()
            if result:
                print(f"\n{Fore.GREEN}Private key found in database!{Style.RESET_ALL}")
                print(f"{Fore.WHITE}Email: {Fore.GREEN}{result[0]}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}Username: {Fore.GREEN}{result[1]}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}Created At: {Fore.CYAN}{result[2]}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Private key not found in the database.{Style.RESET_ALL}")
            cursor.close()
            conn.close()
        else:
            print(f"{Fore.RED}[DEBUG] Failed to connect to the MySQL database.{Style.RESET_ALL}")
    except Error as e:
        print(f"{Fore.RED}Database error: {e}{Style.RESET_ALL}")

def show_about():
    print(f"\n{Fore.YELLOW}-- About This Program --{Style.RESET_ALL}")
    print(f"{Fore.WHITE}This tool allows you to generate a secure 15-character private key, to access some resources")
    print(f"{Fore.WHITE}Every Information stored with associated user data (Email, Username, IP)")
    print(f"{Fore.WHITE}and managed with secure environment.")
    print(f"{Fore.GREEN}Version:{Style.RESET_ALL} 1.0")
    print(f"{Fore.GREEN}Author:{Style.RESET_ALL} RobbersArea\n")

def print_footer():
    print(f"{Fore.GREEN}{'-'*50}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Licensed and Created by {Fore.YELLOW}Robbers Area Foundations{Style.RESET_ALL}")
    print(f"{Fore.WHITE}© 2025 RobbersArea. All rights reserved.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'-'*50}{Style.RESET_ALL}")

def main():
    print_header()

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print(f"")
            print(f"{Fore.GREEN}[//] Successfully Connected to the servers!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[//] Environment are Secured!{Style.RESET_ALL}")
            print(f"")
            print(f"{Fore.GREEN}{'-'*50}{Style.RESET_ALL}")
            conn.close()
        else:
            print(f"{Fore.RED}[!] Failed to connect to the MySQL servers{Style.RESET_ALL}")
    except Error as e:
        print(f"{Fore.RED}[!] Server Problems (Database Connection Error): {e}{Style.RESET_ALL}")

    while True:
        print("\nMenu:")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Create Private Key")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Check Stored Keys")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Check Specific Private Key")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} About")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Exit")

        choice = input(f"{Fore.YELLOW}Choose an option (1-5): {Style.RESET_ALL}").strip()

        if choice == '1':
            create_private_key_flow()
        elif choice == '2':
            check_valid_key_flow()
        elif choice == '3':
            check_specific_key_flow()
        elif choice == '4':
            show_about()
        elif choice == '5':
            print(f"{Fore.GREEN}Thanks for using this program!{Style.RESET_ALL}")
            print_footer()
            sys.exit(0)
        else:
            print(f"{Fore.RED}Invalid option, please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()