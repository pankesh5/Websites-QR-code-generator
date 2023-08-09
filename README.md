# qr_automation
Generating website QR code through API simultaniously.

QR code generation application that allows users to generate QR codes for websites by using text input to provide the website name. The application uses various
libraries and modules such as qrcode, requests, PIL, tkinter and customtkinter to achieve its functionalities.The application begins with a HomePage where
users can choose to either register or login to access the QR code generation feature. The Home Page also displays a dynamic welcome message animation.

Users can switch between light and dark themes using the Mode switch on every page. If a user chooses to register, they are taken to the Register Page where they 
need to provide their name, email id, password, and retype the password. The script checks for existing entries in the database to ensure unique user details.
If the registration is successful, the user is taken to the Login Page. If a user chooses to login, they are taken to the Login Page where they need to enter
their registered email id and password. The script verifies the entered credentials with the database and, if successful, takes the user to the QR Page.

**The QR Page allows the user to input a website name using a text entry box. The application uses the Google Custom Search API to find the URL of the website 
related to the input. Then, it generates a QR code for that URL using the qrcode library and displays it on the page using matplotlib. Additionally, the user can
choose to support the project by either providing payment details or contacting the developers via email.**

**To make it more accessible and user-friendly, we can convert the Python script into an executable (EXE) format using a tool called AutoPYtoEXE. AutoPYtoEXE is a
graphical user interface (GUI) tool that simplifies the process of freezing Python scripts into standalone executables.**

Overall, this QR code generation application offers a user-friendly interface with text input, dynamic welcome animations, and the ability to switch between
light and dark themes. It provides users with convenient registration, login, and password recovery options while creating QR codes for websites with ease.
The application demonstrates the usage of various libraries and integrates well with a database for user management.
