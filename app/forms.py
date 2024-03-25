from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, PasswordField, BooleanField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy as sa
from app import app, db
from app.models import User, Order

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')


class OrderForm(FlaskForm):
    orders = Order()
    order_options = app.config['ORDER_OPTIONS']
    order_options_count = len(order_options)

    def selected_order_item(option, name):
        sel = 1
        for it in app.config['ORDER_OPTIONS'][option]['options']:
            if name ==  "{} ({})".format(it['name'], it['type']):
                return sel
            sel = sel + 1
        return 1 #

    def format_order_items(option):
        item_list = []
        # app.config['ORDER_OPTIONS'][1]['options'][0]['name']
        for it in app.config['ORDER_OPTIONS'][option]['options']:
           name = "{} ({})".format(it['name'], it['type'])
           desc = "{} ({}) - {}".format(it['name'], it['type'],  it['desc'])
           item = (name, desc)
           item_list.append(item)
        return item_list
    
    def format_order_date(option):
        return app.config['ORDER_OPTIONS'][option]['date'];


    select_monday = SelectField(format_order_date(0),choices=format_order_items(0), 
                                default=selected_order_item(0, orders.monday))
    select_tuesday = SelectField(format_order_date(1),choices=format_order_items(1), default=1)
    select_wednesday = SelectField(format_order_date(2),choices=format_order_items(2), default=1)
    select_thursday = SelectField(format_order_date(3),choices=format_order_items(3), default=1)
    select_friday = SelectField(format_order_date(4),choices=format_order_items(4), default=1)

    submit = SubmitField('Order Now')

class PaymentForm(FlaskForm):
    card = StringField('Card Details')
    submit = SubmitField('Process')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')