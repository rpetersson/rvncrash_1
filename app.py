from flask import Flask, session, request, Response, render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import time
import random
import sqlite3

app = Flask(__name__)

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

dict_bets = {}

def game_engine():
    counter = 1
    initial_chance = 100
    multipel_increment = 0.01
    game_crash = False

    while not game_crash:
        # round start

        initial_chance = initial_chance - multipel_increment
        counter = counter + multipel_increment
        #print(round(counter, 2))
        time.sleep(0.1)
        yield "data: {}\n\n".format(round(counter, 2))
        if random.uniform(0.01, 100) > initial_chance:
            game_crash = True
            #print("GAME CRASHED @ " + str(counter))
            yield "data: {}\n\n".format("CRASH! " + str(round(counter, 2)))
            time.sleep(2)
            yield "data: {}\n\n".format("Starting in..")
            time.sleep(2)
            yield "data: {}\n\n".format("1")
            time.sleep(2)
            yield "data: {}\n\n".format("2")
            time.sleep(2)
            yield "data: {}\n\n".format("3")
            time.sleep(2)
            counter = 1
            game_crash = False
            game_crashed_at = counter
            yield game_crashed_at

            game_engine()

@app.route("/index", methods=["POST","GET"])
@app.route("/", methods=["POST","GET"])
@login_required
def index():
    #bet_form_handler
    if request.method == "POST":
        bet = request.form["bet"]
        cashout = request.form["cashout"]

    return render_template("index.html",)

@app.route("/login", methods=["POST","GET"])
def login():

    if request.method == "POST":
        db = sqlite3.connect("./db.db")
        c = db.cursor()
        c.execute("SELECT * FROM users")
        usr = c.fetchall()
        print(usr)
        username = request.form["form_username"]
        password = request.form["form_password"]

        for i in usr:
            if i[1] == username and i[3] == password:
                id = i[1]
                user = User(id)
                login_user(user)
                print("Authenticated... redirect please...")
                session["logged_in"] = True
                return render_template("index.html")

        db.close()



    return render_template("login.html")

@app.route("/register", methods=["POST","GET"])
def register():

    if request.method == "POST":
        print("user form submitted...")
        usr = request.form["usr"]
        email = request.form["email"]
        pwd = request.form["pwd"]
        print(usr,pwd,email)
        db = sqlite3.connect("./db.db")
        c = db.cursor()
        c.execute("INSERT INTO users(usr,email,pwd) VALUES (?,?,?)",(usr, email, pwd,))
        db.commit()
        db.close()
        return render_template("index.html")


    return render_template("register.html")

@app.route("/stream")
def stream():

    return Response(game_engine(), mimetype="text/event-stream")

@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()

    return render_template("logout.html")

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()

