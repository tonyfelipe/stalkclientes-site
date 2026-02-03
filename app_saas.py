from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'segredo_do_stalker'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logado' not in session: return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['email'] == 'teste@stalk.com' and request.form['senha'] == '123456':
            session['logado'] = True
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/')
@login_required
def dashboard():
    conn = sqlite3.connect('meu_saas_leads.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY id DESC')
    leads = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', leads=leads)

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
