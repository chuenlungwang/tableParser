# -*- coding: utf-8 -*-

import re
import json


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
    elif tv == bool:
        return "true" if v else "false"
    else:
        return str(v)


def putList(v):
    items = [putValue(x) for x in v]
    return "{{{0}}}".format(",".join(items))


def simple_format_lua(content):
    template = "local M = {{\n\t{0}\n}}\nreturn M"
    if isinstance(content, list):
        lines = [lua_dumps(x) for x in content]
        return template.format(",\n\t".join(lines))
    else:
        lines = ["[{0}] = {1}".format(lua_dumps(key), lua_dumps(value))
                 for key, value in content.iteritems()]
        return template.format(",\n".join(lines))


def json_dumps(json_content):
    return json.dumps(json_content,
                      sort_keys=True,
                      ensure_ascii=False,
                      separators=(',', ':'))


def simple_format_json(content):
    if isinstance(content, list):
        lines = [json_dumps(x) for x in content]
        return '[\n{0}\n]'.format(',\n'.join(lines))
    else:
        lines = ["{0}:{1}".format(json_dumps(str(key)), json_dumps(value))
                 for key, value in content.iteritems()]
        return '{{\n{0}\n}}'.format(',\n'.join(lines))
