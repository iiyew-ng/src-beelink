from flask import Flask, render_template, request, redirect, session, url_for, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import string, random
import os


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


client = MongoClient(os.getenv("MONGO_URI"))
db = client['shortener']
users = db['users']
urls = db['urls']


def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if not urls.find_one({"short_code": code}):
            return code

# Trang chủ
@app.route('/')
def index():
    # Nếu chưa đăng nhập, hiển thị trang giới thiệu
    if 'user' not in session:
        return render_template('index.html')
    # Nếu đã đăng nhập, hiển thị bảng điều khiển (dashboard)
    user_data = users.find_one({"email": session['user']})
    user_links = list(urls.find({"user_id": user_data['_id']}))
    print(user_links)  # In ra để debug (có thể xóa)
    return render_template('dashboard.html', email=session['user'], links=user_links)

# Đăng ký tài khoản
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        # Kiểm tra email đã tồn tại
        if users.find_one({"email": email}):
            flash('Email đã tồn tại')  # Gửi thông báo lỗi
        else:
            # Thêm người dùng mới vào database
            users.insert_one({"email": email, "password": password})
            flash('Đăng ký thành công, vui lòng đăng nhập.')
            return redirect(url_for('login'))
    return render_template('register.html')

# Đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            session['user'] = email  # Lưu thông tin đăng nhập
            return redirect(url_for('index'))
        else:
            flash('Email hoặc mật khẩu không đúng')
    return render_template('login.html')

# Đăng xuất
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# Rút gọn URL
@app.route('/shorten', methods=['POST'])
def shorten():
    if 'user' not in session:
        return redirect(url_for('login'))
    original_url = request.form['url']
    user_data = users.find_one({"email": session['user']})
    code = generate_code()
    urls.insert_one({
        "original_url": original_url,
        "short_code": code,
        "user_id": user_data['_id']
    })
    short_url = request.host_url + code
    flash(f'URL rút gọn: {short_url}')
    return redirect(url_for('index'))

# Chuyển hướng từ mã rút gọn
@app.route('/<short_code>')
def redirect_short_url(short_code):
    link = urls.find_one({"short_code": short_code})
    if link:
        return redirect(link['original_url'])
    return render_template('error.html'), 404

# Xử lý lỗi 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

# Khởi chạy ứng dụng
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)