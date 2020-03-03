#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# jstevens, 2020-Feb-25, created functions
# jstevens, 2020-Mar-02, finished docstrings and comments
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object
saveFlag = 0    # save flag

# -- PROCESSING -- #
class DataProcessor:
    """Processing the data during runtime"""
 
    @staticmethod
    def write_row (idn, title, artist, table):
        """Function to write data as one dictionary row in a table

        Takes user input or data from a file and forms a dictionary row
        Then appends the row to the list of dictionaries 

        Args:
            idn (string): ID number of the CD, entered by user or read from file, saved as int()
            title (string): Title of the CD, entered by user or read from file, saved as string()
            artist (string): Artist of the CD, entered by user or read from file, saved as string()
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        dicRow = {'ID': int(idn), 'Title': title, 'Artist': artist}
        table.append(dicRow)
    

    @staticmethod
    def del_row (idndel, table):
        """Function to delete a CD row in a table

        Takes the user input of a ID number of the CD to be deleted
        Then deletes the matching row in the list of dictionaries 

        Args:
            idndel (int): ID number of the CD to be deleted, entered by user
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            cdremoved (boolean): Returns True if the ID of the CD was matched and removed or False if it was not matched
        """
        intRowNr = -1
        cdremoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == idndel:
                del table[intRowNr]
                cdremoved = True
                break
        return cdremoved


    @staticmethod
    def sort_table (table):
        """Function to sort the table

        Takes the table and sorts by ascending the ID value of the dictionaries in the list 

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            table (list): Returns the list sorted ascending by ID
        """
        table = sorted(table, key = lambda i: i['ID']) 
        return table
    

    @staticmethod
    def find_next_ID (table):
        """Function to find the next available ID number

        Takes the table and looks for the next ID number that has not been used by matching the ID value of each dict starting at 1 and ascending until no match is found

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            next_ID (int): Returns the number of the next available ID
        """
        intRowNr = 1
        checkrun = True
        for row in table:
            while checkrun:
                if intRowNr == row['ID']:
                    intRowNr = intRowNr + 1
                else:
                    next_ID = intRowNr
                    break
        return next_ID
    

    @staticmethod
    def check_ID (idnf, table):
        """Function to check if the user entered ID has been used 

        Takes the user entered ID number and the table and looks in the ID value to see if it has been used before in any of the dict in the table

        Args:
            idnf (int): ID number of the CD to be checked, entered by user
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            usedid (boolean): Returns True if the ID of the CD was matched or False if it was not matched
        """
        if any(row.get('ID') == int(idnf) for row in table):
            usedid = True       
        else:
            usedid = False     
        return usedid


# -- FILE HANDLING -- #
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            DataProcessor.write_row(data[0], data[1], data[2], table)
        objFile.close()


    @staticmethod
    def save_file(file_name, table):
        """Function to manage data degestion from a list of dictionaries to a file

        Writes the data from a 2D table to the file identified by file_name, table is sorted ascending by ID before saved
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to write the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        objFile = open(file_name, 'w')
        table=DataProcessor.sort_table(table) # sorts the table by id before save
        for row in table:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close()



# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def script_start(file_name, table):
        """Function that runs when the script is first loaded

        Calls the fuction that loads the data from file identified by file_name into a 2D table
        Then displays the file name that the data was loaded from and then calls the fuction to show the loaded 2D table

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        FileProcessor.read_file(file_name, table)
        print('The following CDs have been loaded from ' + file_name)
        IO.show_inventory(table) #show loaded inventory at start of script


    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """
        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')


    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice


    @staticmethod
    def load_inventory(file_name, table):
        """Function that will get user input to reload the inventory from a file

        Will ask for user confirmation then if received reload the inventory from the file by
        calling the fuction that loads the data from file identified by file_name into a 2D table
        then calls the fuction to show the loaded 2D table
        If the user chooses not to load then the user is returned to the main menu and shown the inventory

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(file_name, table)
            IO.show_inventory(table)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(table)


    @staticmethod
    def show_inventory(table):
        """Displays current inventory table with sorting

        Calls the fuction to sort the table then displays the table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        table=DataProcessor.sort_table(table)
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')


    @staticmethod
    def save_inventory(file_name, table):
        """Function to get user input to save the inventory to a file

        Call the show inventory fuction then ask for user input to save the file, 
        if received then call the function to save the file and set and return the saveFlag,
        if not received then return to the main menu.

        Args:
            file_name (string): name of file used to save the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            saveFlag (int): Returns the saveFlag as 0 to reset if file is saved
        """
        IO.show_inventory(table)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        if strYesNo == 'y':
           FileProcessor.save_file(file_name, table)
           saveFlag = 0
           return saveFlag
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')


    @staticmethod
    def add_cd(table):
        """Add a CD to the current inventory table

        Calls the fuction to show the next available ID and displays it, then asks for user input for the ID,
        when received then calls the Check_ID function, if the ID was used then display and start the add_cd function again.
        If the ID was not used then get user input for the title and artist and call the fuction to write the cd to the table,
        set the saveFlag to 1 and call the fuction to show the inventory with the added CD.

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            saveFlag (int): Returns the saveFlag as 1 if a CD was saved.
        """
        next_ID = DataProcessor.find_next_ID(table)
        print('The next available ID is: ' + str(next_ID))
        strID = input('Enter ID: ').strip()
        usedid = DataProcessor.check_ID(strID, table)
        if usedid == True:
            print('That ID is already being used, Please try again!')
            IO.add_cd(table)
        else:
            strTitle = input('What is the CD\'s title? ').strip()
            stArtist = input('What is the Artist\'s name? ').strip()
            DataProcessor.write_row(strID, strTitle, stArtist, table)
            saveFlag = 1
            print('The CD was added')
            IO.show_inventory(table)
            return saveFlag


    @staticmethod
    def del_cd(table):
        """Delete a CD from the current inventory table

        Calls the fuction to show the current inventory, then asks for user input for the ID of the CD to be deleted,
        when received then calls the del_row function, if the CD was deleted then set the display and set the the saveFlag to 1.
        If the CD was not deleted then display, after then show the current inventory.

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            saveFlag (int): Returns the saveFlag as 1 if a CD was removed.
        """
        IO.show_inventory(table)
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        blnCDRemoved = DataProcessor.del_row(intIDDel, table)
        if blnCDRemoved:
            saveFlag = 1
            print('The CD was removed')
            IO.show_inventory(table)
            return saveFlag
        else:
            print('Could not find this CD!')
            IO.show_inventory(table)
        

    @staticmethod
    def exit_script():
        """Fuction that handles exiting the script

        Checks the SaveFlag, if 1 then prompts the user for confirmation to exit without saving
        otherwise exits the script.

        Args:
            None.

        Returns:
            None.
        """
        if saveFlag == 1:
            userexit = (input ("You have not saved the list yet,\nto exit without saving type 'exit'\nor press enter to continue "))
            if userexit.lower() == 'exit':
                print('Goodbye!')
                quit()
            else:
                print("Please Save your List!")
                print()
        else:
            print('Goodbye!')
            quit()

# 1. When program starts, read in the currently saved Inventory
IO.script_start(strFileName, lstTbl) 
# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection

    # 3.1 process exit first
    if strChoice == 'x':
        IO.exit_script()
    # 3.2 process load inventory
    if strChoice == 'l':
        IO.load_inventory(strFileName, lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        saveFlag = IO.add_cd(lstTbl)      
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        saveFlag = IO.del_cd(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        saveFlag = IO.save_inventory(strFileName, lstTbl)
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




