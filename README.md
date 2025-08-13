# Private Key Generator and Manager

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
- MySQL database with a `user_keys` table
- Encrypted configuration files (`data/key.enc` and `data/core.enc`)
- Environment variable `MASTER_KEY` for decryption

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   ```bash
   pip install mysql-connector-python colorama cryptography
   ```

3. **Set Up MySQL Database**:
   - Create a MySQL database and a table named `user_keys` with the following schema:
     ```sql
     CREATE TABLE user_keys (
         id INT AUTO_INCREMENT PRIMARY KEY,
         email VARCHAR(255) NOT NULL,
         username VARCHAR(255) NOT NULL,
         ip_address VARCHAR(50),
         private_key VARCHAR(50) NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```

4. **Prepare Encrypted Configuration Files**:
   - Create a `data` directory in the project root.
   - Generate a Fernet key for `MASTER_KEY` and set it as an environment variable:
     ```bash
     export MASTER_KEY='your-fernet-key-here'
     ```
   - Create `data/key.enc` and `data/core.enc` with encrypted database configuration (see `load_db_config` function for details).

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
- Ensure the `MASTER_KEY` environment variable is set before running the program.
- The program only accepts Gmail addresses (`@gmail.com`) for email input.
- Database errors are logged with detailed error messages for debugging.
- The `user_keys` table must exist in the MySQL database before running the program.

## License
© 2025 Robbers Area Foundations. All rights reserved.