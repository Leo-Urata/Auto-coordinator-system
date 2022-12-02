#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

html = '''Content-type: text/html;


<html>
<head>
  <meta http-equiv="Content-Type" content="text/html" charset="UTF-8" />
  <title>ファイルをアップロードする</title>
</head>
<body>
<h1>ファイルをアップロードする</h1>
<p>%s</p>
<form action="upload.py" method="post" enctype="multipart/form-data">
  <input type="file" name="file" />
  <input type="submit" />
</form>
</body>
</html>
'''

import cgi
import os, sys
import numpy as np
import pandas as pd

try:
    import msvcrt
    msvcrt.setmode(0, os.O_BINARY)
    msvcrt.setmode(1, os.O_BINARY)
except ImportError:
    pass

content=''
files=[]
form = cgi.FieldStorage()
if 'file' in form:
    item = form['file']
    if item.file:
        fout = open(os.path.join('./img/', item.filename), 'wb')
        while True:
            chunk = item.file.read(1000000)
            if not chunk:
                break
            fout.write(chunk)
        fout.close()

    # /cgi-bin/tmpが置かれている場所を指定
    filepath='../img/'+item.filename

    content='<img src="'+filepath+'" width="50%" height="auto">'

print (html % content)
