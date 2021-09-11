"""
    Config related to swagger
"""
from flask_swagger_ui import get_swaggerui_blueprint

# Swagger Configuration


class SwaggerConfig:
    """
    Swagger config
    """

    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.yaml"
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Todo-API-Swagger-UI"}
    )
