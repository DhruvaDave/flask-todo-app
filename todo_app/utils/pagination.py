import logging
from sqlalchemy import func
from todo_app.common import constants
from todo_app.exceptions.http_exception import HttpException

logger = logging.getLogger(__name__)


def get_pagination(query_params):
    """
    Returning parameters required for SQLAlchemy pagination
    args: 
        - query_params: dictionary with pagination request params
    return: offset, limit
    """
    page_no = query_params.get('page_no', constants.DEFAULT_PAGE_NO)
    page_size = query_params.get('page_size', constants.DEFAULT_PAGE_SIZE)

    try:
        page_no = int(page_no)
        page_size = int(page_size)
        if page_no <= 0 or page_size <= 0:
            raise ValueError
    except ValueError as e:
        error_message = f"Invalid page number or page size"
        logger.debug(error_message)
        raise HttpException(error_message, constants.BAD_REQUEST, 400)
  
    offset = (page_no - 1) * page_size
    limit = page_size
   
    return offset, limit
