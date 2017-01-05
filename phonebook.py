"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import pg
from flask import Flask, render_template, request, redirect, url_for

import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

DBUSER = os.environ.get('DBUSER', True)
DBPASS = os.environ.get('DBPASS', True)
DBHOST = os.environ.get('DBHOST', True)
DBNAME = os.environ.get('DBNAME', True)


###
# Routing for your application.
###


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")


@app.route('/submit_login', methods=['POST', 'GET'])
def submit_login():
    username = request.form.get('username')
    password = request.form.get('password')
    query = db.query("select * from users where username = '%s'" % username)
    result_list = query.namedresult()
    if len(result_list) > 0:
        user = result_list[0]
        if user.password == password:
            session['name'] = user.name
            return redirect('/contacts')
        else:
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/logout_page')
def logout_page():
    return "<h1>Goodbye!</h1>"


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['name']
    return redirect('/')


@app.route('/contacts')
def contacts():
    db = pg.DB(host=DBHOST, user=DBUSER, passwd=DBPASS, dbname=DBNAME)
    contacts = db.query('select * from phonebook').namedresult()
    return render_template(
        'contacts.html',
        title='All Contacts',
        contacts=contacts
    )


@app.route('/new_contact')
def new_contact():
    return render_template(
        'new_contact.html',
        title='New Contact'
    )


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    db.insert('phonebook',
              name=name,
              phone_number=phone_number,
              email=email)
    return redirect('/contacts')


@app.route('/update_contact')
def update_contact():
    id = int(request.args.get('id'))
    query = db.query('''
    select * from phonebook
    where id = %d''' % id)
    contact = query.namedresult()[0]
    return render_template(
        'update_contact.html',
        contact=contact
    )


@app.route('/submit_update', methods=['POST'])
def submit_update():
    id = int(request.form.get('id'))
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    action = request.form.get('action')
    if action == 'update':
        db.update('phonebook', {
            'id': id,
            'name': name,
            'phone_number': phone_number,
            'email': email
        })
    elif action == 'delete':
        db.delete('phonebook', {'id': id})
    else:
        raise Exception("ERROR")
    return redirect('/contacts')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
