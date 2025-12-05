# Title: Cities Display
# Author: Arianna Endres
# Date: 12/4/2025

import sqlite3

def main():
    # Connect to the "cities" database.
    conn = sqlite3.connect('cities.db')

    # Create the cursor.
    cursor = conn.cursor()

    # Print the heading.
    print('\nCities Database Contents:\n')

    # Select all columns in the Cities table.
    cursor.execute('''SELECT * FROM Cities''')

    # Set the data variable equal to the list containing all
    # the row values.
    data = cursor.fetchall()

    # Iterate through the list, printing each element of each tuple.
    for row in data:
        print(f'{row[0]:<3} {row[1]:<17} {row[2]:>8,}')

    # Close the database.
    conn.close()

# Call the main function
if __name__ == '__main__':
    main()