""" Third party api wrappers"""
import os
import json
import africastalking

username = os.getenv('africastalking_username')
api_key = os.getenv('africastalking_api_key')
africastalking.initialize(username, api_key)
sms = africastalking.SMS


class ProvidersWrapper:
    """ Class with all the thirdy party helper functions"""

    def send_message(number, message):
        response = sms.send(message, ['+' + number])
        return response
