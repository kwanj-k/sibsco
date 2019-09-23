import json
import queue
from threading import Thread

from providers import ProvidersWrapper


with open("messages.json") as json_file:
    meassages = json.load(json_file)
    messages_list = meassages['messages']

messages_queue = queue.Queue()
for message in messages_list:
    messages_queue.put(message)

num_of_threads = 2

class MessageService:
    def __init__(self, req):
        self.request = req

    def get(self):
        res = {"message":"Make a post request on this endpoint to send messages."}
        return json.dumps(res)

    def post(self):
        while not messages_queue.empty():
            msg = messages_queue.get()
            number = msg['number']
            message = msg['message']
            ProvidersWrapper.send_message(number, message)
            res = {"message":"messages sent"}
        return json.dumps(res)
