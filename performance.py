#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import logging

class Performance(object):
    def __init__(self,info = None):
        self.info = info

    def __enter__(self):
        self.t = time.time()
        return self.t
    
    def __exit__(self,type,value,traceback):
        dif = 1000*(time.time()- self.t)
        logging.info("[PERF %.2f] %s : %.2fms"%(1000*time.time(),self.info,dif))
        return dif
