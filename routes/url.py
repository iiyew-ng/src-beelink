from flask import render_template, request, redirect, session, url_for, flash
from flask import Blueprint
from database.config import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import string, random


url_bp = Blueprint('url', __name__)
users, urls = get_db()


def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if not urls.find_one({"short_code": code}):
            return code


@url_bp.route('/shorten', methods=['POST'])
def shorten():

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    original_url = request.form['url']
    user_data = users.find_one({"email": session['user']})
    code = generate_code()
    urls.insert_one({
        "original_url": original_url,
        "short_code": code,
        "user_id": user_data['_id']
    })
    short_url = request.url_root + code
    flash(f'URL rút gọn: {short_url}')

    return redirect(url_for('auth.index'))