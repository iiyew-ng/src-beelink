from flask import render_template, request, redirect, session, url_for, flash
from flask import Blueprint
from database.config import get_db
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__)
users, urls = get_db()

@auth_bp.route('/')
def index():

    if 'user' not in session:
        return render_template('index.html')
    
    user_data = users.find_one({"email": session['user']})
    user_links = list(urls.find({"user_id": user_data['_id']}))

    return render_template('dashboard.html', email=session['user'], links=user_links)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        
        if users.find_one({"email": email}):
            flash('Email đã tồn tại')

        else:

            users.insert_one({"email": email, "password": password})
            flash('Đăng ký thành công, vui lòng đăng nhập.')
            return redirect(url_for('auth.login'))
        
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.find_one({"email": email})

        if user and check_password_hash(user['password'], password):
            session['user'] = email
            return redirect(url_for('auth.index'))
        else:
            flash('Email hoặc mật khẩu không đúng')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.index'))