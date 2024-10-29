from flask import Flask, request, jsonify, render_template, url_for, redirect, make_response, flash
import jwt
import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '14a0458f42584319bdeed320286f6dd5'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask-midterm'

#file-upload
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

mysql = MySQL(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def protected_route(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.form.get('x-access-token')
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if data.get('role') != 'admin':
                return jsonify({'message': 'Admin access required!'}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@app.route('/get-users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM test")
    data = cur.fetchall()
    cur.close()
    return jsonify({'users':data})

@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()

    if auth and auth.get('username') == 'admin' and auth.get('password') == 'password':
        token = jwt.encode({
            'username': auth['username'],
            'role': 'admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Token expires in 30 minutes
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/update-book', methods=['PUT'])

@app.route('/add-book', methods=['POST'])
@protected_route
def add_book():
    cur = mysql.connection.cursor()
    data = request.get_json()
    cur.execute("INSERT INTO books (id, name, description) VALUES (%s, %s, %s)", (data['id'], data['name'], data['description']))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Book added!', 'data': data})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload-file', methods=['POST'])
@protected_route
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash("No file part", "error")
        return redirect(url_for('upload'))
    
    file = request.files['file']

    if file.filename == '':
        flash("No selected file", "error")
        return redirect(url_for('upload'))

    if file and allowed_file(file.filename):

        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash("File uploaded successfully!", "success")
        return redirect(url_for('upload'))

    flash("File type not allowed", "error")
    return redirect(url_for('upload'))
@app.errorhandler(413)
def request_entity_too_large(error):
    flash("File is too large. Maximum allowed size is 16 MB.", "error")
    return redirect(url_for('upload'))


if __name__ == '__main__':
    app.run(debug=True)