from flask_login import UserMixin
from FlaskPynancer import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '{0}'.format(self.username)


class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    d_name = db.Column(db.String(80), nullable=False)
    d_cost = db.Column(db.Float, nullable=False)
    d_date = db.Column(db.DATETIME, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_associated = db.relationship('User', backref=db.backref('data_hobby', lazy=True))
    def __repr__(self):
        return 'Hobby  {0}'.format(self.d_name)

    def __iter__(self):
        for attr, value in self.__dict__.items():
            if attr.startswith('d_'):
                yield attr,value

class DayExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    d_name = db.Column(db.String(80), nullable=False)
    d_cost = db.Column(db.Float, nullable=False)
    d_date = db.Column(db.DATETIME, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_associated = db.relationship('User', backref=db.backref('data_dayexpense', lazy=True))

    def __repr__(self):
        return 'DayExpense {0}'.format(self.d_name)

class Transportation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    d_name = db.Column(db.String(80), nullable=False)
    d_cost = db.Column(db.Float, nullable=False)
    d_date = db.Column(db.DATETIME, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_associated = db.relationship('User', backref=db.backref('data_transportation', lazy=True))

    def __repr__(self):
        return 'Transportation {0}'.format(self.d_name)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    d_name = db.Column(db.String(80), nullable=False)
    d_cost = db.Column(db.Float, nullable=False)
    d_date = db.Column(db.DATETIME, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_associated = db.relationship('User', backref=db.backref('data_property', lazy=True))

    def __repr__(self):
        return 'Property {0}'.format(self.d_name)

class CreditCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    d_name = db.Column(db.String(80), nullable=False)
    d_cost = db.Column(db.Float, nullable=False)
    d_date = db.Column(db.DATETIME, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_associated = db.relationship('User', backref=db.backref('creditcard', lazy=True))

    def __repr__(self):
        return 'Credit Card {0} : ID associated {1}'.format(self.d_name, self.user_id)


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    d_name = db.Column(db.String(80), nullable=False)
    d_cost = db.Column(db.Float, nullable=False)
    d_date = db.Column(db.DATETIME, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_associated = db.relationship('User', backref = db.backref('data_income', lazy=True))

    def __repr__(self):
        return 'Income {0}'.format(self.d_name)

