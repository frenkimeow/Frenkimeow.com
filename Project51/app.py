from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key_for_newbie'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {
    "admin": {
        "id": "1",
        "username": "admin",
        "full_name": "Карапетов О.О.",  
        "password": generate_password_hash("admin123")
    },
    "user": {
        "id": "2",
        "username": "user",
        "full_name": "Обычный пользователь",
        "password": generate_password_hash("user123")
    }
}

class User(UserMixin):
    def __init__(self, user_id, username, full_name):
        self.id = user_id
        self.username = username
        self.full_name = full_name  

@login_manager.user_loader
def load_user(user_id):
    for data in users.values():
        if data["id"] == user_id:
            return User(data["id"], data["username"], data["full_name"])
    return None

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember_me') else False

        user_data = users.get(username)

        if user_data and check_password_hash(user_data['password'], password):
            # Передаём полное имя в объект пользователя
            user = User(user_data['id'], user_data['username'], user_data['full_name'])
            login_user(user, remember=remember)
            return redirect(url_for('home'))
        
        flash('Неверный логин или пароль')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)