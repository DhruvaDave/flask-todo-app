import enum

# third party imports
from sqlalchemy import (
    Column,
    text,
)


from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import func


class DatetimeMixin(object):
    """
    common mixin class for datetime
    """

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )


class StatusType(enum.Enum):
    """
    Select type of status for Todo items
    """

    todo = "ToDo"
    inprogress = "In Progress"
    done = "Done"