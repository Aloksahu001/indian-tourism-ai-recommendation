# from flask import Flask, render_template, request
# import pandas as pd
# from sklearn.preprocessing import LabelEncoder
# from sklearn.neighbors import NearestNeighbors

# app = Flask(__name__)

# # Load dataset
# df = pd.read_csv("Indian_Tourism_ML_Big_Dataset.csv")

# # Encode categorical columns
# encoders = {}
# for col in ["Weather","Crowd_Level","Tourism_Type","Budget_Level"]:
#     le = LabelEncoder()
#     df[col] = le.fit_transform(df[col])
#     encoders[col] = le

# X = df[["Weather","Crowd_Level","Tourism_Type","Budget_Level"]]

# # ML Model
# model = NearestNeighbors(n_neighbors=5)
# model.fit(X)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/recommend", methods=["POST"])
# def recommend():
#     weather = encoders["Weather"].transform([request.form["weather"]])[0]
#     crowd = encoders["Crowd_Level"].transform([request.form["crowd"]])[0]
#     tourism = encoders["Tourism_Type"].transform([request.form["tourism"]])[0]
#     budget = encoders["Budget_Level"].transform([request.form["budget"]])[0]

#     distances, indices = model.kneighbors([[weather, crowd, tourism, budget]])

#     results = df.iloc[indices[0]][
#         ["State","Place_Name","Best_Time_To_Visit","Famous_For"]
#     ]

#     return render_template("result.html", tables=results.to_dict(orient="records"))

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd
import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)
app.secret_key = "tourism_secret_key"

# ================= DATABASE =================
def get_db():
    return sqlite3.connect("users.db", timeout=10, check_same_thread=False)

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user'
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ================= DATA + ML =================
df = pd.read_csv("Indian_Tourism_ML_Big_Dataset.csv")

encoders = {}
for col in ["Weather", "Crowd_Level", "Tourism_Type", "Budget_Level"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

X = df[["Weather", "Crowd_Level", "Tourism_Type", "Budget_Level"]]
model = NearestNeighbors(n_neighbors=5)
model.fit(X)

# ================= HOME =================
@app.route("/")
def index():
    return render_template("index.html")

# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    success = None

    if request.method == "POST":
        u = request.form["username"]
        e = request.form["email"]
        p = request.form["password"]

        if not re.match(r"[^@]+@[^@]+\.[^@]+", e):
            error = "Invalid email format"
        else:
            try:
                conn = get_db()
                c = conn.cursor()
                c.execute(
                    "INSERT INTO users(username,email,password) VALUES(?,?,?)",
                    (u, e, generate_password_hash(p))
                )
                conn.commit()
                conn.close()
                success = "Account created successfully! Please login."
            except sqlite3.IntegrityError:
                error = " Username or Email already exists"

    return render_template("signup.html", error=error, success=success)

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (u,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[3], p):
            session["user"] = u
            session["role"] = user[4]
            return redirect("/")
        else:
            error = " Invalid login credentials"

    return render_template("login.html", error=error)

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ================= ADMIN =================
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return "Access Denied "

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, username, email, role FROM users")
    users = c.fetchall()
    conn.close()

    return render_template("admin.html", users=users)

# ================= CHATBOT =================
@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    reply = ""
    if request.method == "POST":
        msg = request.form["msg"].lower()
        if "beach" in msg:
            reply = "Goa, Varkala, Baga Beach are great beach destinations."
        elif "hill" in msg:
            reply = "Manali, Ooty, Munnar are famous hill stations."
        elif "religious" in msg:
            reply = "Varanasi, Tirupati, Amritsar are famous religious places."
        else:
            reply = "Ask about beach, hill or religious tourism."

    return render_template("chatbot.html", reply=reply)

# ================= RECOMMENDATION =================
@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    if request.method == "POST":
        weather = encoders["Weather"].transform([request.form["weather"]])[0]
        crowd = encoders["Crowd_Level"].transform([request.form["crowd"]])[0]
        tourism = encoders["Tourism_Type"].transform([request.form["tourism"]])[0]
        budget = encoders["Budget_Level"].transform([request.form["budget"]])[0]

        distances, indices = model.kneighbors(
            [[weather, crowd, tourism, budget]]
        )

        results = df.iloc[indices[0]][
            ["State", "Place_Name", "Best_Time_To_Visit", "Famous_For"]
        ]

        return render_template(
            "result.html",
            places=results.to_dict(orient="records")
        )

    return render_template("recommend.html")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True, threaded=False)
