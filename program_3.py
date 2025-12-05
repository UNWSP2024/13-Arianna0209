# Title: Phonebook Database
# Author: Arianna Endres
# Date: 12/4/2025

# This program creates a phonebook database that stores names and related numbers.

import sqlite3

def main():
    # Connect to the database.
    conn = sqlite3.connect('phonebook.db')

    # Create the cursor.
    cursor = conn.cursor()

    # Create the entries table.
    cursor.execute('''CREATE TABLE Entries (EntryID INTEGER PRIMARY KEY NOT NULL, Name TEXT,
                    PhoneNumber INTEGER)''')

    # Commit the changes.
    conn.commit()

    # Close the database.
    conn.close()

# Call the main function.
if __name__ == '__main__':
    main()

