from flask import Flask, render_template, request, redirect, url_for
from HW3.models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../instance/mydatabase.db'
db.init_app(app)


@app.route('/')
def index():
    return 'qq!'


@app.route('/register/', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user = User(firstname=request.form.get('fname'), secondname=request.form.get('lname'),
                    email=request.form.get('email'), password=request.form.get('pass'))

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('show_users'))
    else:
        return render_template('register.html')


@app.route('/users/')
def show_users():
    users = User.query.all()
    context = {'users': users}
    return render_template('users.html', **context)


@app.cli.command('init-db')
def init_db():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

