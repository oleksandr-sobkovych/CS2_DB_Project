#from db_interaction import DBInteraction
from sqlalchemy.orm import sessionmaker
from db_connect import engine
from classes import Author, MessageStyle, Discount, Customer
from datetime import datetime, timedelta

conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

#interaction = DBInteraction()


def create_author_account(name, surname, password):
    cur_author = Author(name, surname, password)
    session.add(cur_author)
    session.commit()

    return cur_author


def create_customer(name, surname, password):
    cur_customer = Customer(name, surname, password)
    session.add(cur_customer)
    session.commit()

    return cur_customer


def get_author(id):
    return session.query(Author).get(id)


def get_author_by_name(first_name, last_name):
    return session.query(Author) \
        .filter(Author.first_name == first_name and
                Author.last_name == last_name).first()


def add_skill(author_id, style_names):
    author = get_author(author_id)

    for style in style_names:
        # select style from the database
        selected_style = session.query(MessageStyle) \
            .filter(MessageStyle.style_name == style).all()

        if not selected_style:
            # insert this style if it is absent
            selected_style = MessageStyle(style)
            session.add(selected_style)
        else:
            # select first occurance
            selected_style = selected_style[0]

        # back populate data
        author.styles.append(selected_style)

    session.commit()


def create_one_day_discount(author_id, style_id, amount, date_start):
    author = get_author(author_id)

    discount = Discount(author_id, style_id, amount, date_start, date_start +
                        timedelta(hours=1))

    session.add(discount)
    session.commit()


def create_multiple_days_discount(author_id, style_id, amount, date_start,
                                  date_end):
    author = get_author(author_id)

    discount = Discount(author_id, style_id, amount, date_start, date_end)

    session.add(discount)
    session.commit()


def execute():
    result = engine.execute("""
        SELECT a.author_id AS id, CONCAT(a.first_name, ' ', a.last_name) AS full_name FROM Author a
        INNER JOIN AuthorTeam ta ON ta.author_id = a.author_id
        INNER JOIN Team t ON t.team_id = ta.team_id
        INNER JOIN PlacedOrder po ON po.team_id = t.team_id
        WHERE po.created_date >= '2021-01-01'		-- T
        AND po.created_date <  '2021-06-01'		-- F
        GROUP BY id
        HAVING COUNT(DISTINCT po.account_id) >= 2	-- N
        ORDER BY full_name;
    """).all()
    print(result)


if __name__ == '__main__':
    # create_author_account('1name', '1lname', '1pass')
    # print(get_author(12).first_name)
    # add_skill(12, ['assertive', 'hey'])
    execute()
