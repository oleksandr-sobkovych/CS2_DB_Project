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


@APP.route("/customers", methods=["GET"])
def get_customers():
    # http://127.0.0.1:8888/authors
    names = []
    customers = DataStore.db.get_customers()
    for customer in customers:
        names.append({
            'name': "%s %s" % (customer.first_name, customer.last_name),
            'customer_id': customer.customer_id,
            'email': customer.email,
        })
    return jsonify({'status': 'ok', 'customers': names})


@APP.route("/all_media", methods=["GET"])
def get_all_media():
    names = []
    media = DataStore.db.get_networks()
    for one_media in media:
        names.append({
            'name': one_media.media_name,
            'media_id': one_media.media_id,
        })
    return jsonify({'status': 'ok', 'media': names})


@APP.route("/choose_media", methods=["POST"])
def add_medias():
    """DB request for adding medias and creating accounts in them."""
    customer_id = request.json.get('customer_id')
    customer = DataStore.db.get_customer(customer_id)

    # account = DataStore.db.get_account_by_customer_and_media()

    if not customer:
        return jsonify(
            {'status': 'error', 'reason': 'customer does not exist with this id'})
    try:
        DataStore.db.add_customer_medias(customer_id, request.json.get("chosen_media"))
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'database error: ' + str(e)})


@APP.route("/get_orders", methods=["GET"])
def get_orders():
    customer_id = request.args.get('customer_id')
    customer = DataStore.db.get_customer(customer_id)

    if not customer:
        return jsonify(
            {'status': 'error', 'reason': 'customer does not exist with this id'})

    try:
        orders = DataStore.db.get_orders_of(customer_id)
        data = []
        for order in orders:
            data.append({
                'order_id': order.order_id,
                'account_id': order.account_id,
                'team_id': order.team_id,
                'message_id': order.message_id
            })
        return jsonify({'status': 'ok', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'database error: ' + str(e)})


@APP.route("/give_access", methods=["POST"])
def give_access():
    """DB request for adding medias and creating accounts in them."""
    customer_id = request.args.get('customer_id')
    order_id = request.json.get("order_id")

    order = DataStore.db.get_order(order_id)

    if not order:
        return jsonify(
            {'status': 'error',
             'reason': 'order does not exist with this id'})

    account_id = order.account_id
    media_id = DataStore.db.get_account(account_id).media_id
    team_id = order.team_id

    try:
        access = DataStore.db.create_access(account_id, team_id)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'database error: ' + str(e)})


@APP.route("/deny_access", methods=["POST"])
def deny_access():
    customer_id = request.args.get('customer_id')
    order_id = request.json.get("order_id")

    order = DataStore.db.get_order(order_id)

    if not order:
        return jsonify(
            {'status': 'error',
             'reason': 'order does not exist with this id'})

    account_id = order.account_id
    media_id = DataStore.db.get_account(account_id).media_id
    team_id = order.team_id

    try:
        DataStore.db.deny_access(account_id, team_id)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'database error: ' + str(e)})


@APP.route("/customer_media", methods=["GET"])
def get_customer_media():
    customer_id = request.args.get('customer_id')
    customer = DataStore.db.get_customer(customer_id)

    if not customer:
        return jsonify(
            {'status': 'error', 'reason': 'author does not exist with this id'})

    names = []
    media = DataStore.db.get_customer_media(customer_id)
    print(media)
    for one_media in media:
        names.append({
            'name': one_media[1],
            'media_id': one_media[0],
        })
    return jsonify({'status': 'ok', 'media': names})


@APP.route("/all_teams", methods=["GET"])
def get_all_teams():
    names = []
    teams = DataStore.db.get_teams()
    for team in teams:
        names.append({
            'name': team.team_name,
            'team_id': team.team_id,
        })
    return jsonify({'status': 'ok', 'teams': names})


@APP.route("/all_styles", methods=["GET"])
def get_all_styles():
    names = []
    styles = DataStore.db.get_styles()
    for style in styles:
        names.append({
            'name': style.style_name,
            'style_id': style.style_id,
            'authors': [author.author_id for author in style.authors]
        })
    return jsonify({'status': 'ok', 'styles': names})


@APP.route("/author_styles", methods=["GET"])
def get_author_styles():
    author_id = request.args.get('author_id')
    author = DataStore.db.get_author(author_id)
    if not author:
        return jsonify({'status': 'error', 'reason': 'author does not exist with this id'})

    names = []
    styles = DataStore.db.get_styles()
    for style in styles:
        if style.style_id in [st.style_id for st in author.styles]:
            names.append({
                'name': style.style_name,
                'style_id': style.style_id,
                'authors': [author.author_id for author in style.authors]
            })
    return jsonify({'status': 'ok', 'styles': names})


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
        return jsonify({'status': 'ok', 'users': [dict(user) for user in users]})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})


@APP.route("/search_2", methods=["GET"])
def search_2():
    return render_template("query2_past_purchases.html")


@APP.route("/search_results_2", methods=["GET"])
def search_results_2():
    # http://127.0.0.1:8888/search_results_2?customer_id=3&date_start=2021-01-01&date_end=2021-06-01
    customer_id = request.args.get('customer_id')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
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
        users = DataStore.db.search_2(int(customer_id),date_start,date_end)
        return jsonify({'status': 'ok', 'users': [dict(user) for user in users]})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})


@APP.route("/search_3", methods=["GET"])
def search_3():
    return render_template("query3_min_n_customers.html")

@APP.route("/search_results_3", methods=["GET"])
def search_results_3():
    # http://127.0.0.1:8888/search_results_3?date_start=2021-01-01&date_end=2021-06-01&ids=2
    
    numCustomer = request.args.get('numCustomer')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
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
        users = DataStore.db.search_3(date_start,date_end,numCustomer)
        return jsonify({'status': 'ok', 'users': [dict(user) for user in users]})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})


@APP.route("/search_4", methods=["GET"])
def search_4():
    return render_template("query4_customers_with_norders.html")

@APP.route("/search_results_4", methods=["GET"])
def search_results_4():
    # http://127.0.0.1:8888/search_results_4?date_start=2021-01-01&date_end=2021-06-01&order_id=2

    numOrders = request.args.get('numOrders')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
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
        users = DataStore.db.search_4(date_start,date_end,numOrders)
        return jsonify({'status': 'ok', 'users': [dict(user) for user in users]})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})

@APP.route("/search_5", methods=["GET"])
def search_5():
    return render_template("query5_socialmedia_norders.html")

@APP.route("/search_results_5", methods=["GET"])
def search_results_5():
    # http://127.0.0.1:8888/search_results_5?customer_id=1&date_start=2021-01-01&date_end=2021-06-01&count=1

    customer_id = request.args.get('customer_id')
    numOrders = request.args.get('numOrders')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')


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
        users = DataStore.db.search_5(customer_id,date_start,date_end, numOrders)
        return jsonify({'status': 'ok', 'users': [dict(user) for user in users]})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})


@APP.route("/search_6", methods=["GET"])
def search_6():
    return render_template("query6_socialmedia_accounts.html")

@APP.route("/search_results_6", methods=["GET"])
def search_results_6():
    # http://127.0.0.1:8888/search_results_6?date_start=2021-01-01&date_end=2021-06-01&author_id=2
    author_id=request.args.get('author_id')
    date_start=request.args.get('date_start')
    date_end=request.args.get('date_end')
      

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
        users = DataStore.db.search_6(date_start,date_end, author_id)
        return jsonify({'status': 'ok', 'users': [dict(user) for user in users]})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})

@APP.route("/search_7", methods=["GET"])
def search_7():
    return render_template("query7_access_given.html")

@APP.route("/search_results_7", methods=["GET"])
def search_results_7():
    # http://127.0.0.1:8888/search_results_7?customer_id=1
    customer_id=request.args.get('customer_id')
      

    if not (customer_id):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})


    try:
        users = DataStore.db.search_7(customer_id)
        return jsonify({'status': 'ok', 'users': [dict(user) for user in users]})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})



@APP.route("/search_8", methods=["GET"])
def search_8():
    return render_template("query8_common_actions.html")

@APP.route("/search_results_8", methods=["GET"])
def search_results_8():
    # http://127.0.0.1:8888/search_results_8?customer_id=1&date_start=2021-01-01&date_end=2021-06-01&author_id=2
      
    author_id=request.args.get('author_id')
    customerID=request.args.get('customerID')
    date_start=request.args.get('date_start')
    date_end=request.args.get('date_end')

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
        users = DataStore.db.search_8(customerID,author_id, date_start,date_end)
        return jsonify({'status': 'ok', 'users': [dict(user) for user in users]})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})

@APP.route("/search_9", methods=["GET"])
def search_9():
    return render_template("query9_each_social_media_nauthors.html")

@APP.route("/search_results_9", methods=["GET"])
def search_results_9():
    # http://127.0.0.1:8888/search_results_9?customer_id=1&date_start=2021-01-01&date_end=2021-06-01&author_id=2
    author_id=request.args.get('author_id')
    num_authors=request.args.get('num_authors')
    date_start=request.args.get('date_start')
    date_end=request.args.get('date_end')

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
        return jsonify({'status': 'ok', 'users': [dict(user) for user in users]})
    except Exception as e:
        return jsonify({'status': 'error', 'reason': e.args[0]})

@APP.route("/search_10", methods=["GET"])
def search_10():
    return render_template("query10_num_discounts.html")

@APP.route("/search_results_10", methods=["GET"])
def search_results_10():
    # http://127.0.0.1:8888/search_results_10?customer_id=2&date_start=2021-01-01&date_end=2021-06-01
    customer_id=request.args.get('customer_id')
    date_start=request.args.get('date_start')
    date_end=request.args.get('date_end')

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
        return jsonify({'status': 'ok', 'users': [dict(user) for user in users]})
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
    print(users)
    if not users:
        return jsonify({'status': 'ok', 'users': []})
    return jsonify({'status': 'ok', 'users': [dict(user) for user in users]})

@APP.route("/search_12", methods=["GET"])
def search_12():
    return render_template("query12_social_medial_nmessage.html")

@APP.route("/search_results_12", methods=["GET"])
def search_results_12():
    # http://127.0.0.1:8888/search_results_12?customer_id=1&date_start=2021-01-01&date_end=2021-06-01
    author_id=request.args.get('author_id')
    date_start=request.args.get('date_start')
    date_end=request.args.get('date_end')

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
        return jsonify({'status': 'ok', 'users': [dict(user) for user in users]})
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})


@APP.route("/get_customer_by_id", methods=["GET"])
def get_customer_by_id():
    customer_id = request.args.get("customer_id")

    if not customer_id:
        return jsonify({'status': 'error', 'reason': 'no customer_id'})

    try:
        customer_id = int(customer_id)
        customer = DataStore.db.get_customer(customer_id)
    except:
        return jsonify({'status': 'error', 'reason': 'such customer has not been found'})

    return jsonify({'status': 'ok', 'data': {
        'author_id': customer.customer_id,
        'name': customer.first_name + ' ' + customer.last_name
    }})


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
                                                        password, email).author_id
        return jsonify({'status': 'ok', 'data': {'author_id': data.author_id}})
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'database error : ' + str(e)})


@APP.route("/choose_styles", methods=["GET"])
def choose_styles():
    """Page for choosing style and then seeing possible tasks
    TODO: !!!Seeing possible tasks
    """
    return render_template("choose_styles.html")


@APP.route("/author_account", methods=["POST"])
def author_account_post():
    style = request.form.get("style")
    print(style)
    data.style_name = [style]
    DataStore.db.add_skill(data.author_id, [style])
    return redirect("/author_account")


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
    author_id = request.json.get('author_id')
    date_start = request.json.get('date_from')
    date_end = request.json.get('date_to')
    amount = request.json.get('amount')
    style_id = request.json.get('style_id')

    print(author_id, date_start, date_end, amount, style_id)

    if not (author_id and date_start and date_end and amount and style_id):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})

    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
    except:
        return jsonify({'status': 'error', 'reason': 'wrong date'})

    try:
        if DataStore.db.create_multiple_days_discount(author_id,
                                                   style_id, amount, date_start,
                                                   date_end):
            return jsonify({'status': 'ok'})
        else:
            return jsonify({'status': 'error', 'reason': 'wrong parameters'})
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'database error, ' + str(e)})


@APP.route("/create_team", methods=["GET", "POST"])
def create_team():
    # http://127.0.0.1:8888/create_team
    """Page for creating team

    TODO: !!!Create_team.html ????????????????
    """
    return render_template("create_team.html")


@APP.route("/one_day_discount", methods=["GET"])
def one_day_discount():
    # http://127.0.0.1:8888/one_day_discount
    """Page for creating 1 day discount"""
    return render_template("one_day_discount.html")


@APP.route("/one_day_discount", methods=["POST"])
def one_day_discount_post():
    author_id = request.json.get('author_id')
    date_start = request.json.get('date_from')
    amount = request.json.get('amount')

    print(author_id, date_start, amount)

    if not (author_id and date_start and amount):
        return jsonify({'status': 'error', 'reason': 'lacking parameters'})

    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
    except:
        return jsonify({'status': 'error', 'reason': 'wrong date'})

    try:
        if DataStore.db.create_one_day_discount(author_id, amount, date_start):
            return jsonify({'status': 'ok'})
        else:
            return jsonify({'status': 'error', 'reason': 'wrong parameters'})
    except Exception as e:
        return jsonify(
            {'status': 'error', 'reason': 'database error, ' + str(e)})


@APP.route("/create_order", methods=["POST"])
def create_order_post():
    customer_id = request.json.get("customer_id")
    style_id = request.json.get("style_id")
    team_id = request.json.get("team_id")
    media_id = request.json.get("media_id")

    print(customer_id, style_id, team_id, media_id)

    if not (style_id and team_id and media_id):
        return jsonify({'status': 'error', 'reason': 'no parameters'})

    account = DataStore.db.get_account_by_customer_and_media(int(customer_id), int(media_id))

    try:
        order = DataStore.db.create_order(account.account_id, team_id, style_id)
    except AttributeError:
        return jsonify({'status': 'error', 'reason': 'database error'})

    return jsonify({'status': 'ok', 'data': {'order_id': order.order_id}})


@APP.route("/login_or_create_customer")
def login_or_create_customer():
    # http://127.0.0.1:8888/login_or_create_customer
    """Choose login or create an new account as customer"""
    return render_template("login_or_create_customer.html")


@APP.route("/customer_login", methods=["GET"])
def customer_login():
    # http://127.0.0.1:8888/customer_login
    """Cusomer login page"""
    return render_template("customer_login.html")


@APP.route("/customer_login", methods=["POST"])
def login_customer():
    """Login page for customers"""
    email = request.json.get("email")
    password = request.json.get("password")

    if not (email and password):
        return jsonify({'status': 'error', 'reason': 'no email or password'})

    try:
        data.customer_id = DataStore.db.get_customer_by_email_and_password(
            email, password).customer_id
    except AttributeError:
        return jsonify(
            {'status': 'error', 'reason': 'such customer has not been found'})

    return jsonify({'status': 'ok', 'data': {'customer_id': data.customer_id}})


@APP.route("/choose_styles", methods=["POST"])
def choose_author_styles():
    """DB request for choosing styles."""
    author_id = request.json.get("author_id")
    styles = request.json.get("chosen_styles")
    try:
        DataStore.db.add_skill(author_id, styles)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'database error: ' + str(e)})


@APP.route("/customer_signup", methods=["GET"])
def customer_signup():
    """Cusomer signup page"""
    return render_template("customer_singup.html")


@APP.route("/customer_signup", methods=["POST"])
def customer_signup_post():
    # http://127.0.0.1:8888/author_signup
    """Creating customer account"""
    name = request.json.get("name")
    surname = request.json.get("surname")
    email = request.json.get("email")
    password = request.json.get("password")

    if not (name and surname and email and password):
        return jsonify({'status': 'error', 'reason': 'parameters are empty'})

    try:
        data.customer_id = DataStore.db.create_customer(name, surname,
                                                        password,
                                                        email).customer_id
    except:
        return jsonify({'status': 'error', 'reason': 'database error'})

    return jsonify({'status': 'ok', 'customer_id': data.customer_id})


@APP.route("/choose_media")
def choose_media():
    """Cusomer page"""
    return render_template("choose_media.html")


@APP.route("/customer_account")
def customer_account():
    """User page"""
    return render_template("customer_account.html")


@APP.route("/access")
def access():
    return render_template("access.html")


@APP.route("/create_order", methods=["GET"])
def create_order():
    # http://127.0.0.1:8888/create_order
    """Creating order"""
    return render_template("create_order.html")


if __name__ == "__main__":
    APP.run(debug=True, port=8888)



