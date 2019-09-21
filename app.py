import os

from flask import Flask

from providers_wrapper import ProvidersWrapper

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/nexmo')
    def nexmo():
        res = ProvidersWrapper.call_nexmo()
        return res

    return app
