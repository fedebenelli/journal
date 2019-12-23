# journal

This little program will firstly ask for an username and password,all your journal entries will be saved according to that username and encrypted acording to the user's password, so make sure not to change it!

When adding an entry, use the string '\n' to add a new paragraph since pressing intro will just save your input until that point (you can still add a new entry afterwards if that happens)

When you compile your journal a \'journal.md\' file will me made, the content of this file can be compiled into a .pdf file with the software of your choice. (I use pandoc on Linux)

# To-do (I'm totally open to sugestions):
1. Add a title with the user's name and some kind of description at the start of the compiled file
2. Export the full_journal as a .html file (possible with markdown library)
