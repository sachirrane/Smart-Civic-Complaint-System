from flask import Flask, render_template, request ,redirect,session
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "smartcivic123"

def create_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        email TEXT,
        mobile TEXT,
        department TEXT,
        ward TEXT,
        priority TEXT,
        complaint TEXT,
        status TEXT DEFAULT 'Pending',
        created_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ratings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id INTEGER,
        rating INTEGER,
        comments TEXT
    )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():

    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/user_register")
def user_register():
    return render_template("user_register.html")

@app.route("/user_login")
def user_login():
    return render_template("user_login.html")

@app.route("/register")
def register():
    return render_template("complaint.html")

@app.route("/submit", methods=["POST"])
def submit():
    user_id = session["user_id"]
    name = request.form["name"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    department = request.form["department"]
    ward = request.form["ward"]
    priority = request.form["priority"]
    complaint = request.form["complaint"]
    created_at = datetime.now().strftime("%d-%m-%Y %H:%M")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()



    cursor.execute("""
INSERT INTO complaints
(user_id,name,email,mobile,department,ward,priority,complaint,status,created_at)
VALUES (?,?,?,?,?,?,?,?,?,?)
""",
(user_id,name,email,mobile,department,ward,priority,complaint,"Pending",created_at))

    complaint_id = cursor.lastrowid
    conn.commit()
    conn.close()

    
    return render_template(
    "success.html",
    complaint_id=complaint_id,
    name=name,
    department=department,
    priority=priority,
    status="Pending",
    created_at=created_at
)

@app.route("/dashboard")
def dashboard():

    if session.get("admin") != True:
        return redirect("/admin_login")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT complaints.*,
       ratings.rating,
       ratings.comments
   FROM complaints
   LEFT JOIN ratings
   ON complaints.id = ratings.complaint_id
   """)

    complaints = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Pending'")
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE priority='High'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE priority='Medium'")
    medium = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE priority='Low'")
    low = cursor.fetchone()[0]

    today = datetime.now().strftime("%d-%m-%Y")

    cursor.execute(
    "SELECT COUNT(*) FROM complaints WHERE created_at LIKE ?",
    (today + "%",)
)
    today_count = cursor.fetchone()[0]

    cursor.execute("""
     SELECT department, COUNT(*) as total
     FROM complaints
     GROUP BY department
    """)

    department_report = cursor.fetchall()

    cursor.execute("""
    SELECT ward, COUNT(*) as total
    FROM complaints
    GROUP BY ward
    """)

    ward_report = cursor.fetchall()


    cursor.execute("""
   SELECT ward, COUNT(*) as total
   FROM complaints
   GROUP BY ward
   ORDER BY total DESC
   LIMIT 5
   """)

    top_wards = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        complaints=complaints,
        total=total,
        pending=pending,
        high=high,
        medium=medium,
        low=low,
        department_report=department_report,
        ward_report=  ward_report,
        today_count=today_count,
        top_wards=top_wards

    )


@app.route("/search")
def search():

    keyword = request.args.get("keyword")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT * FROM complaints
    WHERE name LIKE ?
    OR department LIKE ?
    OR ward LIKE ?
    """,
    ('%'+keyword+'%',
     '%'+keyword+'%',
     '%'+keyword+'%'))

    complaints = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        complaints=complaints,
        total=len(complaints),
        pending=0,
        high=0
    )

@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM complaints WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")
@app.route("/resolve/<int:id>")
def resolve(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE complaints SET status='Resolved' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/edit/<int:id>")
def edit(id):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM complaints WHERE id=?",
        (id,)
    )

    complaint = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        complaint=complaint
    )

@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    name = request.form["name"]
    department = request.form["department"]
    ward = request.form["ward"]
    priority = request.form["priority"]
    complaint = request.form["complaint"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE complaints
    SET
    name=?,
    department=?,
    ward=?,
    priority=?,
    complaint=?
    WHERE id=?
    """,
    (
        name,
        department,
        ward,
        priority,
        complaint,
        id
    ))

    conn.commit()
    conn.close()

    if session.get("admin") == True:

      return redirect("/dashboard")

    else:
       return redirect("/my_complaints")

    
@app.route("/feedback/<int:id>")
def feedback(id):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM complaints WHERE id=?",
        (id,)
    )

    complaint = cursor.fetchone()

    conn.close()

    return render_template(
        "feedback.html",
        complaint=complaint
    )

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():

    complaint_id = request.form["complaint_id"]
    rating = request.form["rating"]
    comments = request.form["comments"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ratings
    (complaint_id,rating,comments)
    VALUES(?,?,?)
    """,
    (complaint_id,rating,comments))

    conn.commit()
    conn.close()

    return redirect("/my_complaints")

@app.route("/track")
def track():

    return render_template("track.html")

@app.route("/track_result")
def track_result():

    complaint_id = request.args.get("id")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM complaints WHERE id=?",
        (complaint_id,)
    )

    complaint = cursor.fetchone()

    conn.close()

    return render_template(
        "track_result.html",
        complaint=complaint
    )

@app.route("/save_user", methods=["POST"])
def save_user():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users
    (name,email,password)
    VALUES(?,?,?)
    """,
    (name,email,password))

    conn.commit()
    conn.close()

    return """
    <h2>Registration Successful!</h2>
    <a href='/'>Go Home</a>
    """


@app.route("/login_user", methods=["POST"])
def login_user():

    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE email=? AND password=?
    """,
    (email, password))

    user = cursor.fetchone()

    conn.close()

    if user:

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]

        return render_template(
            "customer_dashboard.html",
            user=user
        )

    else:

        return """
        <h2>Invalid Email or Password</h2>
        <a href='/user_login'>Try Again</a>
        """
@app.route("/my_complaints")
def my_complaints():

    user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM complaints WHERE user_id=?",
        (user_id,)
    )

    complaints = cursor.fetchall()

    conn.close()

    return render_template(
        "my_complaints.html",
        complaints=complaints
    )

@app.route("/admin_login")
def admin_login():

    return render_template("admin_login.html")


@app.route("/admin_check", methods=["POST"])
def admin_check():

    email = request.form["email"]
    password = request.form["password"]

    if email == "admin@gmail.com" and password == "admin123":

        session["admin"] = True

        return redirect("/dashboard")
    

    else:

        return """
        <h2>Invalid Admin Login</h2>
        <a href='/admin_login'>Try Again</a>
        """
    

    if __name__ == "__main__":
     create_table()
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )

