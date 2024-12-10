from flask import Flask, redirect, url_for, render_template

app = Flask(__name__, template_folder='templates', static_folder='templates/css')

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/gooogle')
def google():
    return redirect("http://google.com")

if __name__ == '__main__':
    app.run()
