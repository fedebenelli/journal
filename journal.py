###########################################################################
#   Program:    Journal.py v0.5
#   Author:     Federico E. Benelli
#   Desc:       acá describiré algo, supongo
###########################################################################

###
#   # To-do:
#       1. Add a 'month subsection' to the compiled full journal, format should be '## <month>'
#       2. Export the full_journal as a .html file (possible with markdown library)
###

# import markdown
import ast
import sys, os
import getpass
from pathlib import Path
from datetime import datetime as dt
from datetime import date as get_datetime

version = 0.5

def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return encoded_string


def decode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string


# Definition of the date, in different formats
now = dt.now()

year     = now.strftime('%Y')
month    = now.strftime('%B')
date     = now.strftime('%a, %d %b')
hour     = now.strftime('%H:%M')
num_date = now.strftime('%Y-%m-%d')


# Get the script's path
path = os.path.abspath(sys.argv[0])[:-10]

# Print Welcome Message
print(f'''
Welcome to journal.py v {version}!

This little program will firstly ask for an username and password,
all your journal entries will be saved according to that username and
encrypted acording to the user's password, so make sure not to change it!

When adding an entry, use the string \'\\n' to add a new paragraph
since pressing intro will just save your input until that point
(you can still add a new entry afterwards if that happens)

When you compile your journal a \'journal.md\' file will me made,

''')

# Define the user
user     = input('Username: ')
password = getpass.getpass('Password: ')

action = input('Action: [add|compile|exit] -> ')

folder_path = Path(f'{path}/entries/{user}/')

aux_year = 0

# Unless the user tells the program to stop, it will remain open
while action != 'exit':

    # Adding a new journal entry
    if action == 'add':

        # First the entry is received and then the entry file is defined
        entry = input('\nJournal Entry: ')
        entry_file = folder_path / num_date

        # Try to open an already created file
        #   if the open works, the content is decoded
        #   the new entry is added
        #   lastly the whole text is encoded
        try:
            with open(entry_file, encoding='utf-8') as f:
                feed  = decode(password, f.read())
                feed += f'\n\n#### {hour}\n\n{entry}'
                feed  = encode(password, feed)
        
        # If the day's file still doesn't exist, just a new text is created,
        #   the text includes the file's header with the date, and the new entry
        #   finally the text is encoded
        except:
            feed=encode(password, '### '+date+f'\n\n#### {hour}\n\n{entry}')

        # Try to write the file, if the folder of the user still doesn't exist,
        #   it will give an error, so the folder is created on the ´except´ section.
        try:
            with open(entry_file, 'w', encoding='utf-8') as w:
                w.write(feed)
                print('\nEntry added!')

        except:
            os.mkdir(folder_path)
            with open(entry_file, 'w',encoding='utf-8') as w:
                w.write(feed)
                print('\nEntry added!')

    # Compiling all the files into a journal.md file
    if action=='compile':
        
        aux_year  = 0
        aux_month = 0
        # Definition of a string that will have all the data
        full_journal = ''

        # Iteration over each file,
        #   at each iteration the file's content is decoded and added to the journal string
        for filename in os.listdir(folder_path):
            with open(folder_path / filename,encoding='utf-8') as f:
                
                file_year = filename[0:4]
                file_month = filename[5:7]
                
                # Checks if it's opening the first file of the year,
                #  if it is, it will add a line with the year tag to
                #  the compiled file
                if file_year != aux_year:
                    full_journal += f'\n\n# {file_year}\n\n'
                    aux_year = file_year
                    
                # Same but with the month
                if file_month != aux_month:
                    print(file_month)
                    month_name = get_datetime(1900,int(file_month),1).strftime('%B')
                    full_journal +=f'\n\n## {month_name}\n\n'
                    aux_month = file_month
                
                full_journal += decode(password, f.read())
        
        # Printing the whole journal on the console
        print('\nFull Journal:\n'+full_journal)

        # Saving the whole journal into a journal.md file
        with open(path+'journal.md', 'w', encoding='utf-8') as w:
            w.write(full_journal)

    action=input('\nAction: [add|compile|exit] -> ')
