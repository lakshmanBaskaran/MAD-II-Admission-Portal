from flask import Flask, redirect
from config import Config
from extensions import db, login_manager
from models import User
from werkzeug.security import generate_password_hash

# IMPORT ROUTES
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.company import company_bp
from routes.student import student_bp
from services.cache import cache

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    # REGISTER BLUEPRINTS
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

        # Create admin if not exists
        if not User.query.filter_by(role="admin").first():
            admin = User(
                name="Admin",
                email="admin@portal.com",
                password_hash=generate_password_hash("admin123"),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin created: admin@portal.com / admin123")

    return app


app = create_app()


@app.route("/")
def home():
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)