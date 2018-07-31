from flask import Flask, render_template, request, session, url_for, redirect
from models import db, User,Place
from forms import SingupForm, LoginForm,AddressForm
import os

app = Flask(__name__)

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.\
    format(user='postgres', pw='password', url='localhost', db='postgres')

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# silence the deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
db.init_app(app)

app.secret_key = "development-key"


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SingupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            new_user = User(form.first_name.data, form.last_name.data,
                            form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()
            session['mail'] = new_user.email
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate() == False:
            print('validation')
            return render_template('login.html', form=form)
        else:
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home'))
                print('success login')
            else:
                print('faild to login')
                return redirect(url_for('login'))
    elif request.method == "GET":
        print('return to login page')
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/home',methods=['POST','GET'])
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    form = AddressForm()

    places = []
    my_coordinates = (37.4221, -122.0844)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('home.html', form=form)
        else:
        # get the address
            address = form.address.data 

        # query for places around it
        p = Place()
        my_coordinates = p.address_to_latlng(address)
        places = p.query(address)

        # return those results
        return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)

    elif request.method == 'GET':
        return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)


if __name__ == "__main__":
    app.run(debug=True)
