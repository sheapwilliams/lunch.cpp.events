from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, OrderForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Order

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
     form = OrderForm()
     if form.validate_on_submit():
        order = Order(user_id=current_user.get_id() )
        order.monday = form.select_monday.data
        order.tuesday = form.select_tuesday.data
        order.wednesday = form.select_wednesday.data
        order.thursday = form.select_thursday.data
        order.friday = form.select_friday.data
        db.session.add(order)
        db.session.commit()
        flash('Payment processing...' + order.monday + ', ' + order.wednesday + ' - ' + str(order.user_id))
        return redirect(url_for('payment'))
     return render_template('order.html', title="Order", form=form)

@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
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