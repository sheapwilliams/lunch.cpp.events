from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, OrderForm, RegistrationForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Order
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='C++ Now', price=app.config['ORDER_PRICE'], items=app.config['ORDER_OPTIONS'])


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/order', methods=['GET','POST'])
@login_required
def order():
     u = db.session.get(User, current_user.get_id())
     form = OrderForm(orders=u.orders)
    
     if form.validate_on_submit():
        if u.orders == None:
            order = Order(user_id=current_user.get_id())
            order.monday = form.select_monday.data
            order.tuesday = form.select_tuesday.data
            order.wednesday = form.select_wednesday.data
            order.thursday = form.select_thursday.data
            order.friday = form.select_friday.data
            db.session.add(order)
        else:
            u.orders.monday = form.select_monday.data
            u.orders.tuesday = form.select_tuesday.data
            u.orders.wednesday = form.select_wednesday.data
            u.orders.thursday = form.select_thursday.data
            u.orders.friday = form.select_friday.data  
        db.session.commit()
        flash('Payment processing...' + u.orders.monday + ', ' + u.orders.wednesday + ' - user_id: ' + str(u.orders.user_id))
        return redirect(url_for('payment'))
     return render_template('order.html', title="Order", form=form)

@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    user = db.session.get(User, current_user.get_id())
    return render_template('payment.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)