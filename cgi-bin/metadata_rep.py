#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

html = '''Content-type: text/html;


<html lang="ja">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html" charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <title>ファイルの中身を確認する</title>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-3">
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item active">
            <a class="nav-link" href=http://localhost:8888/cgi-bin/home.py>HOME</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href=http://localhost:8888/cgi-bin/metadata_ext.py>特徴量を調べる</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href=http://localhost:8888/cgi-bin/metadata_rep.py>データを閲覧</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href=http://localhost:8888/cgi-bin/search.py>類似度計算</a>
          </li>
        </ul>
      </div>
    </nav>
    
    <h1 class="m-3">ファイルの中身を確認する</h1>
    <div class="m-3">%s</div>
    <form action="metadata_rep.py" method="post" enctype="multipart/form-data">
      <input type="radio" name="rgb値" value="[1]" />rgb値
      <input type="radio" name="AKAZE" value="[2]" />AKAZE
      <input type="radio" name="顔特徴量" value="[3]" />顔特徴量
        <input type="submit" />
    </form>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
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
    df['Unnamed: 0'] = df['imgname'].map(lambda s: "<img src='.{}' width='100' />".format(s))
    df1 = df.to_html(escape=False)

elif form.getfirst('AKAZE'):
    df = pd.read_csv('./cgi-bin/metadata_akaze.csv')
    df['Unnamed: 0'] = df['imgname'].map(lambda s: "<img src='.{}' width='100' />".format(s))
    df1 = df.to_html(escape=False)

elif form.getfirst('顔特徴量'):
    df = pd.read_csv('./cgi-bin/metadata_face.csv')
    df1 = df.to_html()

print (html % df1)

