Instructions to run the main program
1) python3 main.py arg1 arg2
-> arg1 is an integer and can take two values
   0 : Means that only a single file path will be given
   1 : Means file path to a directory will be given
-> arg2 is the path to the file or directory

Sample command :  python3 main.py 0 images/Book-Cover2.jpeg

All the output is printed on the terminal ( Title of the Book, Authors of the Book, publishers of the book, ISBN number of the book )
You can also view the output in the output.ods file ( Excel Sheet )

If you want to change the output file to a differently named file, change the name in the config file

Instructions to run the unit tests
1) coverage run -m pytest test_main.py
2) coverage report -m -i

