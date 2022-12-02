#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

html = '''Content-type: text/html;

<html lang="ja">
  <head>
    <!-- Required meta tags -->
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <title>画像類似検索</title>
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
    
    <h1 class="m-3">画像類似検索</h1>
    <form action="search.py" method="post" enctype="multipart/form-data">
        <input type="file" name="file" />
        <input type="submit" />
    </form>
    %s

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
import read_wakachi
import numpy as np
import pandas as pd
import glob
import re
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from PIL import Image
import matplotlib
matplotlib.use('Agg')
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

# metadata.csvの置き場所を指定
df1=''
df2=''
df3=''
contents=''
title=[]
score=[]
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

#    cgi用パス
    filepath='./img/'+item.filename
#    content用パス
    Filepath='../img/'+item.filename

#    クエリベクトル生成機能
    def ext_mean_rgb(filepath):
      image = np.array(Image.open(filepath).convert('RGB')).reshape(-1,3)
      return np.array([np.mean(image[:,0]),np.mean(image[:,1]),np.mean(image[:,2])])
    qvec=ext_mean_rgb(filepath)

#    meta.csv読み込み機能
    df = pd.read_csv('./metadata.csv', index_col=0)
    tfilepaths=df['0']
    rgbs=df[['1','2','3']]

#    qvecとコサイン類似度を計算する
    def comp_sim(qvec,tvec):
        return np.dot(qvec, tvec) / (np.linalg.norm(qvec) * np.linalg.norm(tvec))
    
    result=np.array([])
    for i in range(rgbs.index.shape[0]):
      result=np.append(result, comp_sim(qvec, rgbs.iloc[i,:].to_numpy()))

#    類似度が大きい順にソートして表示
    rank=np.argsort(result)
    
    for index in rank[:-rank.shape[0]-1:-1]:
        title.append('{}'.format(tfilepaths[index]))
    
    for index in rank[:-rank.shape[0]-1:-1]:
        score.append('{}'.format(result[index]))
     
    df1 = pd.DataFrame(data={'小説ファイル名': title, '類似度': score})
    df2 = df1.set_index(['小説ファイル名','類似度'])
    df3 = df2.to_html()
    contents='<table border="1">'
    for index in rank[:-rank.shape[0]-1:-1]:
        contents=contents+'<tr><td><img src=".'+tfilepaths[index]+'" width="25%" hight="auto"></td><td>'+str(result[index])+'</td></tr>'
    contents=contents+'</table>'

#num=sum(qvec == 1)
#print (html % (df3, contents))
print (html %  contents)

