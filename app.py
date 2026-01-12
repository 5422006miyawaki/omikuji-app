from flask import Flask, render_template
import random
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        dbname="omikuji",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/draw")
def draw():
    results = ["大吉", "吉", "中吉", "小吉", "凶", "大凶"]
    result = random.choice(results)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO fortune_history (result) VALUES (%s)",
        (result,)
    )
    conn.commit()
    cur.close()
    conn.close()

    return render_template("index.html", result=result)

@app.route("/history")
def history():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            result,
            to_char(
                created_at AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Tokyo',
                'YYYY/MM/DD HH24:MI:SS'
            )
        FROM fortune_history ORDER BY created_at DESC
    """)
    histories = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("history.html", histories=histories)

if __name__ == "__main__":
    app.run(debug=True)
