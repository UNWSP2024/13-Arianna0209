# Title: Minnesota Cities Database
# Author: Arianna Endres
# Date: 12/4/2025

# This program creates a database containing population information from 20 MN cities.

import sqlite3

def main():
    # Connect to the database.
    conn = sqlite3.connect('cities.db')

    # Create the cursor.
    cursor = conn.cursor()

    # Drop the table if it already exists so that the program can create a new
    # table each time it runs.
    cursor.execute('DROP TABLE IF EXISTS Cities')

    # Create the table with the CityID being the primary key that identifies each city, the CityName
    # being the name of the city, and the population being the population of the city.
    cursor.execute('''CREATE TABLE Cities (CityID INTEGER PRIMARY KEY NOT NULL,
                                            CityName TEXT, Population INTEGER)''')

    # Create a list containing a tuple with information about each city.
    cities_population = [(1, 'Minneapolis', 428579),
                         (2, 'Saint Paul', 307465),
                         (3, 'Rochester', 307465),
                         (4, 'Bloomington', 88344),
                         (5, 'Duluth', 87986),
                         (6, 'Brooklyn Park', 82893),
                         (7, 'Woodbury', 80596),
                         (8, 'Plymouth', 78551),
                         (9, 'Lakeville', 77971),
                         (10, 'Blaine', 75172),
                         (11, 'Maple Grove', 72739),
                         (12, 'St. Cloud', 72145),
                         (13, 'Eagan', 67240),
                         (14, 'Burnsville', 64864),
                         (15, 'Coon Rapids', 63807),
                         (16, 'Eden Prairie', 62905),
                         (17, 'Apple Valley', 55272),
                         (18, 'Edina', 53564),
                         (19, 'Minnetonka', 52651),
                         (20, 'St. Louis Park', 49899)]

    # Add the data from the above list into the database by iterating through each tuple and adding
    # each of its three elements.
    for entry in cities_population:
        cursor.execute('''INSERT INTO Cities (CityID, CityName, Population) VALUES (?, ?, ?)''',
                       (entry[0], entry[1], entry[2]))


    # Commit the changes.
    conn.commit()

    # Close the database.
    conn.close()

# Call the main function.
if __name__ == '__main__':
    main()