import os
from litmus import Router, rest_controller

from message_service import MessageService
app = Router()

message_service = rest_controller(MessageService)
app.add_route('/', controller=message_service)

if __name__ == '__main__':
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port=8000)
