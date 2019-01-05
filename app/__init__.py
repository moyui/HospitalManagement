from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from .config import config
from flask import redirect, request, url_for


bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    @app.before_request
    def before_request():
        path = request.path
        doctorinfoid = request.cookies.get('doctorid')
        print(path)
        if doctorinfoid is None:
            if path == '/login' or path == '/':
                return
            else:
                return redirect('/login')
        return

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prfix="/")
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prfix="/auth")
    from .charges import charges as charges_blueprint
    app.register_blueprint(charges_blueprint, url_prfix="/charges")
    from .inpatient import inpatient as inpatient_blueprint
    app.register_blueprint(inpatient_blueprint, url_prfix="/inpatient")
    from .outpatient import outpatient as outpatient_blueprint
    app.register_blueprint(outpatient_blueprint, url_prfix="/outpatient")

    return app
