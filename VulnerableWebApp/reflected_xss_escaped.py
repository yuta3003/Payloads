from bottle import route
from bottle import run
from bottle import request
import html

@route('/')
def hello(user=''):
    username = request.query.get('user')
    username = '' if username is None else username
    username = html.escape(username)
    
    body = "<h2> Hello {name} </h2>".format(name=username)
    
    return body

run(host='0.0.0.0', port=8080, debug=True)


"""
http://0.0.0.0:8080/user=Alice
http://0.0.0.0:8080/user=<br><s>Alice</s>
http://0.0.0.0:8080/user=<script>alert('JavaScript injected')</script>
"""
