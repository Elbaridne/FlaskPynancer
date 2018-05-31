from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_login import current_user, login_user, logout_user
from flask_bootstrap import Bootstrap
import flask_login
import forms

from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/MarioMBlu/PycharmProjects/FlaskPynancer/sqlite.db'
app.secret_key = "super secret KEY LMAO"
db = SQLAlchemy(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
Bootstrap(app)


from models import *
import datetime



date = datetime.date.today()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template('index.html')

@app.route('/user', methods=['GET','POST'])
@flask_login.login_required
def user():
    form = forms.EntrieForm()
    if form.validate_on_submit():
        cost_type = globals()[form.add_type.data]
        new_row = cost_type(d_name=form.add_name.data, d_cost=form.add_cost.data, d_date=date.today(),
                            user_id=current_user.id)
        db.session.add(new_row)
        db.session.commit()
        return redirect(url_for('user'))

    user_data = query_month(datetime.date.today())
    int_total_income, int_total_cost, cost_w_keys, income_w_key = month_calc(user_data)

    return render_template('user.html', user_data=user_data, form=form, income=int_total_income, costs=int_total_cost,income_key=income_w_key,group_cost=cost_w_keys)

def month_calc(month_data):
    int_total_income = sum(elem.d_cost for elem in month_data['Income'])//1
    income_w_key = month_data['Income']
    month_data.pop('Income')
    individual_cost = list(sum([cost.d_cost for cost in elem])//1 for key, elem in month_data.items())#TODO NOT GOOD
    int_total_cost = sum(individual_cost)
    cost_w_keys = dict(zip(month_data.keys(),individual_cost)) #TODO Total keys dict { key : cost } sin Income

    # Returns : {'income':value}, int_total_cost, {'cost':value}
    return int_total_income, int_total_cost, cost_w_keys, income_w_key

def query_to_dict():
    user_data = dict()
    user_data['Income'] = db.session.query(Income).filter(Income.user_id == current_user.id).all()
    user_data['Hobbies'] = db.session.query(Hobby).filter(Hobby.user_id == current_user.id).all()
    user_data['Daily expenses'] = db.session.query(DayExpense).filter(DayExpense.user_id == current_user.id).all()
    user_data['Transportation'] = db.session.query(Transportation).filter(Transportation.user_id == current_user.id).all()
    user_data['Properties'] = db.session.query(Property).filter(Property.user_id == current_user.id).all()
    user_data['Credit cards'] = db.session.query(CreditCard).filter(CreditCard.user_id == current_user.id).all()
    return user_data

def query_month(date):

    month = date.month
    user_data = query_to_dict()
    for key, value in user_data.items():
        user_data[key] = [value for value in value if value.d_date.month == month]
    return user_data



@app.route('/user/add', methods=['GET', 'POST'])
@flask_login.login_required
def add_hobby():
    form = forms.EntrieForm()
    if form.validate_on_submit():
        cost_type = globals()[form.add_type.data]
        new_row = cost_type(d_name=form.add_name.data, d_cost=form.add_cost.data, d_date=date.today(), user_id=current_user.id)
        db.session.add(new_row)
        db.session.commit()
        return redirect(url_for('user'))
    return render_template('add_new.html', form=form)

@app.route('/reset') #TODO Not cool at all
def del_all():
    db.drop_all()
    db.create_all()
    return 'Dropping and creating tables'


@app.route('/check')
@flask_login.login_required
def check_users():
    if current_user.is_authenticated:

        return current_user.username
    else:
        return 'Not authenticated'



## USER

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


def authenticate(username, password):
    _user = User.query.filter_by(username=username).first()
    if _user is None:
        return None
    if _user.password == password:
        return _user
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user_authenticated = authenticate(form.username.data, form.password.data)
        if user_authenticated is None:
            return 'Bad credentials'

        login_user(user_authenticated)

        return redirect(url_for('user'))

    return render_template('login.html', form=form)




@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        user_ = User(username=form.username.data, email=form.email.data, password=form.password.data)
        try:
            db.session.add(user_)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return 'Username already taken'

        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/logout')
@flask_login.login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()
