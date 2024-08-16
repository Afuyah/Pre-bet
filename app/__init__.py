from flask import Flask
from .extensions import db, migrate, login_manager, bcrypt, celery
from .auth.routes import auth as auth_blueprint
from .main.routes import main as main_blueprint
from .scraper.scraper import scraper as scraper_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    celery.conf.update(app.config)

    # Register blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(scraper_blueprint)

    return app