#!/usr/bin/python
import sys
import re


def parseargs(args):
    parsed = {}
    parsed['select'] = []
    parsed['from'] = None
    parsed['where'] = []

    i = 1
    state = 'select'
    while i < len(args):
        thisarg = args[i]
        if state == 'select' and thisarg[0] == '/' and thisarg[-1] == '/':
            # regex field definition
            regex = thisarg[1:-1]
            column = ''
            if len(args) > i + 2:
                if args[i+1].lower() == 'as':
                    column = args[i+2]
                    if column[-1] == ',':
                        column = column[0:-1]
                    i += 2
            parsed['select'].append({'column': column, 'regex': regex})
        elif thisarg.lower() == 'from':
            state = 'from'
            if len(args) > i+1:
                parsed['from'] = args[i+1]
                i +=1
        elif thisarg.lower() == 'where':
            state = 'where'
        elif state == 'where' and thisarg.lower() != 'and':
            column = thisarg
            if(col for col in parsed['select'] if col['column'] == column):
                # known column name
                if len(args) > i + 2:
                    operator = args[i+1]
                    compare = args[i+2]
                    parsed['where'].append({'column': column, 'operator': operator, 'compare': compare})
                    i += 2
        i += 1
    return parsed


def compare(obj, op, val):
    if op == "=":
        return obj.lower() == val.lower()
    if op == "<>" or op == "!=":
        return obj.lower() != val.lower()
    if op == ">":
        return obj > val
    if op == ">=" or "=>":
        return obj >= val
    if op == "<":
        return obj < val
    if op == "<=" or "=<":
        return obj <= val

def processline(args, regex, line):
    row = {}
    display = True
    try:
        match = re.match(regex, line)
        if match:
            for col in args['select']:
                val = match.group((col['column']))
                for condition in args['where']:
                    if condition['column'].lower() == col['column'].lower():
                        display = display and compare(val, condition['operator'], condition['compare'])
                row[col['column']] = val
    finally:
        if row and display:
            format(args, row)


def format(args, row):
    first = True
    line = ""
    for col in args['select']:
        if first:
            first = False
        else:
            line += ", "
        val = row[col['column']]
        line += "\"%s\"" % val.replace("\"", "\\\"")
    print line

def do(commandline):
    args = parseargs(commandline)
    regex = ""
    headerLine = ""
    firstline = True
    for col in args['select']:
        if firstline:
            firstline = False
        else:
            regex += ".*?"
            headerLine += ", "
        regex += "(?P<%s>%s)" % (col['column'], col['regex'])
        headerLine += "\"%s\"" % col['column']
    print headerLine
    if args['from'] is None:
        for line in sys.stdin:
            processline(args, regex, line)
    else:
        with open(args['from'], mode='r') as f:
            for line in f:
                processline(args, regex, line)


if len(sys.argv) > 2:
    do(sys.argv)
else:
    do(sys.argv[-1].split())