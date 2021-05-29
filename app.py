from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime

from db_interaction import DBInteraction

APP = Flask(__name__)


class DataStore:
    db = DBInteraction()
    author_id = None
    style_name = None
    customer_id = None


data = DataStore()


@APP.route("/")
def index():
    # http://127.0.0.1:8888/
    """Start page (choose author or customer)"""
    return render_template("index.html")


@APP.route("/login_or_create_author")
def login_or_create_author():
    # http://127.0.0.1:8888/login_or_create_author
    """Choose login or create an new account as author"""
    return render_template("login_or_create_author.html")


@APP.route("/author_login", methods=["GET"])
def author_login():
    # http://127.0.0.1:8888/author_login
    """Login page for authors"""
    return render_template("author_login.html")


@APP.route("/authors", methods=["GET"])
def get_authors():
    # http://127.0.0.1:8888/authors
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


@APP.route("/queries", methods=["GET"])
def queries():
    return render_template("queries.html")


@APP.route("/search_1", methods=["GET"])
def search_1():
    return render_template("query1_past_orders.html")


@APP.route("/search_results_1", methods=["GET"])
def search_results_1():
    # http://127.0.0.1:8888/search_results_1?author_id=3&mess_num=1&date_start=2021-01-01&date_end=2021-06-01
    author_id = request.args.get('author_id')
    mess_num = request.args.get('mess_num')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')

    if not (author_id and mess_num and date_start and date_end):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})

    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
        date_start = datetime.strftime(date_start, '%Y-%m-%d')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        date_end = datetime.strftime(date_end, '%Y-%m-%d')
    except:
        return jsonify({'status': 'error', 'reason': 'wrong date'})

    try:
        users = DataStore.db.search_1(author_id, mess_num, date_start, date_end)
        return jsonify({'status': 'ok', 'users': users})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})


@APP.route("/search_2", methods=["GET"])
def search_2():
    return render_template("query2_past_purchases.html")


@APP.route("/search_results_2", methods=["GET"])
def search_results_2():
    # http://127.0.0.1:8888/search_results_2?customer_id=3&date_start=2021-01-01&date_end=2021-06-01
    customer_id = request.args.get('customerID')
    date_start = request.args.get('dateStart')
    date_end = request.args.get('dateEnd')

    if not (customer_id and date_start and date_end):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})

    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
        date_start = datetime.strftime(date_start, '%Y-%m-%d')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        date_end = datetime.strftime(date_end, '%Y-%m-%d')
    except:
        return jsonify({'status': 'error', 'reason': 'wrong date'})

    try:
        users = DataStore.db.search_2(customer_id,date_start,date_end)
        return jsonify({'status': 'ok', 'users': users})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})


@APP.route("/search_3", methods=["GET"])
def search_3():
    return render_template("query3_min_n_customers.html")

@APP.route("/search_results_3", methods=["GET"])
def search_results_3():
    # http://127.0.0.1:8888/search_results_3?date_start=2021-01-01&date_end=2021-06-01&ids=2
    
    numCustomer = request.args.get('numCustomer')
    date_start = request.args.get('dateStart')
    date_end = request.args.get('dateEnd')


    if not (numCustomer and date_start and date_end):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})

    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
        date_start = datetime.strftime(date_start, '%Y-%m-%d')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        date_end = datetime.strftime(date_end, '%Y-%m-%d')
    except:
        return jsonify({'status': 'error', 'reason': 'wrong date'})

    try:
        users = DataStore.db.search_3(numCustomer,date_start,date_end)
        return jsonify({'status': 'ok', 'users': users})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})


@APP.route("/search_4", methods=["GET"])
def search_4():
    return render_template("query4_customers_with_norders.html")

@APP.route("/search_results_4", methods=["GET"])
def search_results_4():
    # http://127.0.0.1:8888/search_results_4?date_start=2021-01-01&date_end=2021-06-01&order_id=2

    numOrders=request.args.get('numOrders')
    date_start=request.args.get('dateStart')
    date_end=request.args.get('dateEnd')


    if not (numOrders and date_start and date_end):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})

    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
        date_start = datetime.strftime(date_start, '%Y-%m-%d')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        date_end = datetime.strftime(date_end, '%Y-%m-%d')
    except:
        return jsonify({'status': 'error', 'reason': 'wrong date'})

    try:
        users = DataStore.db.search_4(numOrders,date_start,date_end)
        return jsonify({'status': 'ok', 'users': users})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})

@APP.route("/search_5", methods=["GET"])
def search_5():
    return render_template("query5_socialmedia_norders.html")

@APP.route("/search_results_5", methods=["GET"])
def search_results_5():
    # http://127.0.0.1:8888/search_results_5?customer_id=1&date_start=2021-01-01&date_end=2021-06-01&count=1

    customer_id = request.args.get('customerID')
    numOrders = request.args.get('numOrders')
    date_start = request.args.get('dateStart')
    date_end = request.args.get('dateEnd')


    if not (customer_id and numOrders and date_start and date_end):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})

    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
        date_start = datetime.strftime(date_start, '%Y-%m-%d')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        date_end = datetime.strftime(date_end, '%Y-%m-%d')
    except:
        return jsonify({'status': 'error', 'reason': 'wrong date'})

    try:
        users = DataStore.db.search_5(customer_id, numOrders,date_start,date_end)
        return jsonify({'status': 'ok', 'users': users})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})


@APP.route("/search_6", methods=["GET"])
def search_6():
    return render_template("query6_socialmedia_accounts.html")

@APP.route("/search_results_6", methods=["GET"])
def search_results_6():
    # http://127.0.0.1:8888/search_results_6?date_start=2021-01-01&date_end=2021-06-01&author_id=2
    author_id=request.args.get('authorID')
    date_start=request.args.get('dateStart')
    date_end=request.args.get('dateEnd')
      

    if not (author_id and date_start and date_end):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})

    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
        date_start = datetime.strftime(date_start, '%Y-%m-%d')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        date_end = datetime.strftime(date_end, '%Y-%m-%d')
    except:
        return jsonify({'status': 'error', 'reason': 'wrong date'})

    try:
        users = DataStore.db.search_6(author_id,date_start,date_end)
        return jsonify({'status': 'ok', 'users': users})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})

@APP.route("/search_7", methods=["GET"])
def search_7():
    return render_template("query7_access_given.html")

@APP.route("/search_results_7", methods=["GET"])
def search_results_7():
    # http://127.0.0.1:8888/search_results_7?customer_id=1
    customer_id=request.args.get('customerID')
      

    if not (customer_id):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})


    try:
        users = DataStore.db.search_7(customer_id)
        return jsonify({'status': 'ok', 'users': users})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})



@APP.route("/search_8", methods=["GET"])
def search_8():
    return render_template("query8_common_actions.html")

@APP.route("/search_results_8", methods=["GET"])
def search_results_8():
    # http://127.0.0.1:8888/search_results_8?customer_id=1&date_start=2021-01-01&date_end=2021-06-01&author_id=2
      
    author_id=request.args.get('authorID')
    customerID=request.args.get('customerID')
    date_start=request.args.get('dateStart')
    date_end=request.args.get('dateEnd')

    if not (customerID and author_id and date_start and date_end):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})

    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
        date_start = datetime.strftime(date_start, '%Y-%m-%d')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        date_end = datetime.strftime(date_end, '%Y-%m-%d')
    except:
        return jsonify({'status': 'error', 'reason': 'wrong date'})

    try:
        users = DataStore.db.search_8(author_id,customerID, date_start,date_end)
        return jsonify({'status': 'ok', 'users': users})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})

@APP.route("/search_9", methods=["GET"])
def search_9():
    return render_template("query9_each_social_media_nauthors.html")

@APP.route("/search_results_9", methods=["GET"])
def search_results_9():
    # http://127.0.0.1:8888/search_results_9?customer_id=1&date_start=2021-01-01&date_end=2021-06-01&author_id=2
    author_id=request.args.get('authorID')
    num_authors=request.args.get('num')
    date_start=request.args.get('dateStart')
    date_end=request.args.get('dateEnd')

    if not (num_authors and author_id and date_start and date_end):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})

    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
        date_start = datetime.strftime(date_start, '%Y-%m-%d')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        date_end = datetime.strftime(date_end, '%Y-%m-%d')
    except:
        return jsonify({'status': 'error', 'reason': 'wrong date'})

    try:
        users = DataStore.db.search_9(author_id,num_authors, date_start,date_end)
        return jsonify({'status': 'ok', 'users': users})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})

@APP.route("/search_10", methods=["GET"])
def search_10():
    return render_template("query10_num_discounts.html")

@APP.route("/search_results_10", methods=["GET"])
def search_results_10():
    # http://127.0.0.1:8888/search_results_10?customer_id=2&date_start=2021-01-01&date_end=2021-06-01
    customer_id=request.args.get('customerID')
    date_start=request.args.get('dateStart')
    date_end=request.args.get('dateEnd')

    if not (customer_id and date_start and date_end):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})

    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
        date_start = datetime.strftime(date_start, '%Y-%m-%d')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        date_end = datetime.strftime(date_end, '%Y-%m-%d')
    except:
        return jsonify({'status': 'error', 'reason': 'wrong date'})

    try:
        users = DataStore.db.search_10(customer_id, date_start,date_end)
        return jsonify({'status': 'ok', 'users': users})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})

@APP.route("/search_11", methods=["GET"])
def search_11():
    return render_template("query11_num_places.html")

@APP.route("/search_results_11", methods=["GET"])
def search_results_11():
    # http://127.0.0.1:8888/search_results_11?year=2021
    year = request.args.get('year')

    users = DataStore.db.search_11(year)
    return jsonify({'status': 'ok', 'users': users})

@APP.route("/search_12", methods=["GET"])
def search_12():
    return render_template("query12_social_medial_nmessage.html")

@APP.route("/search_results_12", methods=["GET"])
def search_results_12():
    # http://127.0.0.1:8888/search_results_12?customer_id=1&date_start=2021-01-01&date_end=2021-06-01
    author_id=request.args.get('authorID')
    date_start=request.args.get('dateStart')
    date_end=request.args.get('dateEnd')

    if not (author_id and date_start and date_end):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})

    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
        date_start = datetime.strftime(date_start, '%Y-%m-%d')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        date_end = datetime.strftime(date_end, '%Y-%m-%d')
    except:
        return jsonify({'status': 'error', 'reason': 'wrong date'})

    try:
        users = DataStore.db.search_12(author_id, date_start,date_end)
        return jsonify({'status': 'ok', 'users': users})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})


@APP.route("/get_author_by_id", methods=["GET"])
def get_author_by_id():
    author_id = request.args.get("author_id")

    if not author_id:
        return jsonify({'status': 'error', 'reason': 'no author_id'})

    try:
        author_id = int(author_id)
        author = DataStore.db.get_author(author_id)
    except:
        return jsonify({'status': 'error', 'reason': 'such author has not been found'})

    return jsonify({'status': 'ok', 'data': {
        'author_id': author.author_id,
        'name': author.first_name + ' ' + author.last_name
    }})


@APP.route("/author_login", methods=["POST"])
def login_author():
    # http://127.0.0.1:8888/author_login
    """Login page for authors"""
    email = request.json.get("email")
    password = request.json.get("password")

    print(email)
    print(password)
    if not (email and password):
        return jsonify({'status': 'error', 'reason': 'no email or password'})

    try:
        data.author_id = DataStore.db.get_author_by_email_and_password(email,
                                                                       password).author_id
    except AttributeError:
        return jsonify({'status': 'error', 'reason': 'such author has not been found'})

    return jsonify({'status': 'ok', 'data': {'author_id': data.author_id}})


@APP.route("/author_signup", methods=["GET"])
def author_signup():
    # http://127.0.0.1:8888/author_signup
    """Page for author signing up"""
    return render_template("author_signup.html")


@APP.route("/author_signup", methods=["POST"])
def create_author():
    # http://127.0.0.1:8888/author_signup
    """Creating author account"""
    name = request.json.get("name")
    surname = request.json.get("surname")
    email = request.json.get("email")
    password = request.json.get("password")

    if not (name and surname and email and password):
        return jsonify({'status': 'error', 'reason': 'parameters are empty'})

    try:
        data.author_id = DataStore.db.create_author_account(name, surname,
                                                        password, email)
        return jsonify({'status': 'ok'})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})


@APP.route("/choose_styles", methods=["GET"])
def choose_styles():
    # http://127.0.0.1:8888/choose_styles
    """Page for choosing style and then seeing possible tasks

    TODO:
        !!!Seeing possible tasks
        !!!Choose many styles
    """
    return render_template("choose_styles.html")


@APP.route("/author_account", methods=["POST"])
def author_account_post():
    style = request.form.get("style")
    print(style)
    data.style_name = [style]
    DataStore.db.add_skill(data.author_id, [style])
    return redirect("/author_account")


# @APP.route("/task", methods=["GET", "POST"])
# def task():
#     """Page for author tasking doing"""
#     return render_template("task.html")

# @APP.route("/finishing_task", methods=["GET", "POST"])
# def finishing_task():
#     """Page for author tasking doing finish with buttom
#     @Do yoou want to give some discount@"""
#     return render_template("finishing_task.html")

@APP.route("/author_account")
def author_account():
    # http://127.0.0.1:8888/author_account
    """Manage page for authors (creating discount or team)

    TODO: !!!Do it as a menu buttom
    """
    return render_template("author_account.html")


@APP.route("/multiple_days_discount", methods=["GET"])
def multiple_days_discount():
    # http://127.0.0.1:8888/multiple_days_discount
    """Page for creating discount"""
    return render_template("multiple_days_discount.html")


@APP.route("/multiple_days_discount", methods=["POST"])
def multiple_days_discount_post():
    # http://127.0.0.1:8888/multiple_days_discount
    From = datetime.strptime(request.form.get("From"), "%d.%m")
    print(From)
    To = datetime.strptime(request.form.get("To"))
    print(To)
    DataStore.db.create_multiple_days_discount(data.author_id, data.style_name, 5, From, To)
    return redirect("/finish_author")


@APP.route("/create_team", methods=["GET", "POST"])
def create_team():
    # http://127.0.0.1:8888/create_team
    """Page for creating team

    TODO: !!!Create_team.html доробити
    """
    return render_template("create_team.html")


@APP.route("/one_day_discount", methods=["GET"])
def one_day_discount():
    # http://127.0.0.1:8888/one_day_discount
    """Page for creating 1 day discount"""
    return render_template("one_day_discount.html")


@APP.route("/one_day_discount", methods=["POST"])
def one_day_discount_post():
    from_ = datetime.strptime(request.form.get("from"), "%d.%m")
    to_ = request.form.get("discount_number")
    print(from_)
    print(to_)
    DataStore.db.create_one_day_discount(data.author_id, data.style_name,
                                         to_, from_)
    return redirect("/finish_author")


@APP.route("/login_or_create_customer")
def login_or_create_customer():
    # http://127.0.0.1:8888/login_or_create_customer
    """Choose login or create an new account as customer

    TODO: !ПОПРАВИТИ CSS
        """
    return render_template("login_or_create_customer.html")


@APP.route("/customer_login", methods=["GET"])
def customer_login():
    # http://127.0.0.1:8888/customer_login
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
    # http://127.0.0.1:8888/customer_signup
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
    # http://127.0.0.1:8888/customer_account
    """Cusomer page

    TODO
        !!!Доробти, щоб після вибору мережі, було вижно одразу доступні команди
        !!!Кнопка додати мережу
    """
    return render_template("customer_account.html")


@APP.route("/user_space")
def user_space():
    # http://127.0.0.1:8888/user_space
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
    # http://127.0.0.1:8888/create_order
    """Creating order"""
    return render_template("create_order.html")


@APP.route("/create_order", methods=["POST"])
def order_creating():
    # http://127.0.0.1:8888/create_order
    """Creating order

    !!!
    TODO Зробити випадаючі списки
        Додати поле інша інформація
        кнопка "додати стиль
    """
    style = request.form.get("style")
    team = request.form.get("team")
    media = request.form.get("media")
    print(style)
    print(team)
    print(media)
    return redirect("/finish_author")

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
    # http://127.0.0.1:8888/finish_author
    """Result page for discount creating"""
    return render_template("finish_author.html")


if __name__ == "__main__":
    APP.run(debug=True, port=8888)
