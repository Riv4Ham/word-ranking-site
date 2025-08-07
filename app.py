from flask import Flask, render_template, request, redirect, url_for
import random
import sqlite3 



app = Flask(__name__)


def initialize_database():
    conn = sqlite3.connect("data/words.db")
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS words (
            word TEXT PRIMARY KEY,
            score INTEGER DEFAULT 0
        )
    ''')
    # Insert words if they don't exist
    for word in word_list:
        c.execute("INSERT OR IGNORE INTO words (word) VALUES (?)", (word,))
    conn.commit()
    conn.close()

#loads word list
with open('data/dictionary.txt', 'r') as file:
    word_list = [line.strip() for line in file if line.strip()]  # remove blank lines
    initialize_database()




@app.route("/")
def index():
    word1, word2 = random.sample(word_list, 2)

    # Get top 10 words by score
    conn = sqlite3.connect("data/words.db")
    c = conn.cursor()
    c.execute("SELECT word, score FROM words ORDER BY score DESC LIMIT 10")
    leaderboard = c.fetchall()
    conn.close()

    return render_template("index.html", word1=word1, word2=word2, leaderboard=leaderboard)


@app.route("/vote", methods=["POST"])
def vote():
    votedword = request.form["vote"]
    print("user voted for:", votedword)
    conn = sqlite3.connect("data/words.db")
    c = conn.cursor()
    c.execute("UPDATE words SET score = score + 1 WHERE word = ?", (votedword,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)