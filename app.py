from flask import Flask, redirect, url_for, render_template, session, request

app = Flask(__name__, template_folder='templates', static_folder='templates/css')
app.secret_key = "123456"

@app.route('/')
def homepage():
    username = ''
    if 'username' in session:
        username = session['username']
    return render_template('homepage.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['username'].strip() != '':
        session['username'] = request.form['username']
        return redirect(url_for('homepage'))
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('username', '')
    return redirect(url_for('homepage'))

@app.route('/gooogle')
def google():
    return redirect("http://google.com")

if __name__ == '__main__':
    app.run()
