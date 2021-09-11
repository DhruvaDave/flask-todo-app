"""
    Config related to app
"""
from os import environ
import ast


class CommonConfig:
    """
    Flask application config
    """

    app_secret_key = environ.get("FLASK_APP_SECRET_KEY", "HVVCJSCDE64GIUSUB78CJSK")
    wtf_csrf = ast.literal_eval(environ.get("WTF_CSRF_ENABLED", "False"))
    app_port = environ.get("APP_PORT", "4500")
    debug = environ.get("APP_DEBUG", False)

    JWT_EXP_TIME_MINS = int(environ.get("JWT_EXP_TIME_MINS", 120))

