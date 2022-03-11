from os import error
import re
from flask import Flask, render_template, request, url_for, redirect, session
from functions.admin import contact_form,login_user, get_records, get_single_record, edit_record, delete_record, add_user, get_user

app = Flask(__name__)

app.secret_key = "IAN"

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/courses")
def courses():
    return render_template('courses.html')

@app.route("/documents")
def documents():
    return render_template('documents.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    message = ''
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        eaddress = request.form['eaddress']
        message = request.form['message']
        result = contact_form(fname, lname, eaddress, message)

        if result:
            return render_template('contact.html', message='Thank you for your submission')
        else:
            return render_template('contact.html', message='Error with submission')
    else:
        return render_template('contact.html', message=message)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    error = ''
    records = ''
    print(request)

    # If method was POST, a form was submitted
    if request.method == 'POST':

        # If the form was Login, perform log in steps
        if request.form.get('admin') == 'Login':
            username = request.form['username']
            password = request.form['password']

            # pass username and password from form to our login logic
            result = login_user(username, password)

            # If login was successful, create a session for the user, and load data, show data onpage
            if result:
                session['user_id'] = result
                records = get_records()
                # print(records)
            
            # login was not sucessful, show error message
            else:
                error = 'Invalid Username or Password'
        
        # if form was logout button, end user session
        elif request.form.get('admin')  == 'Logout':
            session.pop('user_id')

        
    # if user is logged in previously, show data. If no session, data is not retireved
    if 'user_id' in session:
        records = get_records()

    # return the admin page, showing any message or data that we may have
    return render_template('admin.html', error = error, records = records)

@app.route("/register", methods=['GET', 'POST'])
def register():
    
    error = False
    new_id = False

    # If user submiited form to add a user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if get_user(username):
            new_id = add_user(username, password)
            error = "Registration sucessful. Please login"
            return render_template('admin.html', error = error)
        else:
            error = f"Username {username} not available"
        

    return render_template('register.html', error = error, id = new_id)


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    msg_id = request.args['id']
    if request.method == 'POST':
        if request.form.get('edit') == 'save':
            fname = request.form['fname']
            lname = request.form['lname']
            eaddress = request.form['eaddress']
            message = request.form['message']
            print(fname, lname, eaddress, message)
            edit_record(msg_id, fname, lname, eaddress, message)
            return redirect('/admin')

        elif request.form.get('edit') == 'cancel':
            return redirect('/admin')
        
        elif request.form.get('admin') == 'Delete':
            delete_record(msg_id)
            return redirect('/admin')


    entry = get_single_record(msg_id)

    return render_template('edit.html', record = entry)
