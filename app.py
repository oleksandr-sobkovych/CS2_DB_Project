from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime

from db_interaction import DBInteraction

APP = Flask(__name__)


class DataStore():
    db = DBInteraction()
    author_id = None
    style_name = None
    customer_id = None

data  = DataStore()


@APP.route("/")
def index():
    """Start page (choose author or customer)"""
    return render_template("index.html")


@APP.route("/login_or_create_author")
def login_or_create_author():
    """Choose login or create an new account as author"""
    return render_template("login_or_create_author.html")


@APP.route("/author_login", methods=["GET"])
def author_login():
    """Login page for authors"""
    return render_template("author_login.html")


@APP.route("/authors", methods=["GET"])
def get_authors():
    names = []
    authors = DataStore.db.get_authors()
    for author in authors:
        names.append({
            'name': "%s %s" % (author.first_name, author.last_name),
            'author_id': author.author_id,
            'email': author.email,
            'teams': [team.team_id for team in author.teams],
            'styles': [style.style_id for style in author.styles]
        })
    return jsonify({'status': 'ok', 'authors': names})


@APP.route("/search_1", methods=["GET"])
def search_1():
    author_id = request.args.get('author_id')
    mess_num = request.args.get('mess_num')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')

    date_start = datetime.strptime(date_start, '%Y-%m-%d')
    date_start = datetime.strftime(date_start, '%Y-%m-%d')
    date_end = datetime.strptime(date_end, '%Y-%m-%d')
    date_end = datetime.strftime(date_end, '%Y-%m-%d')

    users = DataStore.db.search_1(author_id, mess_num, date_start, date_end)
    return jsonify({'status': 'ok', 'users': users})


@APP.route("/author_login", methods=["POST"])
def login_author():
    """Login page for authors"""
    email = request.form.get("email")
    password = request.form.get("password")

    print(email)
    print(password)

    try:
        data.author_id = DataStore.db.get_author_by_email_and_password(email,

                                                                 password).author_id
    except AttributeError:
        return redirect("/author_login")
    print(data.author_id)

    return redirect("/author_account")


@APP.route("/author_signup", methods=["GET"])
def author_signup():
    """Page for author signing up"""
    return render_template("author_signup.html")


@APP.route("/author_signup", methods=["POST"])
def create_author():
    """Creating author account"""
    name = request.form.get("name")
    surname = request.form.get("surname")
    email = request.form.get("email")
    password = request.form.get("password")

    print(name)
    print(surname)
    print(email)
    print(password)

    data.author_id = DataStore.db.create_author_account(name, surname,
                                                        password, email)
    return redirect("/author_account")


@APP.route("/author_account", methods=["GET"])
def author_account():
    """Page for choosing style and then seeing possible tasks

    TO DO:
    !!!Seeing possible tasks
    !!!Choose many styles"""
    return render_template("author_account.html")


@APP.route("/author_account", methods=["POST"])
def author_account_post():
    style = request.form.get("style")
    print(style)
    data.style_name = [style]
    DataStore.db.add_skill(data.author_id, [style])
    return redirect("/manage_task")

# @APP.route("/task", methods=["GET", "POST"])
# def task():
#     """Page for author tasking doing"""
#     return render_template("task.html")

# @APP.route("/finishing_task", methods=["GET", "POST"])
# def finishing_task():
#     """Page for author tasking doing finish with buttom
#     @Do yoou want to give some discount@"""
#     return render_template("finishing_task.html")

@APP.route("/manage_task")
def manage_task():
    """Manage page for authors (creating discount or team)

    TO DO
    !!!Do it as a menu buttom"""
    return render_template("manage_task.html")

@APP.route("/discount")
def discount():
    """Page for creating discount"""
    return render_template("discount.html")

@APP.route("/multiple_days_discount", methods=["GET"])
def multiple_days_discount():
    """Page for creating discount"""
    return render_template("multiple_days_discount.html")

@APP.route("/multiple_days_discount", methods=["POST"])
def multiple_days_discount_post():
    From = datetime.strptime(request.form.get("From"), "%d.%m")
    print(From)
    To = datetime.strptime(request.form.get("To"))
    print(To)
    DataStore.db.create_multiple_days_discount(data.author_id, data.style_name, 5, From, To)
    return redirect("/finish_author")

@APP.route("/create_team", methods=["GET", "POST"])
def create_team():
    """Page for creating team

    TO DO
    !!!Create_team.html доробити"""
    return render_template("create_team.html")

@APP.route("/one_day_discount", methods=["GET"])
def one_day_discount():
    """Page for creating 1 day discount"""
    return render_template("one_day_discount.html")

@APP.route("/one_day_discount", methods=["POST"])
def one_day_discount_post():
    from_ = datetime.strptime(request.form.get("from"), "%d.%m")
    to_ = request.form.get("discount_number")
    print (from_)
    print (to_)
    DataStore.db.create_one_day_discount(data.author_id, data.style_name,
                                               to_, from_)
    return redirect("/finish_author")

@APP.route("/login_or_create_customer")
def login_or_create_customer():
    """Choose login or create an new account as customer

    TO DO
    !ПОПРАВИТИ CSS"""
    return render_template("login_or_create_customer.html")

@APP.route("/customer_login", methods=["GET"])
def customer_login():
    """Cusomer login page"""
    return render_template("customer_login.html")


@APP.route("/customer_login", methods=["POST"])
def login_customer():
    """Login page for customers"""
    email = request.form.get("email")
    password = request.form.get("password")

    print(email)
    print(password)

    return redirect("/customer_account")

@APP.route("/customer_signup", methods=["GET"])
def customer_signup():
    """Cusomer signup page"""
    return render_template("customer_singup.html")

@APP.route("/customer_signup", methods=["POST"])
def customer_signup_post():
    """Login page for customers"""
    name = request.form.get("name")
    surname = request.form.get("surname")
    email = request.form.get("email")
    password = request.form.get("password")

    print(name)
    print(surname)
    print(email)
    print(password)
    data.customer_id = DataStore.db.create_customer(name, surname, password, email).customer_id
    return redirect("/customer_account")

@APP.route("/customer_account")
def customer_account():
    """Cusomer page

    TO DO
    !!!Доробти, щоб після вибору мережі, було вижно одразу доступні команди
    !!!Кнопка додати мережу"""
    return render_template("customer_account.html")

@APP.route("/user_space")
def user_space():
    """User page"""
    return render_template("user_space.html")

# @APP.route("/add_styles", methods=["GET", "POST"])
# def add_style():
#     """Adding style"""
#     return render_template("add_style.html")
#
# @APP.route("/add_social_media", methods=["GET", "POST"])
# def add_style():
#     """Adding media"""
#     return render_template("add_social_media.html")
#
# @APP.route("/get_customer", methods=["GET", "POST"])
# def get_customer():
#     """Finding customer for order"""
#     return render_template("get_customer.html")
#

#
@APP.route("/create_order", methods=["GET"])
def create_order():
    """Creating order"""
    return render_template("create_order.html")

@APP.route("/create_order", methods=["POST"])
def order_creating():
    """Creating order

    !!!TO DO
    Зробити випадаючі списки
    Додати поле інша інформація
    кнопка "додати стиль"""
    style = request.form.get("style")
    team = request.form.get("team")
    media = request.form.get("media")
    print(style)
    print(team)
    print(media)
    return redirect("/finish_author")

@APP.route("/past_orders")
def past_orders():
    """Information about orders

    !!!TO DO
    Доробити сторінку"""
    return render_template("past_orders.html")
#
# @APP.route("/give_access", methods=["GET", "POST"])
# def give_access():
#     """Giving access"""
#     return render_template("give_access.html")
#
# @APP.route("/deny_access", methods=["GET", "POST"])
# def deny_access():
#     """Denying access"""
#     return render_template("deny_access.html")


# @APP.route("/status_page", methods=["GET", "POST"])
# def status_page():
#     """Order status page with access buttoms, result and evaluating"""
#     return render_template("status_page.html")
#
@APP.route("/finish_author", methods=["GET", "POST"])
def finish_author():
    """Result page for discount creating"""
    return render_template("finish_author.html")

if __name__ == "__main__":
    APP.run(debug=True)
