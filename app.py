from flask import Flask, render_template, request, session, redirect, url_for
import random
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Add if you use password
    database="guessing_game"
)
cursor = db.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    if "secret_number" not in session:
        session["secret_number"] = random.randint(1, 100)
        session["attempts"] = 0

    message = ""
    if request.method == "POST" and "guess" in request.form:
        guess = request.form["guess"]
        if not guess.isdigit():
            message = "Please enter a valid number!"
        else:
            guess = int(guess)
            session["attempts"] += 1

            if guess < session["secret_number"]:
                message = "Too low! Try again."
            elif guess > session["secret_number"]:
                message = "Too high! Try again."
            else:
                player_name = session.get("player_name", "Unknown")
                cursor.execute("INSERT INTO leaderboard (name, attempts) VALUES (%s, %s)",
                               (player_name, session["attempts"]))
                db.commit()

                message = f"🎉 Congratulations {player_name}! You guessed it in {session['attempts']} attempts."
                session.pop("secret_number")
                session.pop("attempts")

    cursor.execute("SELECT name, attempts FROM leaderboard ORDER BY attempts ASC LIMIT 10")
    leaderboard = cursor.fetchall()

    return render_template("index.html", message=message,
                           attempts=session.get("attempts", 0),
                           leaderboard=leaderboard)

@app.route("/set_name", methods=["POST"])
def set_name():
    session["player_name"] = request.form["player_name"]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
