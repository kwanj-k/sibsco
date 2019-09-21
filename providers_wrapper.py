""" Third party api wrappers"""

import nexmo
import json

class ProvidersWrapper:
    """ Class with all the thirdy party helper functions"""

    def call_nexmo():
        client = nexmo.Client(key='e3f0b9ad', secret='s4gTYtjsWFrJdxgr')
        response = client.send_message({
            'from': 'Nexmo',
            'to': '254703852333',
            'text': 'Hello from Nexmo',
            })
        if response["messages"][0]["status"] == "0":
            res = {"status":"Success", "message":"Message sent successfully"}, 200
        else:
            res = f"Message failed with error: {responseData['messages'][0]['error-text']}"
        return res
        
