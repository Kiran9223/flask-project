# flask-project

CPSC 449 Web Backend Engineering 

Authors:\n Kiran Sukumar, kiransukumar@csu.fullerton.edu\n
         Hisham Panamthodi Kajahussain, hisham.pk@csu.fullerton.edu

Installation and setup:
Instal the packages listed in requirements.txt file in the terminal using pip install "package_name"

Database Configuration:
Configure the MySQL database using the below code
app.config['SECRET_KEY'] = 'Your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'db user name'
app.config['MYSQL_PASSWORD'] = 'db password'
app.config['MYSQL_DB'] = 'db name'

File upload configuration:
Configure the folder setup to store the file uploaded, file format/extension, size, etc. using below code
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'jpg', 'jpeg', 'png'}

Run the application:
In the terminal, run the following command: python app.py
The application will run on localhost port 5000

Endpoints:
![Uploading image.png…]()


