# -*- coding: utf-8 -*-

import re


def lua_dumps(lua_content):
    if type(lua_content) != dict:
        return putScalar(lua_content)

    items = ["[{0}]={1}".format(putScalar(key), putValue(value))
             for key, value in sorted(lua_content.iteritems())]
    return "{{{0}}}".format(",".join(items))


ESCAPE = re.compile(u'[\\\"\b\f\n\r\t\v]')
ESCAPE_DCT = {
    '\\': '\\\\',
    '"': '\\"',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
    '\v': '\\v'
}


def escape(s):
    def replace(match):
        return ESCAPE_DCT[match.group(0)]
    return '"' + ESCAPE.sub(replace, s) + '"'


def putValue(v):
    if type(v) == list:
        return putList(v)
    else:
        return putScalar(v)


def putScalar(v):
    tv = type(v)
    if tv == str:
        return escape(v)
    else:
        return str(v)


def putList(v):
    items = [putScalar(x) for x in v]
    return "{{{0}}}".format(",".join(items))