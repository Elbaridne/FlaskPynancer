from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField, SelectField,FloatField
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired("Please enter your username")])
    password = PasswordField("Password", [validators.DataRequired("Please enter your password")])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username")
    email = StringField("Email")
    password = PasswordField("Password")
    submit = SubmitField("Register")

class EntrieForm(FlaskForm):
    add_type = SelectField('Adding a new... ', choices=[('DayExpense', 'Daily Expenses'),('Hobby','Hobby'),('Transportation','Transportation cost'),('Property','Property cost'),('CreditCard','Credit Card due'),('Income','Income')])
    add_name = StringField('Name')
    add_cost = FloatField('Quantity ($)')
    submit = SubmitField('Add')
