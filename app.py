from flask import Flask, redirect, url_for, render_template, session, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__, template_folder='templates', static_folder='templates/css')

app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    hash_passwd: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

    def to_dict(self, username):
        return {
            "name": self.username
        }

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def homepage():
    user = session.get('user')
    print(user)
    return render_template('homepage.html', user=user)

@app.route('/signup', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if not fullname or not username or not password or not email:
            return render_template('add.html', error="All the fields must be done.")
        
        if User.query.filter_by(username=request.form['username']).first():
            return render_template('sign.html', error="User already taken.")
        hash_passwd = generate_password_hash(request.form['password'])
        new_user = User(fullname=fullname, username=username, hash_passwd=hash_passwd, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('homepage'))
        
    return render_template('sign.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Auth
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.hash_passwd, password):
            session['user'] = user.to_dict(username)
            return redirect(url_for('homepage'))
        else:
            return "User not found.", 404
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('user', '')
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run()
