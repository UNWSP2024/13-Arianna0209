# Title: Phonebook
# Author: Arianna Endres
# Date: 12/5/2025

# This program allows users to read, update, and delete data from the phonebook database in a GUI window.

import sqlite3

import tkinter

import tkinter.messagebox

# Connect to the database.
conn = sqlite3.connect('phonebook.db')

# Create the cursor.
cursor = conn.cursor()

class PhonebookListGUI:
    def __init__(self):
        # Create and title the main window.
        self.main_window = tkinter.Tk()
        self.main_window.title('Phonebook')

        # Add the user prompt.
        self.prompt = tkinter.Label(self.main_window, text='Select an entry to modify or delete it, '
                                                      'or click "add entry" to add a new entry.')


        # Set up the phonebook list:
        # Add column labels.
        self.column_labels = tkinter.Label(self.main_window, text=f'{'ID':^14}\t{'Name':<90}{'Phone Number':<18}')

        # Create the phonebook list frame.
        self.phonebook_listbox_frame = tkinter.Frame(self.main_window)

        # Create the phonebook list (using fixed font so the columns stay in line).
        self.phonebook_listbox = tkinter.Listbox(self.phonebook_listbox_frame, font='TkFixedFont', width=50, height=13)

        # Pack the list.
        self.phonebook_listbox.pack()


        # Fill the phonebook list:
        # Select all the data from the entries table.
        cursor.execute('''SELECT * FROM Entries''')

        # Fetch the data and assign it the "phonebook" variable.
        self.phonebook = cursor.fetchall()

        # Iterate through each row in the phonebook and add it to the listbox.
        for row in self.phonebook:
            self.phonebook_listbox.insert(tkinter.END, f'{row[0]:<5}{row[1]:<30}{row[2]:>15}')


        # Create the buttons:
        # Create a frame for the buttons that will manipulate the data.
        self.button_frame = tkinter.Frame(self.main_window)

        # Create the add, modify, and delete buttons, which redirect the program to their respective functions.
        self.add_button = tkinter.Button(self.button_frame, text='Add Entry', command=self.add_entry_window)
        self.modify_button = tkinter.Button(self.button_frame, text='Modify Entry', command=self.modify_entry_window)
        self.delete_button = tkinter.Button(self.button_frame, text='Delete Entry', command=self.deletion_confirmation)

        # Pack the buttons.
        self.add_button.pack(side='left', padx=5)
        self.modify_button.pack(side='left', padx=5)
        self.delete_button.pack(side='left', padx=5)

        # Create the quit button.
        self.quit_button = tkinter.Button(self.main_window, text='Quit', command=self.end_program_confirmation)

        # Pack all the widgets.
        self.prompt.pack(pady=5)
        self.column_labels.pack()
        self.phonebook_listbox_frame.pack(padx=15, pady=(0, 10))
        self.button_frame.pack(padx=5, pady=5)
        self.quit_button.pack(padx=5, pady=5)

        # Call the tkinter mainloop.
        tkinter.mainloop()

    # Define the function that allows the user to add an entry to the database:
    # Define the function that creates the window and asks for input.
    def add_entry_window(self):
        # Define the function that uses that input to add data to the database.
        def add_entry():
            # Get the name and phone number input.
            name = name_entry.get()
            phone_number = phone_number_entry.get()

            # Make sure the user entered data in both fields before proceeding, if so:
            if name != '' and phone_number != '':
                # Insert the data into the database and commit the changes.
                cursor.execute('''INSERT INTO Entries (Name, PhoneNumber) VALUES (?, ?)''', (name, phone_number))
                conn.commit()

                # Select the entry from the database to keep the formatting the same as the other items in the listbox.
                cursor.execute('''SELECT * FROM Entries WHERE EntryID = (SELECT MAX(EntryID) FROM Entries)''')

                # Fetch the entry.
                row = cursor.fetchone()

                # Insert the entry into the phonebook list and listbox.
                self.phonebook_listbox.insert(tkinter.END, f'{row[0]:<5}{row[1]:<30}{row[2]:>15}')
                self.phonebook.append(row)

                # Provide a confirmation that the data was successfully entered.
                tkinter.messagebox.showinfo('Entry Added', 'Entry successfully added')

                # Close the add window.
                add_window.destroy()

            # If the user left one or both fields blank, show and error messagebox and ask them to re-enter.
            else:
                tkinter.messagebox.showerror('Error', 'Please enter a name and phone number.')

        # Create the window that will ask for input.
        add_window = tkinter.Toplevel(self.main_window)

        # Provide an instruction label telling the user what to do.
        instructions = tkinter.Label(add_window, text='Add an entry by typing in a name and phone number in'
                                                      '\nthe corresponding boxes below.'
                                                      '\nUse the following phone number format:'
                                                      '\n111-111-1111')

        # Create the name input section:
        # Create the name entry frame.
        name_frame = tkinter.Frame(add_window)

        # Create the name entry label.
        name_label = tkinter.Label(name_frame, text='Name')

        # Create the input box.
        name_entry = tkinter.Entry(name_frame)

        # Pack the label and entry widgets.
        name_label.pack(side='left')
        name_entry.pack(side='left')


        # Create the phone number input section:
        # Create the phone number entry frame.
        phone_number_frame = tkinter.Frame(add_window)

        # Create the phone number entry label.
        phone_number_label = tkinter.Label(phone_number_frame, text='Phone Number')

        # Create the input box.
        phone_number_entry = tkinter.Entry(phone_number_frame)

        # Pack the label and entry widgets.
        phone_number_label.pack(side='left')
        phone_number_entry.pack(side='left')


        # Create the button section:
        # Create a frame.
        button_frame = tkinter.Frame(add_window)

        # Create the add button, which redirects the program to the add_entry function,
        # which will add the entry to the database.
        add_button = tkinter.Button(button_frame, text='Add', command=add_entry)

        # Create the cancel button, which destroys the add window.
        cancel_button = tkinter.Button(button_frame, text='Cancel', command=add_window.destroy)

        # Pack the buttons.
        add_button.pack(side='left', padx=5)
        cancel_button.pack(side='left', padx=5)

        # Pack all the widgets.
        instructions.pack()
        name_frame.pack(pady=(5, 0))
        phone_number_frame.pack(pady=(0, 5))
        button_frame.pack(pady=5)


    # Define the function that allows the user to modify data in the database:
    # Define the function that creates the window.
    def modify_entry_window(self):
        # Define the function that performs the modification.
        def modify_entry():
            # Get the primary key (aka the index for the database) for the entry in the database
            # (index is defined in the modify_entry_window function).
            db_index = int((self.phonebook_listbox.get(index)).split(' ')[0])

            # Get the name and phone number input.
            name = name_entry.get()
            phone_number = phone_number_entry.get()

            # Update the name in the database entry if the user enters a name.
            if name != '':
                cursor.execute('''UPDATE Entries SET Name=? WHERE EntryID=?''', (name, db_index))

            # Update the phone number in the database entry if the user enters one.
            elif phone_number != '':
                cursor.execute('''UPDATE Entries SET PhoneNumber=? WHERE EntryID=?''', (phone_number, db_index))

            # If the user leaves both fields blank:
            else:
                # Show an error message asking them to fill in at lease one of the fields.
                tkinter.messagebox.showerror('Error', 'Please enter a name and/or phone number.')

                # Exit the modify_entry function to allow the user to try again.
                return

            # Commit the database changes.
            conn.commit()

            # Select the entry from the database to keep the formatting the same as the other items in the listbox.
            cursor.execute('''SELECT * FROM Entries WHERE EntryID = ?''', (db_index,))

            # Fetch the row.
            row = cursor.fetchone()

            # Delete the corresponding listbox and phonebook list item.
            self.phonebook_listbox.delete(index)
            del self.phonebook[index]

            # Replace the deleted listbox and phonebook list item with a new one containing the updated data.
            self.phonebook_listbox.insert(index, f'{row[0]:<5}{row[1]:<30}{row[2]:>15}')
            self.phonebook.insert(index, row)

            # Provide a confirmation that the data was successfully entered.
            tkinter.messagebox.showinfo('Entry Modified', 'Entry successfully modified')

            # Close the modify window.
            modify_window.destroy()


        # Make sure the user chose an entry to modify, otherwise an error will occur:
        # Get the user's selection.
        selection = self.phonebook_listbox.curselection()

        # Ensure the selection is not an empty tuple. If not:
        if selection != ():
            # Get the index of the selection - this will turn the curselection from a tuple to an integer.
            index = selection[0]

        # If the user did not make a selection:
        else:
            # Create an error messagebox asking the user to select an entry.
            tkinter.messagebox.showerror('Error', 'Please select an entry to modify.')

            # Exit the function so the user can make a selection.
            return


        # Create a window that will allow the user to enter a new name and/or phone number.
        modify_window = tkinter.Toplevel(self.main_window)

        # Add instructions to tell the user what to do.
        instructions = tkinter.Label(modify_window, text='Modify the following entry by typing in a different name'
                                                         '\nand/or a different phone number in the corresponding boxes below.'
                                                         '\nUse the following phone number format:'
                                                         '\n111-111-1111')

        # Show the current name and phone number to the user so they know what they're changing.
        current_info = tkinter.Label(modify_window, text=f'Current name: {(self.phonebook[index])[1]} '
                                                         f'\nCurrent phone number: {(self.phonebook[index])[2]}')

        # Create the name input section:
        # Create the frame.
        name_frame = tkinter.Frame(modify_window)

        # Create the label for the entry box.
        name_label = tkinter.Label(name_frame, text='New name')

        # Create the entry box.
        name_entry = tkinter.Entry(name_frame)

        # Pack the label and entry widgets.
        name_label.pack(side='left')
        name_entry.pack(side='left')


        # Create the phone number input section:
        # Create the frame.
        phone_number_frame = tkinter.Frame(modify_window)

        # Create the label for the entry box.
        phone_number_label = tkinter.Label(phone_number_frame, text='New phone number')

        # Create the entry box.
        phone_number_entry = tkinter.Entry(phone_number_frame)

        # Pack the label and entry widgets.
        phone_number_label.pack(side='left')
        phone_number_entry.pack(side='left')


        # Create the buttons:
        # Create a frame for the buttons.
        button_frame = tkinter.Frame(modify_window)

        # Create a modify button that redirects the program to the function that will modify the entry.
        modify_button = tkinter.Button(button_frame, text='Modify', command=modify_entry)

        # Create a cancel button that will close the modify window.
        cancel_button = tkinter.Button(button_frame, text='Cancel', command=modify_window.destroy)

        # Pack the buttons.
        modify_button.pack(side='left', padx=5)
        cancel_button.pack(side='left', padx=5)


        # Pack all the widgets.
        instructions.pack(padx=10, pady=5)
        current_info.pack(pady=5)
        name_frame.pack(pady=(8, 0))
        phone_number_frame.pack(pady=(0, 10))
        button_frame.pack(pady=5)

    # Define the function that allows the user to delete data in the database:
    # Define the confirmation window in case the user misclicks.
    def deletion_confirmation(self):
        # Define the function that removes the entry from the database and listbox.
        def delete_entry():
            # Get the primary key (aka the index for the database) for the entry in the database
            # (index is defined in the deletion_confirmation function).
            db_index = int((self.phonebook_listbox.get(index)).split(' ')[0])

            # Delete the entry from the database and commit the change.
            cursor.execute('''DELETE FROM Entries WHERE EntryID=?''', (db_index,))
            conn.commit()

            # Delete the entry from the phonebook list and listbox.
            self.phonebook_listbox.delete(index)
            del self.phonebook[index]

            # Provide a confirmation that the data was successfully deleted.
            tkinter.messagebox.showinfo('Entry Deleted', 'Entry successfully deleted')

            # Close the deletion confirmation window.
            confirmation_window.destroy()


        # Make sure the user chose an entry to delete, otherwise an error will occur:
        # Get the user's selection.
        selection = self.phonebook_listbox.curselection()

        # Ensure the selection is not an empty tuple. If not:
        if selection != ():
            # Get the index of the selection - this will turn the curselection from a tuple to an integer.
            index = selection[0]

        # If the user did not make a selection:
        else:
            # Create an error messagebox asking the user to select an entry.
            tkinter.messagebox.showerror('Error', 'Please select an entry to delete.')

            # Exit the function so the user can make a selection.
            return

        # Create a window for the user to confirm their deletion in.
        confirmation_window = tkinter.Toplevel(self.main_window)

        # Add the label asking the user if they're sure they'd like to delete the entry.
        confirmation = tkinter.Label(confirmation_window, text='Are you sure you want to delete'
                                                     f'\n{self.phonebook[index]}')

        # Create the buttons for the user to select:
        # Create the button frame.
        button_frame = tkinter.Frame(confirmation_window)

        # Create a yes button, which will redirect the program to the delete_entry function.
        yes_button = tkinter.Button(button_frame, text='Yes', command=delete_entry)

        # Create a cancel button, which will close the confirmation window.
        cancel_button = tkinter.Button(button_frame, text='Cancel', command=confirmation_window.destroy)

        # Pack the buttons.
        yes_button.pack(side='left', padx=5)
        cancel_button.pack(side='left', padx=5)

        # Pack all the widgets.
        confirmation.pack(padx=5, pady=5)
        button_frame.pack(pady=5)


    # Define the function that will end the program when the user clicks quit:
    # Define the confirmation in case the user misclicks.
    def end_program_confirmation(self):
        # Define the function that will end the program.
        def end_program():
            # Close the database.
            conn.close()

            # Close the confirmation window.
            confirmation_window.destroy()

            # Close the main window.
            self.main_window.destroy()

        # Create the confirmation window.
        confirmation_window = tkinter.Toplevel(self.main_window)

        # Add a label asking the user if they're sure they want to quit.
        confirmation = tkinter.Label(confirmation_window, text='Are you sure you want to quit?')


        # Create the buttons:
        # Create a button frame.
        button_frame = tkinter.Frame(confirmation_window)

        # Create a yes button that will redirect the program to the end_program function.
        yes_button = tkinter.Button(button_frame, text='Yes', command=end_program)

        # Create a cancel button that will close the confirmation window.
        cancel_button = tkinter.Button(button_frame, text='Cancel',
                                       command=confirmation_window.destroy)

        # Pack the buttons.
        yes_button.pack(side='left', padx=5)
        cancel_button.pack(side='left', padx=5)


        # Pack all the widgets:
        confirmation.pack(padx=5, pady=5)
        button_frame.pack(pady=5)


# Call the main function.
if __name__== '__main__':
    # Create an instance of the PhonebookListGUI class.
    phonebook_list_gui = PhonebookListGUI()





