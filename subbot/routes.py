import json
from subbot import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from subbot.forms import RegisterForm, LoginForm
from wtforms.validators import ValidationError
from subbot.functions import connectToGraphDB, updateToGraphDB

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        teacherId = form.teacherId.data
        print("teacherId", teacherId)
        query = {'query': 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \
        PREFIX owl: <http://www.w3.org/2002/07/owl#> \
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\
        PREFIX subject: <http://www.semanticweb.org/subject_ontology#>\
        SELECT ?teacher\
        WHERE{\
            ?teacher subject:teacherId "%s". \
        }' % (teacherId)}
        print(query)
        # connecting to graphDB
        response = connectToGraphDB(query)
        print(response)
        response.encoding = 'utf-8'
        responseJson = json.loads(response.text)
        responseJsonResults = responseJson['results']['bindings']
        print(responseJsonResults)
        if len(responseJsonResults) > 0:
            flash(f'UserId already exists! Please try a different userId!', category='danger')
        else:
            teacherName = form.teacherName.data

            f = open("subbot/id/teacherId.txt", 'r')
            id = f.read()


            linkTeacherId= '<http://www.semanticweb.org/subject_ontology#Teacher'+id+'>'
            query = {'update': 'PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>\
            PREFIX owl:<http://www.w3.org/2002/07/owl#>\
            PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>\
            PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>\
            PREFIX subject:<http://www.semanticweb.org/subject_ontology#>\
            INSERT DATA\
            {\
            %s subject:name "%s" ;\
            subject:teacherId "%s" .\
            }' % (linkTeacherId,teacherName,teacherId)}

            print(query)
            # connecting to graphDB
            response = updateToGraphDB(query)
            print(response)
            if response.status_code==204:
                print('success')

                print(int(id))
                id = int(id)
                id += 1
                print(str(id))
                f = open("subbot/id/teacherId.txt", 'w')
                f.write(str(id))
                f.close()

                flash(f'Teacher account has successfully created!', category='success')
                return redirect(url_for('main_page'))
            else:
                flash(f'Teacher account creation failed. Try again!', category='danger')
                return redirect(url_for('register_page'))




    if form.errors !={}: #if there are not errors from the validations
        for err_msg in form.errors.values():
            print(type(err_msg))
            flash(f'{err_msg.pop()}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        teacherId = form.teacherId.data
        print("teacherId", teacherId)
        query = {'query': 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \
        PREFIX owl: <http://www.w3.org/2002/07/owl#> \
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\
        PREFIX subject: <http://www.semanticweb.org/subject_ontology#>\
        SELECT ?teacher\
        WHERE{\
            ?teacher subject:teacherId "%s". \
        }' % (teacherId)}
        print(query)
        # connecting to graphDB
        response = connectToGraphDB(query)
        print(response)
        response.encoding = 'utf-8'
        responseJson = json.loads(response.text)
        responseJsonResults = responseJson['results']['bindings']
        print(responseJsonResults)
        if len(responseJsonResults) > 0:
            flash(f'Successfully logged in!', category='success')
            print("tearcher id is "+teacherId)
            return render_template('main.html', userId= teacherId)
        else:
            flash(f"There is no teacher with ID '"+teacherId+"'!", category='danger')
            return redirect(url_for('login_page'))

    if form.errors !={}: #if there are not errors from the validations
        for err_msg in form.errors.values():
            print(type(err_msg))
            flash(f'{err_msg.pop()}', category='danger')

    return render_template('login.html', form=form)

@app.route('/main')
def main_page():
    return render_template('main.html')

@app.route('/logout')
def logout_page():
    return render_template('home.html')