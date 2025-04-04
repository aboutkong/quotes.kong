from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Buat database jika belum ada
def init_db():
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS quotes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    author TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()
    c.execute('SELECT content, author FROM quotes ORDER BY id DESC')
    quotes = c.fetchall()
    conn.close()
    return render_template('index.html', quotes=quotes)

@app.route('/add', methods=['GET', 'POST'])
def add_quote():
    if request.method == 'POST':
        content = request.form['content']
        author = request.form.get('author', 'Anonymous')
        conn = sqlite3.connect('quotes.db')
        c = conn.cursor()
        c.execute('INSERT INTO quotes (content, author) VALUES (?, ?)', (content, author))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_quote.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
