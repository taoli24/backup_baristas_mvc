from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from marshmallow.exceptions import ValidationError

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    # create the app instance
    app = Flask(__name__)
    app.config.from_object("config.app_config")

    # Initiate db instance and schema instance
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register error handler with app scope
    @app.errorhandler(ValidationError)
    def register_validation_error(error):
        response = jsonify(error.messages)
        response.status_code = 400
        return response

    # register blue print
    from commands import db_commands
    app.register_blueprint(db_commands)

    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app
