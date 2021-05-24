from sqlalchemy import Table, Column, Integer, String, ForeignKey, DATE
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Declare all many-to-many secondary tables
author_team_association = Table('authorteam', Base.metadata,
    Column('team_id', Integer, ForeignKey('team.team_id')),
    Column('author_id', Integer, ForeignKey('author.author_id'))
)

author_style_association = Table('skill', Base.metadata,
    Column('author_id', Integer, ForeignKey('author.author_id')),
    Column('style_id', Integer, ForeignKey('messagestyle.style_id'))
)

# Declare main classes
class Author(Base):
    __tablename__ = 'author'

    author_id = Column(Integer, primary_key=True)
    first_name = Column('first_name', String(100))
    last_name = Column('last_name', String(100))
    password = Column('password', String(20))
    email = Column('email', String(320))

    teams = relationship('Team', secondary=author_team_association, back_populates='authors')
    styles = relationship('MessageStyle', secondary=author_style_association, back_populates='authors')

    def __init__(self, first_name, last_name, password, email):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email


class Team(Base):
    __tablename__ = 'team'

    team_id = Column(Integer, primary_key=True)
    team_name = Column('team_name', String(100))

    authors = relationship("Author", secondary=author_team_association, back_populates='teams')

    def __init__(self, team_name):
        self.team_name = team_name


class MessageStyle(Base):
    __tablename__ = 'messagestyle'

    style_id = Column(Integer, primary_key=True)
    style_name = Column('style_name', String(100))

    authors = relationship("Author", secondary=author_style_association, back_populates='styles')

    def __init__(self, style_name):
        self.style_name = style_name


class Message(Base):
    __tablename__ = 'message'

    message_id = Column(Integer, primary_key=True)
    text = Column('text', String(5000))
    style_id = Column(Integer, ForeignKey('messagestyle.style_id'))
    style = relationship("MessageStyle")


class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True)
    first_name = Column('first_name', String(100))
    last_name = Column('last_name', String(100))
    email = Column('email', String(320))


class SocialMedia(Base):
    __tablename__ = 'socialmedia'

    media_id = Column(Integer, primary_key=True)
    media_name = Column('first_name', String(100))


class Account(Base):
    __tablename__ = 'account'

    account_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    media_id = Column(Integer, ForeignKey('socialmedia.media_id'))
    style_id = Column(Integer, ForeignKey('messagestyle.style_id'))
    password = Column('password', String(20))
    username = Column('username', String(20))
    registration_date = Column('registration_date', DATE)

    customer = relationship("Customer")
    media = relationship("SocialMedia")
    style = relationship("MessageStyle")


class PlacedOrder(Base):
    __tablename__ = 'placedorder'

    order_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id'))
    team_id = Column(Integer, ForeignKey('team.team_id'))
    message_id = Column(Integer, ForeignKey('message.message_id'))
    created_date = Column('created_date', DATE)

    account = relationship("Account")
    team = relationship("Team")
    message = relationship("Message")


class Access(Base):
    __tablename__ = 'access'

    access_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id'))
    author_id = Column(Integer, ForeignKey('author.author_id'))
    access_granted_date = Column('access_granted_date', DATE)
    access_terminated_date = Column('access_terminated_date', DATE)

    account = relationship("Account")
    author = relationship("Author")


class Discount(Base):
    __tablename__ = 'discount'

    discount_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('author.author_id'))
    style_id = Column(Integer, ForeignKey('messagestyle.style_id'))
    discount_percentage = Column('discount_percentage', Integer)
    discount_date_start = Column('discount_date_start', DATE)
    discount_date_end = Column('discount_date_end', DATE)

    author = relationship("Author")
    style = relationship("MessageStyle")

    def __init__(self, author_id, style_id, discount_percentage,
                 discount_date_start, discount_date_end):
        self.author_id = author_id
        self.style_id = style_id
        self.discount_percentage = discount_percentage
        self.discount_date_start = discount_date_start
        self.discount_date_end = discount_date_end


class Review(Base):
    __tablename__ = 'review'

    review_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('placedorder.order_id'))
    message = Column('message', String(500))
    rating = Column('rating', Integer)
    created_date = Column('created_date', DATE)

    order = relationship("PlacedOrder")

