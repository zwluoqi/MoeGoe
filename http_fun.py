#!/usr/bin/env python
# -*- coding: utf-8 -*-
class HttpRequest:
  params ={}
  
class HttpResponse:
  data = None
  status_code = 0
  mimetype = None
  def __init__(self, data: None, status_code: int,mimetype:None):
    self.data = data
    self.status_code = status_code
    self.mimetype = mimetype
