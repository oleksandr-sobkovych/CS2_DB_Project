from flask import Flask, render_template, request, jsonify, redirect

APP = Flask(__name__)

APP.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@APP.route("/")
def index():
    """Start page (choose author or customer)"""
    return render_template("index.html")

# @APP.route("/login_or_create_author", methods=["GET", "POST"])
# def login_or_create_author():
#     """Choose login or create an new account as author"""
#     return render_template("login_or_create_author.html")

@APP.route("/author_login", methods=["GET"])
def create_author():
    """Login page for authors"""
    return render_template("author_login.html")


@APP.route("/author_login", methods=["POST"])
def login_author():
    """Login page for authors"""
    email = request.form.get("email")
    password = request.form.get("password")

    print(email)
    print(password)

    # get name, last_name, password params
    # create_author_account(name, surname, password)
    return redirect("/author_account")

# @APP.route("/author_signup", methods=["GET", "POST"])
# def author_signup():
#     """Page for author signing up"""
#     return render_template("author_signup.html")
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
    return redirect("/manage_task")

# @APP.route("/task", methods=["GET", "POST"])
# def author_signup():
#     """Page for author signing up"""
#     return render_template("author_signup.html")

@APP.route("/manage_task", methods=["GET", "POST"])
def manage_task():
    """Manage page for authors (creating discount or team)"""
    return render_template("manage_task.html")

@APP.route("/discount", methods=["GET", "POST"])
def discount():
    """Page for creating discount"""
    return render_template("discount.html")

# @APP.route("/create_customer", methods=["GET", "POST"])
# def create_customer():
#     """Creating customer page"""
#     return render_template("create_customer.html")
#
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
@APP.route("/one_day_discount", methods=["GET"])
def one_day_discount():
    """Page for creating 1 day discount"""
    return render_template("one_day_discount.html")

@APP.route("/one_day_discount", methods=["POST"])
def one_day_discount_post():
    from_ = request.form.get("from")
    to_ = request.form.get("to")
    print (from_)
    print (to_)
    return redirect("/finish_author")
#
# @APP.route("/create_order", methods=["GET", "POST"])
# def create_order():
#     """Creating order"""
#     return render_template("create_order.html")
#
# @APP.route("/create_multiple_days_discount", methods=["GET", "POST"])
# def create_multiple_days_discount():
#     """Creating discount"""
#     return render_template("create_multiple_days_discount.html")
#
# @APP.route("/orders", methods=["GET", "POST"])
# def orders():
#     """Information about orders"""
#     return render_template("orders.html")
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
#
@APP.route("/finish_author", methods=["GET", "POST"])
def finish_author():
    """Result page for discount creating"""
    return render_template("finish_author.html")

if __name__ == "__main__":
    APP.run(debug=True)
