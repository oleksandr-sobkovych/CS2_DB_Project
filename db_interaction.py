"""
Main module to interact with the database
"""
from sqlalchemy.orm import sessionmaker
from db_connect import engine
from classes import Author, MessageStyle, Discount, Customer
from datetime import timedelta


class DBInteraction:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_author_account(self, name, surname, password, email):
        cur_author = Author(name, surname, password, email)
        self.session.add(cur_author)
        self.session.commit()

        return cur_author

    def create_customer(self, name, surname, password, email):
        cur_customer = Customer(name, surname, password, email)
        self.session.add(cur_customer)
        self.session.commit()

        return cur_customer

    def get_author(self, author_id):
        return self.session.query(Author).filter(Author.author_id ==
                                                 author_id).first()

    def get_author_by_name(self, first_name, last_name):
        return self.session.query(Author) \
            .filter(Author.first_name == first_name and
                    Author.last_name == last_name).first()

    def get_author_by_email_and_password(self, email, password):
        return self.session.query(Author) \
            .filter(Author.email == email and
                    Author.password == password).first()

    def add_skill(self, author_id, style_names):
        author = self.get_author(author_id)

        for style in style_names:
            # select style from the database
            selected_style = self.session.query(MessageStyle) \
                .filter(MessageStyle.style_name == style).all()

            if not selected_style:
                # insert this style if it is absent
                selected_style = MessageStyle(style)
                self.session.add(selected_style)
            else:
                # select first occurance
                selected_style = selected_style[0]

            # back populate data
            author.styles.append(selected_style)

        self.session.commit()

    def create_one_day_discount(self, author_id, style_name, amount, date_start):
        author = self.get_author(author_id)

        discount = Discount(author_id, style_name, amount, date_start,
                            date_start +
                            timedelta(hours=1))

        self.session.add(discount)
        self.session.commit()

    def get_style_by_name(self, style_name):
        return self.session.query(MessageStyle) \
            .filter(MessageStyle.style_name == style_name).first()

    def create_multiple_days_discount(self, author_id, style_name, amount, date_start,
                                      date_end):
        author = self.get_author(author_id)
        style_id = self.get_style_by_name(style_name)

        discount = Discount(author_id, style_name, amount, date_start, date_end)

        self.session.add(discount)
        self.session.commit()

    def execute_3rd_query(self):  # TODO: bad name need to fix
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




