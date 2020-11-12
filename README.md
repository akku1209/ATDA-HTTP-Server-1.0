<h2 text-align='center'>ATDA HTTP SERVER 1.0</h2>

<h3>Supports following methods:</h3>

1. GET
2. POST
3. PUT
4. DELETE
5. HEAD

<h3>Steps for Running Server:</h3>

1. change working directory to the root of the project
2. change the permissions of /html/priv.html 
    >> chmod 300 /html/priv.html 
3. Configure the program by changing/ entering values in the server.config file <br />
    (if you dont enter values, server will run using the default values)

4. start the server by using command:
    >> python3 main.py [port_number]

5. Enter the menu option:
    a. to start server enter '1'
    b. to end program enter '3'
    (you cannot pause server without starting it)

6. Send request on 'http://127.0.0.1:[port_number]/[html_page]' <br />
    (you can choose htmls from html folder of your choice <br />
    a folder is already provided, but you can make your own <br />
    just make sure you enter the path of folder in the server.config file) <br />

7. you can check the logs in Log folder with levels of logging


<h3>For auto-testing:</h3>

1. Run the autotester.py program 
    >>python3 autotester.py
2. Press enter key for the report
3. Report will be created in Report folder

