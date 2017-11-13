from flask import Flask, render_template, request, flash
app = Flask(__name__)
app.secret_key = 'this should be a secret key'


@app.route('/')
def index():
    # return HTML
    # return "<h1>this is the index page!<h1>"
    return render_template('index.html')


@app.route('/courses')
def show_all_courses():
    courses = [
        'MISY350',
        'FINC312',
        'ACCT315'
    ]

    return render_template('courses.html', courses=courses)


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
