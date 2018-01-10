from flask_api.exceptions import APIException
from werkzeug.exceptions import HTTPException


class InvalidParameter(APIException):
    status_code = 204
    detail = 'Invalid parameters'


class TaskNotFound(APIException):
    status_code = 404
    detail = 'This task does not exist'


class PageNotFound(HTTPException):
    code = 404
    description = 'We couldn\'t find the page you requested'
