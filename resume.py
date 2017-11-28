import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'this should be a secret key'


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)


class Professor(db.Model):
    __tablename__ = 'professors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    dept = db.Column(db.String(10))
    courses = db.relationship('Course', backref='professor')


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(256))
    title = db.Column(db.String(256))
    desc = db.Column(db.Text)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'))


@app.route('/')
def index():
    # return HTML
    # return "<h1>this is the index page!<h1>"
    return render_template('index.html')


@app.route('/courses')
def show_all_courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)


#@app.route('/courses')
#def show_all_courses():
#    courses = [
#        'MISY350',
#        'FINC312',
#        'ACCT315'
#    ]
#
#    return render_template('courses.html', courses=courses)


@app.route('/professors')
def show_all_professors():
    professors = Professor.query.all()
    return render_template('professors.html', professors=professors)


@app.route('/professor/add', methods=['GET','POST'])
def add_professors():
    if request.method == 'GET':
        return render_template('professors-add.html')
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        dept = request.form['dept']

        # insert the data into the database
        professor = Professor(name=name, dept=dept)
        db.session.add(professor)
        db.session.commit()
        return redirect(url_for('show_all_professors'))


@app.route('/professor/edit/<int:id>', methods=['GET', 'POST'])
def edit_professors(id):
    professor = Professor.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('professors-edit.html', professor=professor)
    if request.method == 'POST':
        # update data based on the form data
        professor.name = request.form['name']
        professor.dept = request.form['dept']
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_professors'))


@app.route('/course/add', methods=['GET', 'POST'])
def add_courses():
    if request.method == 'GET':
        professors = Professor.query.all()
        return render_template('courses-add.html', professors=professors)
    if request.method == 'POST':
        # get data from the form
        number = request.form['number']
        title = request.form['title']
        desc = request.form['desc']
        professor_name = request.form['professor']
        professor = Professor.query.filter_by(name=professor_name).first()
        course = Course(number=number, title=title, desc=desc, professor=professor)

        # insert the data into the database
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('show_all_courses'))


@app.route('/course/edit/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    course = Course.query.filter_by(id=id).first()
    professors = Professor.query.all()
    if request.method == 'GET':
        return render_template('courses-edit.html', course=course, professors=professors)
    if request.method == 'POST':
        # update data based on the form data
        course.number = request.form['number']
        course.title = request.form['title']
        course.desc = request.form['desc']
        professor_name = request.form['professor']
        professor = Professor.query.filter_by(name=professor_name).first()
        course.professor = professor
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_courses'))


@app.route('/about')
def about():
    return render_template('about.html')



# https://goo.gl/Pc39w8 explains the following line
if __name__ == '__main__':

    # activates the debugger and the reloader during development
    # app.run(debug=True)
    app.run()

    # make the server publicly available on port 80
    # note that Ports below 1024 can be opened only by root
    # you need to use sudo for the following conmmand
    # app.run(host='0.0.0.0', port=80)
