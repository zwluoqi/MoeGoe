#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request,send_file,make_response
import http_fun as func
from api import Speaker
import io
import sys

app = Flask(__name__)
speaker = Speaker('models/genshion/config.json', 'models/genshion/model.pth')

@app.route('/moegoe_web')
def moegoe_web():
    print('hello world get')
    data = request.args.to_dict()
    
    funcrequest = func.HttpRequest()
    funcrequest.params = data
    funresponse =  speaker.main(funcrequest)
    if len(funresponse.mimetype) >0:
        file_obj = io.BytesIO(funresponse.data)
        return send_file(file_obj, mimetype='audio/wav', as_attachment=False)


    else:
        # Return text response
        response = make_response(funresponse.data)
        response.headers['Content-Type'] = 'text/plain'
    response.status_code = funresponse.status_code
    # [ZH]今天天气好极了,你觉得呢,宝贝[ZH]
    return response

@app.route('/moegoe_post', methods=['POST'])
def moegoe_post():
    print('hello world post')
    data = request.form.to_dict()
    print(data)

    return ""

if __name__ == '__main__':
    # 判断是否存在第一个参数，如果不存在就使用默认参数
    if len(sys.argv) < 2:
        _port = 44444
    else:
        _port = sys.argv[1]

    app.run(host='0.0.0.0',port=_port,debug = True)
