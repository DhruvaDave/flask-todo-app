import logging
from datetime import datetime, timedelta

import jwt
from todo_app.config.app_config import CommonConfig
from todo_app.common.constants import JWT_ENCRYPTION_ALGO


logger = logging.getLogger(__name__)


def generate_jwt_token(email, exp_time, **kwargs):
    """
    generate JWT token as temporary token
    """
    token = jwt.encode(
        {"email": email, "exp": datetime.utcnow() + timedelta(minutes=exp_time), **kwargs},
        CommonConfig.app_secret_key,
    )
    return token

def decode_jwt_token(token):
    decoded = jwt.decode(token, CommonConfig.app_secret_key, algorithms=[JWT_ENCRYPTION_ALGO])
    return decoded