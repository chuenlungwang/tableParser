import sys
import os

import configParser as parser
from os.path import join as path_join

ignore_dir = [".git"]

def _list_dir_tree(root, path, ret):
    subdirs = [path_join(path, f) for f in os.listdir(path) if os.path.isdir(path_join(path, f))]
    if len(subdirs) == 0:
        return
    else:
        for f in subdirs:
            shortpath = f[len(root)+1:]
            if shortpath in ignore_dir:
                continue
            ret.append(shortpath)
            _list_dir_tree(root, f, ret)

def list_dir_tree(path):
    ret = ['.']
    _list_dir_tree(path, path, ret)
    return ret

def mkdir_tree(root, dirs):
    for f in dirs:
        try:
            os.mkdir(path_join(root, f))
        except OSError:
            pass

def generate(srcpath, despath) :
    if (srcpath is None) or (despath is None):
        print("Require argument srcpath and despath")
        return

    subdirs = list_dir_tree(srcpath)
    if not os.path.exists(despath):
        os.makedirs(despath)
    mkdir_tree(despath, subdirs)
    for d in subdirs:
        srcdir = path_join(srcpath, d)
        desdir = path_join(despath, d)
        meta_files = [path_join(srcdir, f) for f in os.listdir(srcdir)
                      if os.path.isfile(path_join(srcdir, f))
                      and f.endswith('xml')]
        for mf in meta_files :
            parser.parse(mf, srcdir, desdir)

if __name__ == "__main__" :
    if len(sys.argv) == 3 :
        srcpath = sys.argv[1]
        despath = sys.argv[2]
        generate(srcpath, despath)
    else:
        print("Usage: python TableBuild.py *srcpath* *despath*")
