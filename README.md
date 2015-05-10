# grepsql
read parts of a text file using a SQL like syntax

This will go through a line by line and parse it out into the one or more regex patterns defined.  It will then apply the where clause to those patterns and return matching rows.  It will then format the output the values in a comma delimited list


## Usage
```
grepsql.py SELECT /regex/ AS column FROM file WHERE column = val
```
or
```
grepsql.py "SELECT /regex/ AS column FROM file WHERE column = val"
```

### SELECT /regex/ as column
This is in the format of ```SELECT /regex/ AS column1, /regex/ AS column2, ...```
One or more columns may be defined with a regex parameter and a name

### FROM filename
This is the name of the file to read.  Skip the FROM section entirely to read from STDIN instead.

### WHERE column = val
Check the parsed values in some way. Valid comparisons: = <> != <= =>.
*note: due to problems with the way the command line is parsed, the greater than or less than parameters may not work as expected.  In this case you must enclose the entire SQL in quotes*

##Example
Let's say you have apache logs that look like this:

```
127.0.0.1 - - [10/May/2015:14:52:11 +0200] "GET / HTTP/1.1" 200 2594
127.0.0.1 - - [10/May/2015:14:52:11 +0200] "GET /icons/blank.gif HTTP/1.1" 200 148
127.0.0.1 - - [10/May/2015:14:52:11 +0200] "GET /icons/text.gif HTTP/1.1" 200 229
127.0.0.1 - - [10/May/2015:14:52:11 +0200] "GET /icons/unknown.gif HTTP/1.1" 200 245
127.0.0.1 - - [10/May/2015:14:52:11 +0200] "GET /icons/folder.gif HTTP/1.1" 200 225
127.0.0.1 - - [10/May/2015:14:52:18 +0200] "GET /notfound.html HTTP/1.1" 404 1031
127.0.0.1 - - [10/May/2015:14:52:25 +0200] "GET /admin.html HTTP/1.1" 404 1031
127.0.0.1 - - [10/May/2015:14:52:29 +0200] "GET /admin/ HTTP/1.1" 404 1031

```

To look through the logs 
```
./grepsql.py SELECT /[0-9.]*/ AS IP, /\\[.*?\\]/ AS Date, /\".*\"/ AS Resource , /\\d\\d\\d/ AS Response FROM access_log WHERE response = 404
```

this will process th file 'access_log', parse each line into IP, Date, Resource, and Response values.  It will then filter out all rows where Response is equal to "404".

The output looks like this:
```
"IP", "Date", "Resource", "Response"
"127.0.0.1", "[10/May/2015:14:52:18 +0200]", "\"GET /notfound.html HTTP/1.1\"", "404"
"127.0.0.1", "[10/May/2015:14:52:25 +0200]", "\"GET /admin.html HTTP/1.1\"", "404"
"127.0.0.1", "[10/May/2015:14:52:29 +0200]", "\"GET /admin/ HTTP/1.1\"", "404"

```

