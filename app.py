from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Step 1: Create the database table
def init_db():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Step 2: Display all articles
@app.route('/')
def index():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute("SELECT * FROM articles")
    articles = c.fetchall()
    conn.close()
    return render_template("index.html", articles=articles)

# Step 3: View a single article
@app.route('/article/<int:id>')
def article(id):
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute("SELECT * FROM articles WHERE id=?", (id,))
    article = c.fetchone()
    conn.close()
    return render_template("article.html", article=article)

# Step 4: Add a new article
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect('news.db')
        c = conn.cursor()
        c.execute("INSERT INTO articles (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template("add.html")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
