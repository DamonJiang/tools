#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import json

def LoadJson(obj, sample):    
    def structCompare(x,y):
        if isinstance(y, dict):
            if not isinstance(x, type(y)):
                return False
            for key in y:
                if not x.has_key(key):
                    return False
                if not structCompare(x[key],y[key]):
                    return False
        elif isinstance(y, list):
            if not isinstance(x, type(y)):
                return False            
            if len(y):
               for item in x:
                   if not structCompare(item,y[0]):
                       return False
        elif isinstance(y,basestring):
            if not isinstance(x, basestring):
                return False
        return True
    jsonObj = obj
    if isinstance(obj,basestring):
        try:
            jsonObj = json.loads(obj)
        except:
            return None
    if structCompare(jsonObj ,sample):
        return jsonObj
    else:
        return None
