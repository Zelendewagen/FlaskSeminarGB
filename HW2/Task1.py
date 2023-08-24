from flask import Flask, render_template, session, redirect, url_for, make_response, request

app = Flask(__name__)
app.secret_key = '3342beb0adf3bb01ea33b8f535fdde2167062754be477ac10b934014b0e6e5ea'


@app.route('/')
def index():
    if 'name' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = make_response(redirect(url_for('index')))
        response.set_cookie(request.form.get('name'), request.form.get('mail'))
        session['name'] = request.form.get('name') or 'noone'
        return response
    else:
        return render_template("login.html")


@app.route('/logout/')
def logout():
    session.pop('name', None)
    return redirect(url_for('login'))


app.run(debug=True)
