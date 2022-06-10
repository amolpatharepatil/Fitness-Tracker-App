from flask import Flask, render_template, request, flash, jsonify, redirect
from pymongo import MongoClient
import os, json
import datetime, pytz
import random
from flask_mysqldb import MySQL
from collections import defaultdict

app = Flask(__name__)

# Config MySQL
mysql = MySQL()
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "1234"
app.config["MYSQL_DB"] = "fitness_tracker"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql.init_app(app)


def temp():
    workouts = [
        "Running",
        "Cycling",
        "Trekking",
        "Skipping",
        "Bicep Curls",
        "Tricep Extensions",
        "Dips",
        "Front Raise",
        "Shoulder Press",
        "Dumbbell Shrugs",
        "Pull-ups",
        "Deadlift",
        "Lat Pull Down",
        "Push-ups",
        "Inclined Dumbbell Flies",
    ]
    eID = []
    planids = ["001", "002", "003"]
    cur = mysql.connection.cursor()
    for one in workouts:
        ExerciseID = str(random.randrange(100, 999))
        PlanID = random.choice(planids)
        exe = cur.execute(
            "insert into `Exercises` (`ExerciseID`,`PlanID`, `Exercise`) values('"
            + ExerciseID
            + "','"
            + PlanID
            + "','"
            + one
            + "')"
        )
        mysql.connection.commit()


@app.route("/")
def home():
    temp()
    return render_template("index.html")


@app.route("/login_signup")
def login_signup():
    return render_template("loginSignup.html", status=0)


@app.route("/trainer_login_signup")
def trainer_login_signup():
    return render_template("trainerLoginSignup.html", status=0)


@app.route("/signup_user", methods=["POST", "GET"])
def signup_user():
    name = request.form.get("name", "")
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    print(name, password, email, "YO")
    cur = mysql.connection.cursor()
    exe = cur.execute(
        "insert into `users` (`Name`,`Password`,`Email`) values('"
        + name
        + "','"
        + password
        + "','"
        + email
        + "')"
    )
    mysql.connection.commit()
    exe = cur.execute("insert into `goals` (`Email`) values('" + email + "')")
    mysql.connection.commit()
    return render_template("dashboard.html", email=email)


@app.route("/signup_trainer", methods=["POST", "GET"])
def signup_trainer():
    name = request.form.get("name", "")
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    print(name, password, email, "YO")
    cur = mysql.connection.cursor()
    exe = cur.execute(
        "insert into `trainer` (`Name`,`Password`,`Email`) values('"
        + name
        + "','"
        + password
        + "','"
        + email
        + "')"
    )
    cur = mysql.connection.cursor()
    exe = cur.execute(
        "select count(*) as count from `trainer` where `Email` = '"
        + email
        + "' and `Password` = '"
        + password
        + "'"
    )
    user = list(cur.fetchall())
    user = user[0]["count"]
    wtArray = []
    exe = cur.execute("select * from `users`")
    users = list(cur.fetchall())
    print(users, "YOLO")
    for one in users:
        exe = cur.execute(
            "select * from `goals` where `Email` = '" + one["Email"] + "'"
        )
        cW = list(cur.fetchall())[0]
        wtArray.append(cW)
    mysql.connection.commit()
    return render_template(
        "trainerHome.html", email=email, users=users, wtArray=wtArray, lt=len(wtArray)
    )


@app.route("/login_user", methods=["POST", "GET"])
def login_user():
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    cur = mysql.connection.cursor()
    exe = cur.execute(
        "select count(*) as count from `users` where `Email` = '"
        + email
        + "' and `Password` = '"
        + password
        + "'"
    )
    user = list(cur.fetchall())
    user = user[0]["count"]
    if user == 1:
        return render_template("dashboard.html", email=email)
    return render_template("loginSignup.html", status=-1)


@app.route("/login_trainer", methods=["POST", "GET"])
def login_trainer():
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    cur = mysql.connection.cursor()
    exe = cur.execute(
        "select count(*) as count from `trainer` where `Email` = '"
        + email
        + "' and `Password` = '"
        + password
        + "'"
    )
    user = list(cur.fetchall())
    user = user[0]["count"]
    wtArray = []
    exe = cur.execute("select * from `users`")
    users = list(cur.fetchall())
    print(users, "YOLO")
    for one in users:
        exe = cur.execute(
            "select * from `goals` where `Email` = '" + one["Email"] + "'"
        )
        cW = list(cur.fetchall())[0]
        wtArray.append(cW)
    print(wtArray, "WT ARRAY")
    if user == 1:
        return render_template(
            "trainerHome.html",
            email=email,
            users=users,
            wtArray=wtArray,
            lt=len(wtArray),
        )
    return render_template("trainerLoginSignup.html", status=-1)


@app.route("/dashboard")
def dashboard():
    email = request.args.get("email")
    return render_template("dashboard.html", email=email)


@app.route("/makenewplan")
def makenewplan():
    email = request.args.get("email")
    print(email)
    workouts = [
        "Running",
        "Cycling",
        "Trekking",
        "Skipping",
        "Bicep Curls",
        "Tricep Extensions",
        "Dips",
        "Front Raise",
        "Shoulder Press",
        "Dumbbell Shrugs",
        "Pull-ups",
        "Deadlift",
        "Lat Pull Down",
        "Push-ups",
        "Inclined Dumbbell Flies",
    ]
    return render_template("makeNewPlan.html", email=email, workouts=workouts)


@app.route("/savenewplan")
def savenewplan():
    workouts = [
        "Running",
        "Cycling",
        "Trekking",
        "Skipping",
        "Bicep Curls",
        "Tricep Extensions",
        "Dips",
        "Front Raise",
        "Shoulder Press",
        "Dumbbell Shrugs",
        "Pull-ups",
        "Deadlift",
        "Lat Pull Down",
        "Push-ups",
        "Inclined Dumbbell Flies",
    ]
    email = request.args.get("email")
    print(email, "THIS")
    cur = mysql.connection.cursor()
    exe = cur.execute("select * from `trainer` where `Email` = '" + email + "'")
    user = list(cur.fetchall())[0]
    planID = str(random.randint(100, 999))
    planName = user["Name"] + "s Plan"
    exe = cur.execute(
        "insert into `exercise plans` (`PlanID`,`Plan Name`,`Creator`) values('"
        + planID
        + "','"
        + planName
        + "','"
        + user["Name"]
        + "')"
    )
    mysql.connection.commit()
    return render_template("makeNewPlan.html", email=email, workouts=workouts)


@app.route("/getWorkoutPlan")
def get_workout_plan():
    email = request.args.get("email")
    return render_template("workoutplan.html", email=email)


@app.route("/getDailyWorkout")
def get_daily_workout():
    email = request.args.get("email")
    workouts = [
        "Running",
        "Cycling",
        "Trekking",
        "Skipping",
        "Bicep Curls",
        "Tricep Extensions",
        "Dips",
        "Front Raise",
        "Shoulder Press",
        "Dumbbell Shrugs",
        "Pull-ups",
        "Deadlift",
        "Lat Pull Down",
        "Push-ups",
        "Inclined Dumbbell Flies",
    ]
    exercises = []
    sets = []
    reps = []
    cur = mysql.connection.cursor()
    exe = cur.execute("select * from `users` where `Email` = '" + email + "'")
    user = list(cur.fetchall())
    user = user[0]
    exe = cur.execute("select * from `goals` where `Email` = '" + email + "'")
    goalData = list(cur.fetchall())
    goalData = goalData[0]
    intensity = goalData["Intensity"]
    if intensity == "Beginner":
        total = 4
        setLength = 3
        repLength = 10
    elif intensity == "Intermediate":
        total = 7
        setLength = 3
        repLength = 13
    else:
        total = 10
        setLength = 5
        repLength = 15
    for i in range(0, total):
        rand = random.randrange(0, 14)
        if rand == 0 or rand == 1 or rand == 2:
            sets.append(0)
            reps.append(0)
        else:
            sets.append(setLength)
            reps.append(repLength)
        exercises.append(workouts[rand])
    return render_template(
        "showExercise.html",
        email=email,
        exercises=exercises,
        sets=sets,
        reps=reps,
        length=len(exercises),
        intensity=intensity,
    )


@app.route("/random")
def random1():
    return render_template("showExercise.html")


@app.route("/getProgress")
def get_progress():
    email = request.args.get("email")
    cur = mysql.connection.cursor()
    exe = cur.execute("select * from `weightLog` where `Email` = '" + email + "'")
    user = list(cur.fetchall())
    dates = []
    weights = []
    length = 0
    for one in user:
        dates.append(one["Timestamp"])
        weights.append(one["Weight"])
        length = length + 1
    return render_template(
        "progress.html", email=email, dates=dates, weights=weights, length=length
    )


@app.route("/getSetGoals")
def get_set_goals():
    cur = mysql.connection.cursor()
    exe = cur.execute("select * from `exercise plans`")
    plans = list(cur.fetchall())
    email = request.args.get("email")

    return render_template("setGoals.html", email=email, plans=plans)


@app.route("/setGoals", methods=["GET", "POST"])
def set_goals():
    email = request.args.get("email")
    currentWeight = request.form.get("currentWeight")
    targetWeight = request.form.get("targetWeight")
    intensity = request.form.get("intensity")
    cur = mysql.connection.cursor()

    exe = cur.execute(
        "UPDATE `goals` SET `Current Weight` = %s, `Target Weight` = %s, `Intensity` = %s WHERE `Email` = %s",
        (currentWeight, targetWeight, intensity, email),
    )
    mysql.connection.commit()
    dt = str(datetime.datetime.now(tz=pytz.UTC))  # Stores the current time in UTC
    timestamp = dt[0:10]
    exe = cur.execute(
        "insert into `weightLog` (`Email`,`Timestamp`,`Weight`) values('"
        + email
        + "','"
        + timestamp
        + "','"
        + currentWeight
        + "')"
    )
    mysql.connection.commit()
    return render_template("dashboard.html", email=email)


@app.route("/getLogWeight")
def get_log_weight():
    email = request.args.get("email")
    return render_template("logWeight.html", email=email)


@app.route("/logWeight", methods=["POST", "GET"])
def log_weight():
    dt = str(datetime.datetime.now(tz=pytz.UTC))  # Stores the current time in UTC
    timestamp = dt[0:10]
    email = request.args.get("email")
    loggedWeight = request.form.get("loggedWeight")
    cur = mysql.connection.cursor()
    exe = cur.execute(
        "insert into `weightLog` (`Email`,`Timestamp`,`Weight`) values('"
        + email
        + "','"
        + timestamp
        + "','"
        + loggedWeight
        + "')"
    )
    mysql.connection.commit()
    return render_template("dashboard.html", email=email)


@app.route("/customerProgress", methods=["POST", "GET"])
def customerProgress():
    yo = request.form["user"]
    print(yo, "TEST")
    return render_template("customerProgress.html")


def convert_to_dict(test_list):
    res = defaultdict(list)
    {res[key].append(sub[key]) for sub in test_list for key in sub}

    # printing result
    # print("The extracted dictionary : " + str(dict(res)))
    result = dict(res)
    return result


if __name__ == "__main__":
    app.run(debug=True)
