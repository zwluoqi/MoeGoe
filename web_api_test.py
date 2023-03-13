#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request,send_file,make_response
# import http_fun as func
# from api import Speaker
import io
import sys
from flask import jsonify

app = Flask(__name__)

@app.route('/moegoe_web_test')
def moegoe_web_test():
    print('hello world moegoe_web_test')
    response = make_response("welcome")
    response.headers['Content-Type'] = 'text/plain'
    response.status_code = 200
    return response

if __name__ == '__main__':
    # 判断是否存在第一个参数，如果不存在就使用默认参数
    if len(sys.argv) < 2:
        _port = 44444
    else:
        _port = sys.argv[1]

    app.run(host='0.0.0.0',port=_port,debug = True)