#!/usr/bin/python
# coding=utf8

import os, sys, re, hashlib, json
from optparse import OptionParser

reload(sys)  
sys.setdefaultencoding('utf8')

sep = os.path.sep if os.path.sep != "\\" else "\\\\"
indent = '  |'
print_head = '-'

dir_only, all_files, show_size, extension, ignore, config_file, hash_less = False, False, False, None, None, None, False

parser = OptionParser(description="Tool to compute hash values (sha1), default work on current path.",
    usage="python %s [path] [options]"%os.path.basename(__file__), version="Get Hash Tool v0.5.0")
parser.add_option("-d","--dir", 
    dest="dir", default=dir_only, action="store_true",
    help="show dir hash value only")
parser.add_option("-a","--all", 
    dest="all", default=all_files, action="store_true",
    help="include all files")
parser.add_option("-s","--size", 
    dest="size", default=show_size,action="store_true",
    help="show file size (Do NOT contains subdirectory)")
parser.add_option("-e","--ext", 
    dest="extension",default=extension,
    help="include extension list, use ',' to join values. eg.'exe,txt,log'")
parser.add_option("-i","--ignore",
    dest="ignore",default=ignore, 
    help="ignore files")
parser.add_option("-c","--config", 
    dest="config", default=config_file,
    help="load config file")
parser.add_option("-x","--hashless", 
    dest="hashless", default=hash_less, action="store_true",
    help="DO NOT compute hash value, list files only, invalid in config file")

(options, args) = parser.parse_args()

config_file = options.config

if config_file:
    if not os.path.exists(config_file):
        print "Config file doesn't exist"
        sys.exit(0)

    with open(config_file, 'r') as fp:
        try:
            cfg = json.loads(fp.read())
        except Exception as e:
            print "Config File Error:",e
            sys.exit(0)
        dir_only = cfg.get("dir", dir_only)
        all_files = cfg.get("all", all_files)
        show_size = cfg.get("size", show_size)
        extension = cfg.get("ext", extension)
        ignore = cfg.get("ignore",ignore)
        if not isinstance(dir_only, bool) or not isinstance(all_files, bool) or \
            not isinstance(extension, basestring) or not isinstance(ignore, basestring):
            print "'dir','all','size' should be bool type, 'ext','ignore' should be string type."

dir_only = options.dir or dir_only 
all_files = options.all or all_files
show_size = options.size or show_size
extension = options.extension or extension
ignore =  options.ignore or ignore
hash_less = options.hashless

work_path = args[0] if len(args) else os.path.abspath(os.path.dirname(__file__))
if not os.path.isdir(work_path):
    print "Please input a legal path"
    sys.exit(0)
work_path = os.path.abspath(work_path)
work_path = work_path[:-1] if work_path[-1] == sep else work_path

ext_list = list(set(re.split(',',extension))) if extension else list()
ext_list = ['.'+ x if x else x for x in ext_list]
ignore_list = list(set(re.split(',', ignore))) if ignore else list()

root_level = len(re.split(sep, work_path)) 
root_hash_tool = hashlib.sha1()

print "INCLUDE:"," ".join([x if x else "N/A" for x in ext_list])
print "IGNORE:",os.path.basename(__file__)," ".join(ignore_list)
print "PATH:", work_path

def file_filter(file):
    if file[0] == '.':
        return False
    if file == os.path.basename(__file__):
        return False
    if file in ignore_list:
        return False
    if all_files:
        return True
    ext = os.path.splitext(file)
    if ext[-1] in ext_list:
        return True
    return False


def get_hash_value(file):
    if hash_less:
        return None
    file_hash_tool = hashlib.sha1()
    with open(file,"rb") as fp:
        while True:
            line = fp.read(1024*1024*10)
            if not line:
                break;
            file_hash_tool.update(line)
    return file_hash_tool.hexdigest()


def format_size(size):
    units = ["","K","M","G","T"]
    for unit in units:
        if size < 1000:
            return "%s%s"%(size,unit)
        size = round(size/1024, 2)
    return str(size) + 'P'


def main():
    for root, dirs, files in os.walk(work_path):
        files = sorted(filter(file_filter, files))
        dirs[:] = sorted([d for d in dirs if not d[0] == '.'])

        split_path = re.split(sep, root)
        level = len(split_path) - root_level
        output_list = list()
        dir_size = 0
        dir_hash_tool = hashlib.sha1()
        dir_hash_value = '-'*10

        for file in files:
            file_hash_value = get_hash_value(os.path.join(root, file))
            if file_hash_value:
                dir_hash_tool.update(file_hash_value)
            file_size = os.path.getsize(os.path.join(root, file))
            dir_size = dir_size + file_size
            if dir_only:
                continue
            file_output_msg = indent * (level + 1) + print_head
            if not hash_less:
                file_output_msg = "%s %s"%(file_output_msg, file_hash_value)
            file_output_msg = "%s %s"%(file_output_msg, file)
            if show_size:
                file_output_msg = "%s %s"%(file_output_msg, format_size(file_size))
            if not dir_only:
                output_list.append(file_output_msg)

        if len(files):
            dir_hash_value = dir_hash_tool.hexdigest()
            root_hash_tool.update(dir_hash_value)

        dir_output_msg = indent * level + print_head + split_path[-1] + "/"
        if not hash_less:
            dir_output_msg = "%s %s"%(dir_output_msg, dir_hash_value[-10:])
        if show_size:
            dir_output_msg = "%s %s"%(dir_output_msg,format_size(dir_size))
        print dir_output_msg
        if len(output_list):
            print os.linesep.join(output_list)

    if not hash_less:
        print "HASH:", root_hash_tool.hexdigest()


if __name__ == '__main__':
    main()