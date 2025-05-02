from flask import render_template, redirect, url_for
from flask import Blueprint
from database.config import get_db

users, urls = get_db()
redirect_bp = Blueprint('redirect', __name__)


@redirect_bp.route('/<short_code>')
def redirect_short_url(short_code):
    return redirect(url_for('redirect.redirect_page', short_code=short_code))


@redirect_bp.route('/r/<short_code>')
def redirect_page(short_code):

    link = urls.find_one({"short_code": short_code})
    if link:

        return render_template('redirect.html', original_url=link['original_url'])
    return render_template('error.html'), 404


@redirect_bp.route('/go/<short_code>')
def go_to_original(short_code):
    link = urls.find_one({"short_code": short_code})
    if link:
        return redirect(link['original_url'])
    return render_template('error.html'), 404