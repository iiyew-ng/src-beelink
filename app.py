from flask import Flask, send_from_directory
from routes.auth import auth_bp
from routes.url import url_bp
from utils.utils import redirect_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


app.register_blueprint(auth_bp)
app.register_blueprint(url_bp)
app.register_blueprint(redirect_bp)


@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.root_path + '/templates', 'sitemap.xml')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)