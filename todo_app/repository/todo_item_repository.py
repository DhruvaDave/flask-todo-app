import logging

from todo_app.config.db_handler import handler
from todo_app.models.todo_items import TblTodoItems, TblTodoItemUsers
from todo_app.models.todo_list import TblTodoLists
from todo_app.common.constants import MY_LIST

logger = logging.getLogger(__name__)

db_session = handler.db_session


class TodoItemRepo:

    @staticmethod
    def create_todo_item(todo_item_data, add_todo_list_id):
        """
        Create todo item
        """
        todo_user_item_data = []
        create_assign_record = False

        print("---------todo_item_data---------",todo_item_data)
        if 'assign_to' in todo_item_data:
            print("---------i--f-------")
            assign_to = todo_item_data.pop('assign_to')
            create_assign_record = True

        print("----------add_todo_list_id---------",add_todo_list_id)
        if add_todo_list_id:
            list_id = TblTodoLists.query\
                .filter(TblTodoLists.name == MY_LIST).first()
            print("-------list_id------",list_id)
            todo_item_data.update({
                "todo_list_id_fk": list_id.todo_list_id
            })

        todo_item = TblTodoItems(**todo_item_data)
        db_session.add(todo_item)
        db_session.flush()
        print("--------todo_item--------",todo_item,todo_item.todo_item_id)

        for assignee in assign_to:
            todo_user_item_data.append(TblTodoItemUsers(
                **{'assigned_user_id_fk': assignee, "todo_item_id_fk": todo_item.todo_item_id}))

        print("--------create_assign_record--------",create_assign_record)
        db_session.add_all(todo_user_item_data)
        if create_assign_record:
            TodoItemRepo.create_todo_items_with_assign()
        else:
            db_session.flush()
            db_session.commit()

        return True

    @staticmethod
    def create_todo_items_with_assign():
        """
        Create items with assign to users
        """
        db_session.commit()
        return True

    @staticmethod
    def assign_todo_item(todo_item_id, assign_todo_item_data):
        """
        Assign todo item
        """
        todo_user_item_data = []
        for assignee in assign_todo_item_data:
            todo_user_item_data.append(TblTodoItemUsers(
                **{'assigned_user_id_fk': assignee, "todo_item_id_fk": todo_item_id}))

        db_session.add_all(todo_user_item_data)
        db_session.commit()

        return True

    @staticmethod
    def fetch_user_todo_item(user_id,  offset, limit):
        """
            Fetch Todo Item
        """
        query = (
            TblTodoItems.query\
                .join(TblTodoItemUsers, TblTodoItems.todo_item_id == TblTodoItemUsers.todo_item_id_fk)\
                .filter(TblTodoItemUsers.assigned_user_id_fk == user_id)
        )
        total = query.count()
        user_todo_item_data = query.offset(offset).limit(limit).all()
        return total, user_todo_item_data

    @staticmethod
    def fetch_todo_item(item_id, assign_to):
        """
            Fetch Todo Item
        """
        todo_item_data = False
        todo_item_data = (
        TblTodoItems.query\
            .filter(TblTodoItemUsers.assigned_user_id_fk.in_(assign_to))\
            .filter(TblTodoItemUsers.todo_item_id_fk == item_id)
            .all()
        )
        return todo_item_data