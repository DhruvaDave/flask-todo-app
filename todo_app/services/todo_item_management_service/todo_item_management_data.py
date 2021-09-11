from datetime import date
import json
import logging
from sqlalchemy import exc
from flask import session, jsonify
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.sqltypes import Time

from todo_app.common import constants
from todo_app.exceptions.http_exception import HttpException
from todo_app.utils.http_response_handler import HttpResponseHandler


from todo_app.repository.todo_item_repository import TodoItemRepo
from todo_app.utils.pagination import get_pagination

from todo_app.common import messages
from todo_app.utils.session_management import get_current_user_id

logger = logging.getLogger(__name__)


class TodoItemData:

    @staticmethod
    def todo_item_add(form):
        """
            Add todo item
        """
        if not form.validate_on_submit():
            logging.debug(messages.INVALID_FORM_MESSAGE, form.errors)
            raise HttpException(messages.INVALID_FORM_MESSAGE,
                                constants.BAD_REQUEST, 400)
      
        
        user_id = get_current_user_id()
       
        
        add_todo_list_id = False
        
        data = {
            "user_id_fk": user_id,
            "parent_todo_item_id_fk": form.parent_todo_item_id.data if form.parent_todo_item_id else None,
            "title": form.title.data,
            "description": form.description.data,
            "start_date": form.start_date.data if form.start_date else None,
            "due_date": form.due_date.data if form.due_date else None,
            "status": form.status.data,
            "assign_to": form.assign_to.data if form.assign_to else None,
            "comment": form.comment.data if form.comment.data else None
        }
        logging.info(f'Todo item data {data}')
        if form.user_todo_list_id.data:
            data.update({
                "user_todo_list_id_fk": form.user_todo_list_id.data,
            })
        else:
            add_todo_list_id = True
        logging.info(f'Add todo list id {add_todo_list_id}')

        TodoItemRepo.create_todo_item(data, add_todo_list_id)
        logger.info('Todo Item added successfully')
       

        return jsonify(
            {
                "code": constants.CREATED,
                "message": "Todo Item Added Successfully"
            }
        ), constants.ENTITY_CREATED

    
    @staticmethod
    def assign_todo_item(form):
        """
            Assign todo item follower
        """
        if not form.validate_on_submit():
            logging.debug(messages.INVALID_FORM_MESSAGE, form.errors)
            raise HttpException(messages.INVALID_FORM_MESSAGE,
                                constants.BAD_REQUEST, 400)

        try:
            todo_item = TodoItemRepo.fetch_assigned_todo_item(form.todo_item_id.data, form.assign_to.data)
            if todo_item:
                logging.debug(f"Assignee already exists for item {form.todo_item_id.data}")
                return HttpResponseHandler.exist()
                
            user_id = get_current_user_id()
          
            TodoItemRepo.assign_todo_item(form.todo_item_id.data, form.assign_to.data)

            return HttpResponseHandler.success(messages="Todo Item Added Successfully")
        except Exception as ex:
            logging.debug(f'Error while assigning item to users {ex}')
            raise HttpException(
                f"Server Error!", constants.DEFAULT_ERROR_CODE, constants.DEFAULT_HTTP_ERROR_CODE) from ex


    @staticmethod
    def get_assign_todo_item(query_params):
        """
            Get Assign todo item follower
        """
        
        user_id = get_current_user_id()
        logging.info(f'Fetching assigned todo item for user {user_id}')
        offset, limit = get_pagination(query_params)
        total, item_data = TodoItemRepo.fetch_user_todo_item(user_id,  offset, limit)
        if total == 0:
            logging.debug(f'No todo item found for user {user_id}')
            return jsonify({"code": constants.NO_ENTITY_FOUND,
                            "message": "No results found."})
        result = {}
        data = []
        for item in item_data:
            data.append({
                "title": item.title,
                "description": item.description,
                "start_date": item.start_date,
                "due_date": item.due_date,
                "status": item.status
            })
        result.update({
            "data": data,
            "page": query_params.get('page_no'),
            "page_size": query_params.get('page_size'),
            "total_records": total
        })
        return HttpResponseHandler.success(message="Todo Item Fetched Successfully", **result)
        
    @staticmethod
    def add_comment_todo_item(form):
        """
            Add comment todo item follower
        """
        if not form.validate_on_submit():
            logging.debug(messages.INVALID_FORM_MESSAGE, form.errors)
            raise HttpException(messages.INVALID_FORM_MESSAGE,
                                constants.BAD_REQUEST, 400)

        try:
            todo_item = TodoItemRepo.fetch_todo_item(form.todo_item_id.data)
            if not todo_item:
                return HttpResponseHandler.invalid_request_entity()
                
            creator_assignee = []
            for item in todo_item:
                creator_assignee.append(item.user_id_fk)
            
            todo_item_assignee = TodoItemRepo.fetch_assignee_todo_item(form.todo_item_id.data)
            for assignee in todo_item_assignee:
                creator_assignee.append(assignee.assigned_user_id_fk)


            logging.info(f'Creator assinee users {creator_assignee}')
            user_id = get_current_user_id()
            if user_id not in list(set(creator_assignee)):
                return HttpResponseHandler.bad_request(
                    message="Only creator or assignee allowed to add comments.")

            data = {
                "comment": form.comment.data
            }
            TodoItemRepo.post_comment_todo_item(form.todo_item_id.data, data)

            return HttpResponseHandler.success(messages="Comment Added Successfully")
        except Exception as ex:
            logging.debug(f'Error while assigning item to users {ex}')
            raise HttpException(
                f"Server Error!", constants.DEFAULT_ERROR_CODE, constants.DEFAULT_HTTP_ERROR_CODE) from ex
