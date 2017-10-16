from flask import Flask, render_template, request, redirect, session, flash
import re
import md5 
password = 'password'
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app,'logindb')


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html') 


@app.route('/login_page')
def login():
	return render_template('success.html') 

# after LOG IN
@app.route('/login', methods=['post'])
def longinprocess():
	email = request.form['email']
	password = md5.new(request.form['password']).hexdigest()
	user_query = "SELECT * FROM logins where logins.email = :email"
	query_data = { 'email': email}
	user = mysql.query_db(user_query, query_data)

	print user
	EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
	# invalid email
	if len(request.form['email'])<1:
		flash("Valid Email format!")
		return redirect('/login_page')
	# email doesn't exists
	elif len(request.form['password']) <1:
		flash("no password")
		return redirect('/login_page')
	# invalid user
	elif  not user:
		flash("Wrong email")
		return redirect('/login_page')
	# invalid password
	elif user[0]['password'] != password:
		flash("Wrong password")
		return redirect('/login_page')
	# correct info
	else:
		session['id'] = user[0]['id']
		return redirect ('/welcome')


# # Displaying Results
@app.route('/register', methods=['POST'])
def takeResults():
	fname = request.form['first_name']
	lname = request.form['last_name']
	email = request.form['email']
	password = request.form['password']
	confirmpw = request.form['confirm']
	regex = re.compile(r'^[^\W_]+(-[^\W_]+)?$', re.U)

	EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
	# invalid first name
	if len(fname)<2 or fname.isalpha() == False:
		flash("First name has to have at least two alphabetic characters ")
		return redirect('/')
	# invalid last name
	elif len(lname)<2 or not regex.match(lname):
		flash("Last name has to have at least two alphabetic characters ")
		return redirect('/')
	# invail email
	elif len(request.form['email']) < 1 or not EMAIL_REGEX.match(request.form['email']):
		flash("Inalid Email format!")
		return redirect('/')
	# invalid password
	elif len(password) <1:
		flash("blank")
	elif password != confirmpw:
		flash("Passwords are not matching!")
		return redirect('/')
	# correct info 
	else:

		password = md5.new(request.form['password']).hexdigest()
        # we want to insert into our query.
		query = "INSERT INTO logins (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)"
        # We'll then create a dictionary of data from the POST data received.
        data = {
				'first_name': request.form['first_name'],
				'last_name': request.form['last_name'],
				'email': request.form['email'],
				'password': password
			}
        # Run query, with dictionary values injected into the query.
        mysql.query_db(query,data)
        return redirect('/welcome')


@app.route('/welcome')
def success():
    return render_template("welcome.html")



app.run(debug=True)