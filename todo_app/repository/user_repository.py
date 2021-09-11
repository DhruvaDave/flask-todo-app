import logging

from todo_app.config.db_handler import handler
from todo_app.models.user_management import TblUsers

logger = logging.getLogger(__name__)

db_session = handler.db_session


class UserRepo:

    @staticmethod
    def create_users(users_data):
        """
        Create user
        """
        user = TblUsers(**users_data)
        db_session.add(user)
        db_session.flush()
        db_session.commit()
        return user.user_id

    @staticmethod
    def fetch_user_by_email(email):
        """
            Fetch user by email
        """
        user_data = (
            TblUsers.query\
                .filter(TblUsers.email == email)
                .first()
        )
        return user_data

   