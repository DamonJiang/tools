#!/usr/bin/python
# coding=utf8

import re

result = []

def vlsm(start, end, segment_left = 0, segment_right = 255, mask = 0):
    global result
    if segment_left == start and segment_right == end:
        result.append((segment_left, segment_right, mask))
        return
    segment_half = (segment_left + segment_right)/2
    if start <= segment_half:
        if end > segment_half:
            vlsm(start, segment_half, segment_left, segment_half, mask + 1)
        else:
            vlsm(start, end, segment_left, segment_half, mask + 1)
    if end > segment_half:
        if start <= segment_half:
            vlsm(segment_half + 1, end, segment_half + 1, segment_right, mask + 1)
        else:
            vlsm(start, end, segment_half + 1, segment_right, mask + 1)



def split_ip(ip_start, ip_end):
    ip_start_list = re.split(r'\.', ip_start)
    ip_end_list = re.split(r'\.', ip_end)
    total_len = len(ip_start_list) if len(ip_start_list) <= len(ip_end_list) else len(ip_end_list)
    index = 0
    pre_str = ""
    for i in range(total_len):
        if ip_start_list[i] == ip_end_list[i]:
            pre_str += "%s."%ip_start_list[i]
            continue
        vlsm(int(ip_start_list[i]), int(ip_end_list[i]))
        index = i
        break
    for item in result:
        print "%s%s%s/%s"%(pre_str,item[0],".0"*(total_len-i-1), item[2]+(index)*8)


split_ip("10.0.0.0","10.16.0.0")
#vlsm(165,186)
#print result

