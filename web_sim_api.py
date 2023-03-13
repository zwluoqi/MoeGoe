#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from math import fabs
import os
import web
import time
import hashlib
import os
import http_fun as func
from api import Speaker

urls = (
    '/moegoe_web_test', 'moegoe_web_test',
    '/moegoe_web_speaker', 'moegoe_web_speaker',
    '/moegoe_web', 'moegoe_web',
)

speaker = Speaker('models/genshion/config.json', 'models/genshion/model.pth')

class moegoe_web_test:

    def __init__(self):
        print('__init__')

    def GET(self):
        print('GET')
        # 获取输入参数
        return '''['特别周', '无声铃鹿', '东海帝皇（帝宝，帝王）', '丸善斯基', '富士奇迹', '小栗帽', '黄金船', '伏特加', '大和赤骥', '大树快车', '草上飞', '菱亚马逊', 
    '目白麦昆', '神鹰', '好歌剧', '成田白仁', '鲁道夫象征（皇帝）', '气槽', '爱丽数码', '星云天空', '玉藻十字', '美妙姿势', '琵琶晨光', '摩耶重炮', '曼城茶座', '美浦波旁', '目白赖恩', 
    '菱曙', '雪中美人', '米浴', '艾尼斯风神', '爱丽速子（爱丽快子）', '爱慕织姬', '稻荷一', '胜利奖券', '空中神宫', '荣进闪耀', '真机伶', '川上公主', '黄金城（黄金城市）', '樱花进王', 
    '采珠', '新光风', '东商变革', '超级小海湾', '醒目飞鹰（寄寄子）', '荒漠英雄', '东瀛佐敦', '中山庆典', '成田大进', '西野花', '春丽（乌拉拉）', '青竹回忆', '微光飞驹', '美丽周日', 
    '待兼福来', 'mr cb（cb先生）', '名将怒涛（名将户仁）', '目白多伯', '优秀素质', '帝王光辉', '待兼诗歌剧', '生野狄杜斯', '目白善信', '大拓太阳神', '双涡轮（两立直，两喷射，二锅头，逆喷射）',
               ]'''
        # i = web.input(name=None)
        # return self.render.index(i.name)


    def POST(self):
        print('POST')
        return '''['特别周', '无声铃鹿', '东海帝皇（帝宝，帝王）', '丸善斯基', '富士奇迹', '小栗帽', '黄金船', '伏特加', '大和赤骥', '大树快车', '草上飞', '菱亚马逊', 
    '目白麦昆', '神鹰', '好歌剧', '成田白仁', '鲁道夫象征（皇帝）', '气槽', '爱丽数码', '星云天空', '玉藻十字', '美妙姿势', '琵琶晨光', '摩耶重炮', '曼城茶座', '美浦波旁', '目白赖恩', 
    '菱曙', '雪中美人', '米浴', '艾尼斯风神', '爱丽速子（爱丽快子）', '爱慕织姬', '稻荷一', '胜利奖券', '空中神宫', '荣进闪耀', '真机伶', '川上公主', '黄金城（黄金城市）', '樱花进王', 
    '采珠', '新光风', '东商变革', '超级小海湾', '醒目飞鹰（寄寄子）', '荒漠英雄', '东瀛佐敦', '中山庆典', '成田大进', '西野花', '春丽（乌拉拉）', '青竹回忆', '微光飞驹', '美丽周日', 
    '待兼福来', 'mr cb（cb先生）', '名将怒涛（名将户仁）', '目白多伯', '优秀素质', '帝王光辉', '待兼诗歌剧', '生野狄杜斯', '目白善信', '大拓太阳神', '双涡轮（两立直，两喷射，二锅头，逆喷射）',
    1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
        1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
               ]'''

class moegoe_web_speaker:
    def __init__(self):
        print('moegoe_web_speaker __init__')

    def GET(self):
        print('moegoe_web_speaker GET')
        input_data = web.input()
        input_dict = dict(input_data)
        response = speaker.getSpeakers()
        return response

    def POST(self):
        print('POST')
        return "moegoe_web_speaker post"

class moegoe_web:
    def __init__(self):
        print('moegoe_web __init__')

    def GET(self):
        print('moegoe_web GET')
        input_data = web.input()
        input_dict = dict(input_data)

        funcrequest = func.HttpRequest()
        funcrequest.params = input_dict
        funresponse =  speaker.main(funcrequest)
        if len(funresponse.mimetype) >0:
            # 设置Content-Type头为audio/mpeg
            web.header('Content-Type', funresponse.mimetype)
            web.header('Content-Disposition', 'attachment; filename="audio.wav"')
            return funresponse.data
            # file_obj = io.BytesIO(funresponse.data)
            # return send_file(file_obj, mimetype='audio/wav', as_attachment=False)
        else:
            # Return text response
            # response = make_response(funresponse.data)
            # response.headers['Content-Type'] = 'text/plain'
            web.ctx.status = str(funresponse.status_code) + " " + funresponse.data
            # [ZH]今天天气好极了,你觉得呢,宝贝[ZH]
            return funresponse.data
        
    def POST(self):
        print('POST')
        return "moegoe_web post"
        
if __name__ == "__main__":
    application = web.application(urls, globals())
    application.run()
    print('hello world')