"""
    DB Handler used across project
"""
import logging
from todo_app.utils.db_utils import MySQLHandler 
from todo_app.config.db_config import DBConfig

logger = logging.getLogger("DB-Handler")

db_passcode = DBConfig.password.replace("%", "%%")
handler = MySQLHandler(
    DBConfig.host,
    DBConfig.user,
    DBConfig.password,
    DBConfig.port,
    DBConfig.dbname,
    DBConfig.pool_size,
)


def register_models():
    """
    Model initialization
    """
    logger.info("Initializing MySQL handler ... ")
    handler.initialize_db()

    # pylint: disable=W0611,C0415
    # note: Ignoring 'Import outside toplevel' as related to system trace
    # DATABASE TABLES WILL BE CREATED ONLY FOR MODELS IMPORTED HERE
    from todo_app.models.user_management import TblUsers
    from todo_app.models.user_todo_list import TblUserTodoList
    from todo_app.models.todo_list import TblTodoLists
    from todo_app.models.todo_items import TblTodoItems, TblTodoItemUsers

    handler.Base.metadata.create_all(bind=handler.engine)
