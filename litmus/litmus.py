"""
This file is a meant to make custom frame work like set up.
It will enable us to have a enpoints/routes for our API without
using a framework like flask or Django.
We will use WebOb to create a request and response object which 
is centered around the WSGI model.

For more info https://docs.pylonsproject.org/projects/webob/en/stable/do-it-yourself.html
"""
import os, inspect
import sys
import re
from webob import Request, exc, Response
import tempita
"""
Here we create the regular expression(var_regex).
The re.VERBOSE flag makes the regular expression
parser ignore whitespace and allow comments.
"""
var_regex = re.compile(r'''
    \{          # The exact character "{"
    (\w+)       # The variable name (restricted to a-z, 0-9, _)
    (?::([^}]+))? # The optional :regex part
    \}          # The exact character "}"
    ''', re.VERBOSE)

def template_to_regex(template):
    """ Function to compile templates to regular expressions."""
    # This variable will hold the regular expression that we are creating.
    regex = ''
    # This contains the position of the end of the last match.
    last_pos = 0
    for match in var_regex.finditer(template): # The finditer method yields all the matches.
        # On the next line, We're getting all the non-{} text from after the last match,
        # up to the beginning of this match.
        # We call re.escape on that text, which escapes any characters that have special meaning.
        # So .html will be escaped as \.html.
        regex += re.escape(template[last_pos:match.start()])
        var_name = match.group(1) # The first match is the variable name.
        # expr is the regular expression we'll match against, the optional second match.
        # The default is [^/]+, which matches any non-empty, non-/ string.
        expr = match.group(2) or '[^/]+'
        expr = '(?P<%s>%s)' % (var_name, expr)
        regex += expr
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    regex = '^%s$' % regex
    return regex
 
def load_controller(string):
    module_name, func_name = string.split(':', 1)
    __import__(module_name)
    module = sys.modules[module_name]
    func = getattr(module, func_name)
    return func


class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, template, controller, **vars):
        if isinstance(controller, str):
            controller = load_controller(controller)
        self.routes.append((re.compile(template_to_regex(template)),controller,vars))

    def __call__(self, environ, start_response):
        """
        This method makes the Router object itself a WSGI application.
        """
        req = Request(environ)
        for regex, controller, vars in self.routes:
            match = regex.match(req.path_info)
            if match:
                req.urlvars = match.groupdict()
                req.urlvars.update(vars)
                return controller(environ, start_response)
        return exc.HTTPNotFound('No route matched')(environ, start_response)

def rest_controller(cls):
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            instance = cls(req, **req.urlvars)
            action = req.urlvars.get('action')
            if action:
                action += '_' + req.method.lower()
            else:
                action = req.method.lower()
            try:
                method = getattr(instance, action)
            except AttributeError:
                raise exc.HTTPNotFound("No action %s" % action)
            resp = method()
            if isinstance(resp, str):
                resp = Response(body=resp)
        except exc.HTTPException as e:
            resp = e
        return resp(environ, start_response)
    return replacement
