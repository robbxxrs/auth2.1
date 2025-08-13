# Auth 2.1

## Overview
This Python application generates and manages secure 15-character private keys, storing associated user data (email, username, IP address) in a MySQL database. It uses encrypted configuration files for secure database connections and provides a user-friendly command-line interface with colorized output.

## Features
- **Generate Private Keys**: Creates random 15-character private keys using a combination of letters and digits.
- **Database Integration**: Stores user data (email, username, IP address, private key) in a MySQL database with duplicate checks.
- **Key Validation**: Allows checking all stored keys or searching for a specific private key.
- **Secure Configuration**: Uses Fernet encryption to securely load database credentials from encrypted files.
- **User Interface**: Features a colorful ASCII art header and menu-driven interface using the `colorama` library.
- **IP Detection**: Automatically captures the user's IP address using socket programming.
- **About Section**: Displays program information, version, and author details.

## Requirements
- Python 3.x
- Required Python libraries:
  - `mysql-connector-python`
  - `colorama`
  - `cryptography`

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/robbxxrs/auth2.1
   cd auth2.1-main
   ```

2. **Install Dependencies**:
   ```bash
   pip install mysql-connector-python colorama cryptography
   ```

## Usage
1. Run the script:
   ```bash
   python main.py
   ```

2. Follow the menu prompts:
   - **Option 1**: Create a new private key (requires a Gmail address and username).
   - **Option 2**: View all stored keys in the database.
   - **Option 3**: Search for a specific private key.
   - **Option 4**: Display program information.
   - **Option 5**: Exit the program.

## Example Output
```
  _____       _     _
 |  __ \     | |   | |                       /\
 | |__) |___ | |__ | |__   ___ _ __ ___     /  \   _ __ ___  __ _
 |  _  // _ \| '_ \| '_ \ / _ \ '__/ __|   / /\ \ | '__/ _ \/ _` |
 | | \ \ (_) | |_) | |_) |  __/ |  \__ \  / ____ \| | |  __/ (_| |
 |_|  \_\___/|_.__/|_.__/ \___|_|  |___/ /_/    \_\_|  \___|\__,_|

Licensed and Created by @Robbers Area Foundations
© 2025 RobbersArea. All rights reserved.
--------------------------------------------------

[//] Successfully Connected to the servers!
[//] Environment are Secured!
--------------------------------------------------

Menu:
1. Create Private Key
2. Check Stored Keys
3. Check Specific Private Key
4. About
5. Exit
Choose an option (1-5):
```

## Notes
- The program only accepts Gmail addresses (`@gmail.com`) for email input.
- Database errors are logged with detailed error messages for debugging.

## License
© 2025 Robbers Area Foundations. All rights reserved.
