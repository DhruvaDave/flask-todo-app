from flask import jsonify, make_response

from todo_app.common import constants 

class HttpResponseHandler:
    """
    Common methods to handle http responses.
    """
    
    @staticmethod
    def build(message, http_code, custom_code, **kwargs):
        response_dict = {
            'code': custom_code,
            'message': message
        }
        response_dict.update(kwargs)
        return jsonify(response_dict), http_code

    @staticmethod
    def invalid_credentials(message="Invalid Credentials",  **kwargs):
        return HttpResponseHandler\
            .build(message=message, http_code=constants.BAD_REQUEST_CODE,
                   custom_code=constants.UNAUTHORISED, **kwargs)

    @staticmethod
    def build_with_page(page, data, message="Success",**kwargs):
        response_dict = {
            'page': page["page_no"],
            'page_size': page["page_size"],
            'data': data,
            'total_records': page['total_records'],
            'code': constants.SUCCESS
        }
        response_dict.update(kwargs)
        return HttpResponseHandler.build(message=message, http_code=constants.SUCCESS_CODE,
                                         custom_code=constants.SUCCESS, **response_dict)

    @staticmethod
    def success(message="Success",**kwargs):
        response_dict = {
            'code': constants.SUCCESS,
            'message': message
        }
        response_dict.update(kwargs)
        return jsonify(response_dict),constants.SUCCESS_CODE

    @staticmethod
    def bad_request(message="Bad Request"):
        return jsonify( {
            'code': constants.BAD_REQUEST,
            'message': message
        }), constants.BAD_REQUEST_CODE

    @staticmethod
    def exist(message="Entity Already Exist", **kwargs):
        response_dict = {
            'code': constants.ENTITY_EXISTS,
            'message': message
        }
        if kwargs:
            response_dict.update(kwargs)
        return jsonify(response_dict), constants.BAD_REQUEST_CODE

    @staticmethod
    def invalid_request_entity(message="Entity Does not Exist"):
        return jsonify({
            'code': constants.NO_ENTITY_FOUND,
            'message': message
        }), constants.BAD_REQUEST_CODE


    @staticmethod
    def no_data(message="Entity Does not Exist"):
        return jsonify({
            'code': constants.NO_CONTENT,
            'message': message
        }), constants.NO_CONTENT_CODE
