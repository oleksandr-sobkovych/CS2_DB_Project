"""
Main module to interact with the database
"""
from sqlalchemy.orm import sessionmaker
from db_connect import engine
from classes import Author, MessageStyle, Discount, Customer, SocialMedia, Team, Access, Account, PlacedOrder
from datetime import timedelta, datetime


class DBInteraction:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.engine = engine
        self.all_styles_id = None
        self.views_exist = False
        self.indices_exist = False

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

    def get_networks(self):
        return self.session.query(SocialMedia).all()

    def create_views(self):
        return self.engine.execute("""
        CREATE OR REPLACE VIEW joined_orders AS
        SELECT po.order_id, t.*, po.message_id, po.created_date,
        c.first_name AS c_first_name, c.last_name AS c_last_name,
        a.author_id, a.first_name AS a_first_name, a.last_name AS a_last_name,
        acc.*
        FROM PlacedOrder po
        INNER JOIN Account acc USING (account_id)
        INNER JOIN Customer c USING (customer_id)
        INNER JOIN Team t USING (team_id)
        INNER JOIN AuthorTeam ta USING (team_id)
        INNER JOIN Author a USING (author_id)
        ORDER BY order_id;

        CREATE OR REPLACE VIEW joined_access AS
        SELECT access.access_id, access.access_granted_date, 
        access.access_terminated_date, acc.*,
        c.first_name AS c_first_name, c.last_name AS c_last_name,
        a.author_id, a.first_name AS a_first_name, a.last_name AS a_last_name
        FROM Access
        INNER JOIN Account acc USING (account_id)
        INNER JOIN Customer c USING (customer_id)
        INNER JOIN Author a USING (author_id)
        ORDER BY access_id;
        """)

    def get_customer_by_email_and_password(self, email, password):
        return self.session.query(Customer) \
            .filter(Customer.email == email,
                    Customer.password == password).one_or_none()

    def get_author(self, author_id):
        return self.session.query(Author).filter(Author.author_id ==
                                                 author_id).one_or_none()

    def get_customer(self, customer_id):
        return self.session.query(Customer).filter(Customer.customer_id ==
                                                 customer_id).one_or_none()

    def get_teams(self):
        return self.session.query(Team).all()

    def get_authors(self):
        return self.session.query(Author).all()

    def get_customers(self):
        return self.session.query(Customer).all()

    def get_styles(self):
        return self.session.query(MessageStyle).all()

    def create_order(self, account_id, team_id, msg_id):
        cur_order = PlacedOrder(account_id, team_id, msg_id, datetime.now())
        self.session.add(cur_order)
        self.session.commit()

        return cur_order

    def create_access(self, account_id, author_id, duration_hrs):
        cur_access = Access(account_id, author_id, datetime.now(),
                            datetime.now() + timedelta(hours=duration_hrs))
        self.session.add(cur_access)
        self.session.commit()

        return cur_access

    def get_account_by_customer_and_media(self, customer_id, media_id):
        return self.session.query(Account)\
            .filter(Account.customer_id == customer_id,
                    Account.media_id == media_id).one_or_none()

    def get_customer_media(self, customer_id):
        return self.engine.execute("""
                          SELECT DISTINCT A.media_id, SocialMedia.media_name
                          FROM SocialMedia
                          JOIN Account A on SocialMedia.media_id = A.media_id
                         WHERE A.customer_id = %s;
                      """ % customer_id).all()

    def add_customer_medias(self, customer_id, media_ids):
        customer = self.get_customer(customer_id)

        for media in media_ids:
            media_id = self.session.query(SocialMedia).filter(
                SocialMedia.media_id == media).one_or_none().media_id
            self.session.add(Account(customer_id, media_id,
                                     customer.password, customer.email,
                                     datetime.now()))
        self.session.commit()

    def search_1(self, author_id, mess_num, date_start, date_end):
        return self.engine.execute("""
            SELECT CONCAT(cus.first_name, ' ', cus.last_name) as name from Customer cus
            INNER JOIN Account acc ON cus.customer_id = acc.customer_id
            INNER JOIN PlacedOrder ord ON ord.account_id = acc.account_id
            INNER JOIN Team team ON team.team_id = ord.team_id
            INNER JOIN AuthorTeam ta ON team.team_id = ta.team_id
            INNER JOIN Author author ON author.author_id = ta.author_id
            WHERE author.author_id = %s
            AND ord.created_date >= '%s'
            AND ord.created_date <  '%s'
            GROUP BY cus.first_name, cus.last_name, author.author_id, ord.order_id
            HAVING COUNT(cus.first_name) >= %s
        """ % (author_id, date_start, date_end, mess_num)).all()

    def search_2(self, customer_id, date_start, date_end):
        return self.engine.execute("""
            SELECT CONCAT(author.first_name, ' ', author.last_name) as name FROM Author author
            INNER JOIN AuthorTeam ta ON ta.author_id = author.author_id
            INNER JOIN Team team ON team.team_id = ta.team_id
            INNER JOIN PlacedOrder ord ON ord.team_id = team.team_id
            INNER JOIN Account acc ON ord.account_id = ord.account_id
            INNER JOIN Customer cus ON cus.customer_id = acc.customer_id
            WHERE cus.customer_id = %s
            AND ord.created_date >= '%s'
            AND ord.created_date <  '%s'
            GROUP BY (author.author_id)
        """ % (customer_id, date_start, date_end)).all()

    def search_3(self, date_start, date_end, ids):
        return self.engine.execute("""
            SELECT a.author_id AS id, CONCAT(a.first_name, ' ', a.last_name) AS full_name FROM Author a
            INNER JOIN AuthorTeam ta ON ta.author_id = a.author_id
            INNER JOIN Team t ON t.team_id = ta.team_id
            INNER JOIN PlacedOrder po ON po.team_id = t.team_id
            WHERE po.created_date >= '%s'		
                AND po.created_date < '%s'		
            GROUP BY id
            HAVING COUNT(DISTINCT po.account_id) >= %s      
            ORDER BY full_name;

        """ % (date_start, date_end, ids)).all()

    def search_4(self, date_start, date_end, order_id):
        return self.engine.execute("""
            SELECT c.customer_id AS id, CONCAT(c.first_name, ' ', c.last_name) AS full_name FROM Customer c
            INNER JOIN Account ac ON ac.customer_id = c.customer_id
            INNER JOIN PlacedOrder po ON po.account_id = ac.account_id
            WHERE po.created_date >= '%s'		
                AND po.created_date <  '%s'		
            GROUP BY id
            HAVING COUNT(po.order_id) >= %s				
            ORDER BY full_name;
        """ % (date_start, date_end, order_id)).all()

    def search_5(self, customer_id, date_start, date_end, count):
        return self.engine.execute("""
            SELECT sm.media_id FROM SocialMedia sm
            INNER JOIN Account acc ON sm.media_id = acc.media_id
            INNER JOIN PlacedOrder ord ON acc.account_id = ord.account_id
            WHERE acc.customer_id = %s
                AND ord.created_date >= '%s' 
                AND ord.created_date < '%s'
            GROUP BY sm.media_id
            HAVING COUNT(*) > %s;
        """ % (customer_id, date_start, date_end, count)).all()

    def search_6(self, date_start, date_end, author_id):
        return self.engine.execute("""
            SELECT acc.account_id FROM Account acc
            INNER JOIN Access acs ON acc.account_id = acs.account_id
            WHERE acs.access_granted_date <= '%s'
            AND acs.access_terminated_date >= '%s'
            AND acs.author_id = %s;
        """ % (date_start, date_end, author_id)).all()

    def search_7(self, customer_id):
        return self.engine.execute("""
            SELECT * FROM Author a
            INNER JOIN Access ON access.author_id = a.author_id
            INNER JOIN Account acc ON acc.account_id = access.account_id
            WHERE customer_id = %s      
            AND access_terminated_date < CURRENT_TIMESTAMP;
        """ % customer_id).all()

    def search_8(self, customer_id, author_id, date_start, date_end):
        if not self.views_exist:
            self.create_views()
        return self.engine.execute("""
            SELECT  (
                    SELECT COUNT(*)
                    FROM joined_orders
                    WHERE customer_id = %s
                    AND author_id = %s
                    AND (created_date >= date '%s'     -- F
                        OR created_date <= date '%s')  -- T
                    ) +
                    (
                    SELECT COUNT(*)
                    FROM joined_access
                    WHERE customer_id = %s
                    AND author_id = %s
                    AND ((access_granted_date >= date '%s'             -- F
                         AND access_granted_date <= date '%s')         -- T
                    OR (access_terminated_date >= date  '%s'           -- F
                         AND access_terminated_date <= date '%s'))     -- T
                    ) AS event_count;

        """ % (customer_id, author_id, date_start, date_end,
               customer_id, author_id,
               date_start, date_end, date_start, date_end)).all()

    def search_9(self, customer_id):    # TODO: write this query
        return self.engine.execute("""
        
        """ % customer_id).all()

    def search_10(self, customer_id, date_start, date_end):    # TODO: check this query
        return self.engine.execute("""
            SELECT messagestyle.style_name, COUNT(*) AS orders_count FROM customer
            JOIN account ON (customer.customer_id=account.customer_id)
            JOIN placedorder ON (placedorder.account_id=account.customer_id)
            JOIN message ON (placedorder.message_id=message.message_id)
            JOIN messagestyle ON (message.style_id=messagestyle.style_id)
            JOIN discount ON (discount.style_id=messagestyle.style_id)
            WHERE customer.customer_id = %s  -- C
                AND placedorder.created_date BETWEEN '%s' AND '%s'         -- F, T
                AND placedorder.created_date BETWEEN discount.discount_date_start AND discount.discount_date_end
            GROUP BY messagestyle.style_name
        """ % (customer_id, date_start, date_end)).all()

    def search_11(self):
        if not self.views_exist:
            self.create_views()
        return self.engine.execute("""
            SELECT EXTRACT(MONTH FROM created_date) AS month,
            COUNT (*) AS num_orders
            FROM joined_orders
            GROUP BY month;
        """).all()

    def search_12(self, customer_id, date_start, date_end):
        return self.engine.execute("""
            SELECT socialmedia.media_name, COUNT (*) AS orders_count FROM socialmedia
            JOIN account ON (socialmedia.media_id = account.media_id)
            JOIN placedorder ON (placedorder.account_id = account.account_id)
            JOIN customer ON (customer.customer_id = account.customer_id)
            WHERE customer.customer_id = %s --C
                AND placedorder.created_date BETWEEN '%s' AND '%s' 
            GROUP BY socialmedia.media_name
        """ % (customer_id, date_start, date_end)).all()

    def get_author_by_name(self, first_name, last_name):
        return self.session.query(Author) \
            .filter(Author.first_name == first_name and
                    Author.last_name == last_name).first()

    def get_author_by_email_and_password(self, email, password):
        return self.session.query(Author) \
            .filter(Author.email == email and
                    Author.password == password).first()

    def add_skill(self, author_id, style_ids):
        author = self.get_author(author_id)

        for style_id in style_ids:
            # select style from the database
            selected_style = self.session.query(MessageStyle) \
                .filter(MessageStyle.style_id == style_id).all()

            if not selected_style:
                # insert this style if it is absent
                selected_style = MessageStyle(style_id)
                self.session.add(selected_style)
            else:
                # select first occurrence
                selected_style = selected_style[0]

            # back populate data
            author.styles.append(selected_style)

        self.session.commit()

    def create_one_day_discount(self, author_id, amount, date_start):
        if date_start < datetime.now():
            return False

        discount = Discount(author_id, 1, amount, date_start,
                            date_start + timedelta(hours=24))

        self.session.add(discount)
        self.session.commit()
        return True

    def get_style_by_name(self, style_name):
        return self.session.query(MessageStyle) \
            .filter(MessageStyle.style_name == style_name).one_or_none()

    def create_multiple_days_discount(self, author_id, style_id, amount,
                                      date_start, date_end):
        print(date_start < datetime.now(), date_end < date_start,  style_id, [st.style_id for st in self.get_author(author_id).styles])
        if (date_start < datetime.now() or date_end < date_start
                or int(style_id) not in [st.style_id for st in self.get_author(author_id).styles]):
            return False
        discount = Discount(author_id, style_id, amount, date_start, date_end)

        self.session.add(discount)
        self.session.commit()
        return True
