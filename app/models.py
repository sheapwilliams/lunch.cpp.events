
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone
from time import time
import jwt
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from hashlib import md5
from app import app, db, login 

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(256), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    orders: so.Mapped['Order'] = so.relationship( back_populates='user')

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)
    

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

    
class Order(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    monday: so.Mapped[str] = so.mapped_column(sa.String(256), index=False)
    tuesday: so.Mapped[str] = so.mapped_column(sa.String(256), index=False)
    wednesday: so.Mapped[str] = so.mapped_column(sa.String(256), index=False)
    thursday: so.Mapped[str] = so.mapped_column(sa.String(256), index=False)
    friday: so.Mapped[str] = so.mapped_column(sa.String(256), index=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True,  unique=True)
    user: so.Mapped[User] = so.relationship(back_populates='orders')

    def __repr__(self) -> str:
        return '<Order id:{} uid:{} m:{} t:{} w:{} t:{} f:{} timestamp:{}>'.format(
            self.id,self.user_id,self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.timestamp
            )
    
    def total(self) -> float:
        total = 0;
        if self.monday != "None (N)":
            total += app.config['ORDER_PRICE']
        if self.tuesday != "None (N)":
            total += app.config['ORDER_PRICE']
        if self.wednesday != "None (N)":
            total += app.config['ORDER_PRICE']
        if self.thursday != "None (N)":
            total += app.config['ORDER_PRICE']
        if self.friday != "None (N)":
            total += app.config['ORDER_PRICE']
        return total
    
def load_order(user_id):
    oq = sa.select(Order).where(Order.user_id==user_id)
    order = db.session.scalars(oq).first()
    if order == None:
        return Order(user_id)

    return Order(order)

