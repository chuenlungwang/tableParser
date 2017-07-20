# -*- coding: utf-8 -*-
from __future__ import print_function

import sys

reload(sys)
sys.setdefaultencoding('utf8')

from collections import namedtuple
import xml.etree.ElementTree as ET
import os
import json
import codecs

import xlrd

File  = namedtuple('File',  ['name', 'language', 'sheets'])
Sheet = namedtuple('Sheet', ['dest', 'key', 'fields'])
Field = namedtuple('Field', ['name', 'type', 'element'])

def process_field_element(field):
    field_name = field.get('name')
    field_type = field.get('type')
    field_element = field.get('element')
    return Field(field_name, field_type, field_element)

def process_sheet_element(sheet):
    sheet_dest = sheet.get('dest')
    sheet_key  = sheet.get('key')
    fields = {}
    for x in sheet.findall('field'):
        fields[x.get('column')] = process_field_element(x)
    return Sheet(sheet_dest, sheet_key, fields)

def process_file_element(fileE):
    fileName = fileE.get('name')
    languages = [ x.text for x in fileE.findall('./language/name')]
    sheets = {}
    for x in fileE.findall('sheet'):
        sheets[x.get('name')] = process_sheet_element(x)
    return File(fileName, languages, sheets)

def parse_xml_meta(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return [process_file_element(x) for x in root.findall('file')]

def refine(type, element, value):
    value = value.strip()
    if len(value) == 0:
        return None

    if type == "int32":
        return int(float(value))
    elif type == "int64":
        return long(float(value))
    elif type == "string":
        return value
    elif type == "array":
        return [refine(element, None, str(x)) for x in eval(value)]

def read_xlsx(file_path, sheet_metaes):
    workbook = xlrd.open_workbook(file_path)
    xlsx_content = {}
    for sheetname, sheet_meta in sheet_metaes.iteritems():
        sheet = workbook.sheet_by_name(sheetname)
        col_index = {}
        for x in xrange(sheet.ncols):
            colname = sheet.cell(0, x).value
            if colname in sheet_meta.fields:
                col_index[colname] = x

        sheet_content = {} if sheet_meta.key else []
        for x in xrange(1, sheet.nrows):
            key_value = None
            row_value = {}
            for colname, field in sheet_meta.fields.iteritems():
                col = col_index[colname]
                field_value = refine(field.type, field.element, str(sheet.cell(x, col).value))
                row_value[field.name] = field_value
                if field.name == sheet_meta.key :
                    assert field.type != 'array'
                    key_value = field_value
            if type(sheet_content) == dict :
                sheet_content[key_value] = row_value
            else:
                sheet_content.append(row_value)

        xlsx_content[sheet_meta.dest] = sheet_content

    return xlsx_content

def parse(meta_file, src_dir, dest_dir) :
    files = parse_xml_meta(meta_file)

    if not os.path.exists(dest_dir) :
        os.mkdir(dest_dir, 0755)
    for file in files:
        file_path = os.path.join(src_dir, file.name)
        if os.path.isfile(file_path) :
            xlsx_content = read_xlsx(file_path, file.sheets)
            for dest_name, config_content in xlsx_content.iteritems() :
                dest_path = os.path.join(dest_dir, dest_name + ".json")
                with codecs.open(dest_path, 'w', 'utf-8') as f :
                    json_str = json.dumps(config_content,
                                          sort_keys    = True,
                                          ensure_ascii = False,
                                          indent       = 4,
                                          separators   = (',', ":"))
                    f.write(json_str)
