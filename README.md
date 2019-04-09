Table Parser Repository
=======================

This project is created for parse config in Excel into several language, such
as Lua, json.

Each configuration file has its own meta file -- an xml file, which describe
source file name, data sheet, data column name and field name, field type.

Config data supports `int32`, `int64`, `float`, `bool`, `string` and `array` types. The element type of
`array` could be any scalar type support.

How To Test
===========

If you want to test, just type this command:

    make test

For clear directory:
    
    make clean
