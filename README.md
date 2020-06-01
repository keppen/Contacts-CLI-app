# Contacts-CLI-app

Simple command line app that can be used to storage contacts details and arranging them into groups.

To install use 'pip install .'  or 'python setup.py' install when in contacts/ directiory. 
There are a couple modules that are needed to run this program. They can be installed by 'pip install -r reqfiles.txt' command.
It is recomended to intsall the app in virtual enviroment.

Once installed, the app can be evoked by typing 'contacts' in command line of termial.
For now, the app can create, update, delete and view items lplaced in libr.db database. It can not add contact to group yet.

Eg. to update a last name of an entry following command can be used: 'contacts udpate --what contact --entry 1'. 
Then the program will ask about details, what items name will be changed and the new name.

Using --help option is recomended.
