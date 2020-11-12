ATDA HTTP SERVER 1.0

Supports following methods:
1. GET
2. POST
3. PUT
4. DELETE
5. HEAD

Steps for Running Server:
1. change working directory to the root of the project
2. change the permissions of /html/priv.html 
    >> chmod 300 /html/priv.html 
3. Configure the program by changing/ entering values in the server.config file
    (if you dont enter vlues, server will run using the default values)

4. start the server by using command:
    >> python3 main.py [port_number]

5. Enter the menu option:
    a. to start server enter '1'
    b. to end program enter '3'
    (you cannot pause server without starting it)

6. Send request on 'http://127.0.0.1:[port_number]/[html_page]'
    (you can choose htmls from html folder of your choice
    a folder is already provided, but you can make your own
    just make sure you enter the path of folder in the server.config file)

7. you can check the logs in Log folder with levels of logging


For auto-testing:
1. Run the autotester.py program 
    >>python3 autotester.py
2. Press enter key for the report
3. Report will be created in Report folder


For testing with customised inputs:(this test cant check maximum connections)
1. give the desired input in the input file (test_file.txt) in the given format
    the first line specifies number of connections
    METHOD;html
    (if no html is entered, index.html will be shown)
2. Run the server using the steps 1-3 
3. run the test.py program
    >>python3 test.py
4. give port number as input
