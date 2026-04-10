# from flask import Flask, render_template, request, redirect, session, url_for
# import pandas as pd
# import os
# import re
# from werkzeug.security import generate_password_hash, check_password_hash
# from sklearn.preprocessing import LabelEncoder
# from sklearn.neighbors import NearestNeighbors

# # port = int(os.environ.get("PORT", 8080))
# # app.run(host="0.0.0.0", port=port)


# app = Flask(__name__)
# app.secret_key = "SECRET_KEY"

# # ================= DATABASE =================
# DATABASE_URL = os.environ.get("DATABASE_URL")

# def get_db():
#     if DATABASE_URL:
#         import psycopg2
#         return psycopg2.connect(DATABASE_URL)
#     else:
#         import sqlite3
#         return sqlite3.connect("users.db")

# def init_db():
#     conn = get_db()
#     cur = conn.cursor()

#     try:
#         cur.execute("""
#         CREATE TABLE IF NOT EXISTS users(
#             id SERIAL PRIMARY KEY,
#             username TEXT UNIQUE,
#             email TEXT UNIQUE,
#             password TEXT,
#             role TEXT DEFAULT 'user'
#         )
#         """)
#     except:
#         cur.execute("""
#         CREATE TABLE IF NOT EXISTS users(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE,
#             email TEXT UNIQUE,
#             password TEXT,
#             role TEXT DEFAULT 'user'
#         )
#         """)

#     conn.commit()
#     cur.close()
#     conn.close()

# init_db()

# # ================= DATA =================
# df = pd.read_csv(os.path.join(os.getcwd(), "Indian_Tourism_ML_Big_Dataset.csv"))

# encoders = {}
# for col in ["Weather", "Crowd_Level", "Tourism_Type", "Budget_Level"]:
#     le = LabelEncoder()
#     df[col] = le.fit_transform(df[col])
#     encoders[col] = le

# X = df[["Weather", "Crowd_Level", "Tourism_Type", "Budget_Level"]]
# model = NearestNeighbors(n_neighbors=5)
# model.fit(X)

# # ================= ROOT =================
# @app.route("/")
# def root():
#     return redirect(url_for("login"))

# # ================= LOGIN =================
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     error = None

#     if request.method == "POST":
#         u = request.form["username"]
#         p = request.form["password"]

#         conn = get_db()
#         cur = conn.cursor()

#         if DATABASE_URL:
#             cur.execute("SELECT * FROM users WHERE username=%s", (u,))
#         else:
#             cur.execute("SELECT * FROM users WHERE username=?", (u,))

#         user = cur.fetchone()
#         cur.close()
#         conn.close()

#         if user and check_password_hash(user[3], p):
#             session.clear()
#             session["user"] = u
#             session["role"] = user[4]
#             return redirect("/dashboard")
#         else:
#             error = "Invalid login credentials"

#     return render_template("login.html", error=error)

# # ================= DASHBOARD =================
# @app.route("/dashboard")
# def dashboard():
#     if "user" not in session:
#         return redirect(url_for("login"))
#     return render_template("index.html")

# # ================= LOGOUT =================
# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for("login"))

# # ================= SIGNUP =================
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     return render_template("signup.html")


# # ================= ADMIN =================
# @app.route("/admin")
# def admin():
#     if session.get("role") != "admin":
#         return "Access Denied"

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("SELECT id, username, email, role FROM users")
#     users = cur.fetchall()

#     cur.close()
#     conn.close()

#     return render_template("admin.html", users=users)

# # ================= CHATBOT =================
# @app.route("/chatbot", methods=["GET", "POST"])
# def chatbot():
#     reply = ""
#     if request.method == "POST":
#         msg = request.form["msg"].lower()

#         if "beach" in msg:
#             reply = "Goa, Varkala, Baga Beach are great beach destinations."
#         elif "hill" in msg:
#             reply = "Manali, Ooty, Munnar are famous hill stations."
#         elif "religious" in msg:
#             reply = "Varanasi, Tirupati, Amritsar, Mahakaleshwar are famous religious places."
#         else:
#             reply = "Ask about beach, hill or religious tourism."

#     return render_template("chatbot.html", reply=reply)

# # ================= RECOMMENDATION =================
# @app.route("/recommend", methods=["GET", "POST"])
# def recommend():
#     if request.method == "POST":
#         weather = encoders["Weather"].transform([request.form["weather"]])[0]
#         crowd = encoders["Crowd_Level"].transform([request.form["crowd"]])[0]
#         tourism = encoders["Tourism_Type"].transform([request.form["tourism"]])[0]
#         budget = encoders["Budget_Level"].transform([request.form["budget"]])[0]

#         distances, indices = model.kneighbors(
#             [[weather, crowd, tourism, budget]]
#         )

#         results = df.iloc[indices[0]][
#             ["State", "Place_Name", "Best_Time_To_Visit", "Famous_For"]
#         ]

#         return render_template(
#             "result.html",
#             places=results.to_dict(orient="records")
#         )

#     return render_template("recommend.html")

# # ================= RUN =================
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)


# from flask import Flask, render_template, request, redirect, session, url_for
# import pandas as pd
# import os
# from werkzeug.security import generate_password_hash, check_password_hash
# from sklearn.preprocessing import LabelEncoder
# from sklearn.neighbors import NearestNeighbors

# app = Flask(__name__)
# app.secret_key = "SECRET_KEY"

# # ================= DATABASE =================
# DATABASE_URL = os.environ.get("DATABASE_URL")

# # Fix Railway postgres:// issue
# if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
#     DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# def get_db():
#     import psycopg2
#     return psycopg2.connect(DATABASE_URL)

# def init_db():
#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS users(
#         id SERIAL PRIMARY KEY,
#         username TEXT UNIQUE,
#         email TEXT UNIQUE,
#         password TEXT,
#         role TEXT DEFAULT 'user'
#     )
#     """)

#     conn.commit()
#     cur.close()
#     conn.close()

# init_db()

# # ================= DATA =================
# df = pd.read_csv(os.path.join(os.getcwd(), "Indian_Tourism_ML_Big_Dataset.csv"))

# encoders = {}
# for col in ["Weather", "Crowd_Level", "Tourism_Type", "Budget_Level"]:
#     le = LabelEncoder()
#     df[col] = le.fit_transform(df[col])
#     encoders[col] = le

# X = df[["Weather", "Crowd_Level", "Tourism_Type", "Budget_Level"]]
# model = NearestNeighbors(n_neighbors=5)
# model.fit(X)

# # ================= ROOT =================
# @app.route("/")
# def root():
#     return redirect(url_for("login"))

# # ================= SIGNUP =================
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     error = None

#     if request.method == "POST":
#         username = request.form["username"]
#         email = request.form["email"]
#         password = request.form["password"]

#         hashed_password = generate_password_hash(password)

#         conn = get_db()
#         cur = conn.cursor()

#         try:
#             cur.execute(
#                 "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
#                 (username, email, hashed_password),
#             )
#             conn.commit()

#             print("✅ USER INSERTED:", username)

#             return redirect(url_for("login"))

#         except Exception as e:
#             print("❌ SIGNUP ERROR:", e)
#             error = "User already exists or DB error"

#         cur.close()
#         conn.close()

#     return render_template("signup.html", error=error)

# # ================= LOGIN =================
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     error = None

#     if request.method == "POST":
#         u = request.form["username"]
#         p = request.form["password"]

#         conn = get_db()
#         cur = conn.cursor()

#         cur.execute(
#             "SELECT * FROM users WHERE username=%s OR email=%s",
#             (u, u)
#         )

#         user = cur.fetchone()

#         print("🔍 LOGIN USER:", user)

#         cur.close()
#         conn.close()

#         if user and check_password_hash(user[3], p):
#             session.clear()
#             session["user"] = user[1]
#             session["role"] = user[4]

#             return redirect("/dashboard")
#         else:
#             error = "Invalid login credentials"

#     return render_template("login.html", error=error)

# # ================= DASHBOARD =================
# @app.route("/dashboard")
# def dashboard():
#     if "user" not in session:
#         return redirect(url_for("login"))
#     return render_template("index.html")

# # ================= LOGOUT =================
# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for("login"))

# # ================= ADMIN =================
# @app.route("/admin")
# def admin():
#     if session.get("role") != "admin":
#         return "Access Denied"

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("SELECT id, username, email, role FROM users")
#     users = cur.fetchall()

#     cur.close()
#     conn.close()

#     return render_template("admin.html", users=users)

# # ================= CHATBOT =================
# @app.route("/chatbot", methods=["GET", "POST"])
# def chatbot():
#     reply = ""
#     if request.method == "POST":
#         msg = request.form["msg"].lower()

#         if "beach" in msg:
#             reply = "Goa, Varkala, Baga Beach are great beach destinations."
#         elif "hill" in msg:
#             reply = "Manali, Ooty, Munnar are famous hill stations."
#         elif "religious" in msg:
#             reply = "Varanasi, Tirupati, Amritsar, Mahakaleshwar are famous religious places."
#         else:
#             reply = "Ask about beach, hill or religious tourism."

#     return render_template("chatbot.html", reply=reply)

# # ================= RECOMMENDATION =================
# @app.route("/recommend", methods=["GET", "POST"])
# def recommend():
#     if request.method == "POST":
#         weather = encoders["Weather"].transform([request.form["weather"]])[0]
#         crowd = encoders["Crowd_Level"].transform([request.form["crowd"]])[0]
#         tourism = encoders["Tourism_Type"].transform([request.form["tourism"]])[0]
#         budget = encoders["Budget_Level"].transform([request.form["budget"]])[0]

#         distances, indices = model.kneighbors(
#             [[weather, crowd, tourism, budget]]
#         )

#         results = df.iloc[indices[0]][
#             ["State", "Place_Name", "Best_Time_To_Visit", "Famous_For"]
#         ]

#         return render_template(
#             "result.html",
#             places=results.to_dict(orient="records")
#         )

#     return render_template("recommend.html")

# # ================= RUN =================
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port, debug=True)


from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd
import os
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

# ================= DATABASE =================
DATABASE_URL = os.environ.get("DATABASE_URL")

print("🚀 DATABASE_URL:", DATABASE_URL)

# Fix Railway postgres:// issue
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def get_db():
    import psycopg2
    return psycopg2.connect(DATABASE_URL, sslmode='require')  # ✅ SSL FIX

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user'
    )
    """)

    conn.commit()
    cur.close()
    conn.close()

# ================= FORCE TABLE CREATE =================
@app.route("/create-table")
def create_table():
    init_db()
    return "✅ Table Created Successfully"

# ================= DATA =================
df = pd.read_csv(os.path.join(os.getcwd(), "Indian_Tourism_ML_Big_Dataset.csv"))

encoders = {}
for col in ["Weather", "Crowd_Level", "Tourism_Type", "Budget_Level"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

X = df[["Weather", "Crowd_Level", "Tourism_Type", "Budget_Level"]]
model = NearestNeighbors(n_neighbors=5)
model.fit(X)

# ================= ROOT =================
@app.route("/")
def root():
    return redirect(url_for("login"))

# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db()
            cur = conn.cursor()

            print("🟡 Inserting user...")

            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password),
            )

            conn.commit()

            print("✅ USER INSERTED:", username)

            cur.close()
            conn.close()

            return redirect(url_for("login"))

        except Exception as e:
            print("❌ SIGNUP ERROR:", e)
            error = str(e)

    return render_template("signup.html", error=error)

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        try:
            conn = get_db()
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM users WHERE username=%s OR email=%s",
                (u, u)
            )

            user = cur.fetchone()

            print("🔍 LOGIN USER:", user)

            cur.close()
            conn.close()

            if user and check_password_hash(user[3], p):
                session.clear()
                session["user"] = user[1]
                session["role"] = user[4]

                return redirect("/dashboard")
            else:
                error = "Invalid login credentials"

        except Exception as e:
            print("❌ LOGIN ERROR:", e)
            error = "DB Error"

    return render_template("login.html", error=error)

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
