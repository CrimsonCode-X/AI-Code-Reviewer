import os
import re
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ── Config ──────────────────────────────────────────────────────────────────
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me-in-production-please')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ── Extensions ───────────────────────────────────────────────────────────────
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message = 'Please sign in to access the code reviewer.'
login_manager.login_message_category = 'error'

# ── User Model ────────────────────────────────────────────────────────────────
class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables on first run
with app.app_context():
    db.create_all()

# ── Gemini Client ─────────────────────────────────────────────────────────────
try:
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
except Exception as e:
    print(f"Failed to initialize Gemini Client: {e}")
    client = None

# ── Auth Routes ───────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    email    = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    # Validation
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        flash('Username must be 3–20 characters (letters, numbers, underscores).', 'error')
        return redirect(url_for('login_page') + '?tab=register')

    if len(password) < 6:
        flash('Password must be at least 6 characters.', 'error')
        return redirect(url_for('login_page') + '?tab=register')

    if User.query.filter_by(username=username).first():
        flash('That username is already taken.', 'error')
        return redirect(url_for('login_page') + '?tab=register')

    if User.query.filter_by(email=email).first():
        flash('An account with that email already exists.', 'error')
        return redirect(url_for('login_page') + '?tab=register')

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    flash(f'Account created! Welcome, {username}. Please sign in.', 'success')
    return redirect(url_for('login_page'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out.', 'success')
    return redirect(url_for('login_page'))


# ── App Routes ────────────────────────────────────────────────────────────────
@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
@login_required
def analyze_code():
    if not client:
        return jsonify({"error": "Gemini API key not configured. Please set GEMINI_API_KEY."}), 500

    data     = request.json
    code     = data.get('code', '')
    language = data.get('language', 'javascript')

    if not code:
        return jsonify({"error": "No code provided"}), 400

    prompt = f"""
You are an expert AI Code Reviewer. Analyze the following {language} code.
Provide your response strictly in the following JSON format:
{{
  "bugs": "Markdown formatted explanation of any logical errors, security vulnerabilities, or syntax errors.",
  "optimizations": "Markdown formatted explanation of performance inefficiencies, memory leaks, or algorithmic improvements.",
  "quality": "Markdown formatted explanation of code readability, best practices, maintainability, and style enhancements."
}}

If there are no issues in a category, mention that the code looks good in that regard.

Code to analyze:
```{language}
{code}
```
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        response_text = response.text

        # Strip potential markdown block syntax
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        result = json.loads(response_text.strip())
        return jsonify(result)

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from AI response: {e}")
        print("Raw response:", response.text)
        return jsonify({"error": "AI response was not in expected JSON format."}), 500
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
