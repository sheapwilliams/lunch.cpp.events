from flask import render_template, flash, redirect, url_for, jsonify, request, session
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
import stripe
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, OrderForm, PaymentForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
from app.models import User, Order, Session
from app.email import send_password_reset_email, send_order_email


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
            app.logger.info("Failed login for: %s", user)
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        sess = db.session.get(Session, current_user.get_id())
        if sess is not None:
            db.session.delete(sess)
            db.session.commit()
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    sess = db.session.get(Session, current_user.get_id())
    if sess is not None:
        db.session.delete(sess)
        db.session.commit()
    logout_user()
    return redirect(url_for('index'))


@app.route('/order', methods=['GET','POST'])
@login_required
def order():
     form = OrderForm()
     u = db.session.get(User, current_user.get_id())
     tp = 0

     if u.orders is not None:
        tp = u.orders.total_paid
    
     if form.validate_on_submit():
        sess = db.session.get(Session, current_user.get_id())
        if sess is None:
            sess = Session(user_id=current_user.get_id(),
                monday = form.select_monday.data,
                tuesday = form.select_tuesday.data,
                wednesday = form.select_wednesday.data,
                thursday = form.select_thursday.data,
                friday = form.select_friday.data,
                total_paid = tp
                )
            db.session.add(sess)
        else:
            sess.monday = form.select_monday.data
            sess.tuesday = form.select_tuesday.data
            sess.wednesday = form.select_wednesday.data
            sess.thursday = form.select_thursday.data
            sess.friday = form.select_friday.data
            
        db.session.commit()
        #flash('Payment processing...' + u.orders.monday + ', ' + u.orders.wednesday + ' - user_id: ' + str(u.orders.user_id))
        return redirect(url_for('payment'))
     
     if u.orders != None:
         form.select_monday.data = u.orders.monday
         form.select_tuesday.data = u.orders.tuesday
         form.select_wednesday.data = u.orders.wednesday
         form.select_thursday.data = u.orders.thursday
         form.select_friday.data = u.orders.friday

     return render_template('order.html', title="Order", form=form)


@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    form = PaymentForm()
    user = db.session.get(User, current_user.get_id())
    so = db.session.get(Session, current_user.get_id())
    if not user or not so:
        return redirect(url_for('index'))
    
    if form.validate_on_submit():
        if so.chargeDiff() == 0:
            return redirect(url_for('change_order'))
        
        flash('processing!')
        return redirect(url_for('create_checkout_session'))

    return render_template('payment.html', title='Payment', form=form, user=user, so=so)


@app.route('/change-order', methods=['GET','POST'])
@login_required
def change_order():
    user = db.session.get(User, current_user.get_id())
    so = db.session.get(Session, current_user.get_id())


    if user.orders == None:
        order = Order(user_id=current_user.get_id())
        order.monday = so.monday
        order.tuesday = so.tuesday
        order.wednesday = so.wednesday
        order.thursday = so.thursday
        order.friday = so.friday
        order.status = ""
        order.total_paid = 0
        db.session.add(order)
        db.session.commit()
    else:
        if so.monday != "Past":
            user.orders.monday = so.monday
        if so.tuesday != "Past":    
            user.orders.tuesday = so.tuesday
        if so.wednesday != "Past":    
            user.orders.wednesday =  so.wednesday
        if so.thursday != "Past":    
            user.orders.thursday = so.thursday
        if so.friday != "Past":
            user.orders.friday = so.friday

    send_order_email(user)

    db.session.delete(so)
    db.session.commit()

    return render_template('change_order.html', title='Order Updated', user=user)


@app.route('/create-checkout-session', methods=['GET','POST'])
@login_required
def create_checkout_session():
    so = db.session.get(Session, current_user.get_id())
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1OzSA8LBbTglYvMbQRU47oPX',
                    'quantity': so.totalDaysDiff(),
                },
            ],
            mode='payment',
            success_url=app.config['SERVER_DOMAIN'] + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=app.config['SERVER_DOMAIN'] + '/cancel',
            automatic_tax={'enabled': False},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@app.route('/success', methods=['GET'])
@login_required
def success():
    session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    user = db.session.get(User, current_user.get_id())
    so = db.session.get(Session, current_user.get_id())

    if user:
        paid = session.amount_total / 100

        if user.orders == None:
            order = Order(user_id=current_user.get_id())
            order.monday = so.monday
            order.tuesday = so.tuesday
            order.wednesday = so.wednesday
            order.thursday = so.thursday
            order.friday = so.friday
            order.status = ""
            order.total_paid = 0
            db.session.add(order)
            db.session.commit()
        else:
            if so.monday != "Past":
                user.orders.monday = so.monday
            if so.tuesday != "Past":    
                user.orders.tuesday = so.tuesday
            if so.wednesday != "Past":    
                user.orders.wednesday =  so.wednesday
            if so.thursday != "Past":    
                user.orders.thursday = so.thursday
            if so.friday != "Past":
                user.orders.friday = so.friday

        user.orders.total_paid += paid
        user.orders.status = "Paid!"
        send_order_email(user)

    db.session.delete(so)
    db.session.commit()

    return render_template('success.html', title='Successfully Purchased', user=user)


@app.route('/cancel')
def cancel():
    so = db.session.get(Session, current_user.get_id())
    db.session.delete(so)
    db.session.commit()
    return render_template('cancel.html')


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


@app.route('/status')
@login_required
def status():
    user = db.session.get(User, current_user.get_id())
    if user.orders == None:
        return render_template('status_none.html', title='Order Status')
    
    return render_template('status.html', title='Order Status', user=user)


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

