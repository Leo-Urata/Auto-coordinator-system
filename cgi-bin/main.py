#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

html = '''Content-type: text/html;

<html>
<head>
  <meta http-equiv="Content-Type" content="text/html" charset="UTF-8" />
  <link href="../css/main.css" rel="stylesheet" type="text/css" />
  <title>人工知能(AI)アルゴリズムデザイン) 2022</title>
</head>
<body>
<nav>
  <ul>
    <li><a href=http://localhost:8888/cgi-bin/main.py>HOME</a></li>
    <li><a href=http://localhost:8888/cgi-bin/metadata_ext.py>特徴量を調べる</a></li>
    <li><a href=http://localhost:8888/cgi-bin/metadata_rep.py>データを閲覧する</a></li>
    <li><a href=http://localhost:8888/cgi-bin/search.py>類似度検索する</a></li>
  </ul>
</nav>
<h1>課題概要</h1>
%s
</body>
</html>
'''

import cgi
import os, sys
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import cv2 as cv
import pickle
from facenet_pytorch import MTCNN, InceptionResnetV1


try:
    import msvcrt
    msvcrt.setmode(0, os.O_BINARY)
    msvcrt.setmode(1, os.O_BINARY)
except ImportError:
    pass

df1=''
files=[]
form = cgi.FieldStorage()

if form.getfirst('rgb値'):
    df = pd.read_csv('./cgi-bin/metadata.csv')
    df['Unnamed: 0'] = df['0'].map(lambda s: "<img src='.{}' width='100' />".format(s))
    df1 = df.to_html(escape=False)

elif form.getfirst('AKAZE'):
    df = pd.read_csv('./cgi-bin/metadata_akaze.csv')
    df['Unnamed: 0'] = df['imgname'].map(lambda s: "<img src='.{}' width='100' />".format(s))
    df1 = df.to_html(escape=False)

elif form.getfirst('顔特徴量'):
    df = pd.read_csv('./cgi-bin/metadata_face.csv')
    df1 = df.to_html()

print (html % df1)
