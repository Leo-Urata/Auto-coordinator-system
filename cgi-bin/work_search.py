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

    <title>オートコーディネート</title>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item active">
            <a class="nav-link" href=http://localhost:8888/cgi-bin/work_home.py>HOME</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href=http://localhost:8888/cgi-bin/work_ext.py>アイテム登録</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href=http://localhost:8888/cgi-bin/work_rep.py>アイテムリスト</a>
          </li>
         <li class="nav-item dropdown active">
            <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">オートコーディネート</a>
            <div class="dropdown-menu">
              <a class="dropdown-item" href=http://localhost:8888/cgi-bin/work_search.py>自分で画像を選ぶ</a>
              <a class="dropdown-item" href=http://localhost:8888/cgi-bin/work_search_2.py>テンプレートから選ぶ</a>
            </div>
          </li>
        </ul>
      </div>
    </nav>
    
    <div class="container bg-light">
        <h1 class="pt-3 ml-3"><span class="badge badge-secondary">オートコーディネート</span></h1>
        <form class="was-validated" action="work_search.py" method="post" enctype="multipart/form-data">
          <div class="custom-file w-50 m-3">
            <input type="file" class="custom-file-input" name="outer_file" />
            <label class="custom-file-label">アウター</label>
          </div>
          <div class="custom-file w-50 m-3">
            <input type="file" class="custom-file-input" name="tops_file" />
            <label class="custom-file-label">トップス</label>
          </div>
          <div class="custom-file w-50 m-3">
            <input type="file" class="custom-file-input" name="buttoms_file" />
            <label class="custom-file-label">ボトムス</label>
          </div>
          <div>
          <input class="btn btn-primary m-3" type="submit" />
          </div>
        </form>
        <div class="m-3">%s</div>
        <div class="m-3">%s</div>
        <div class="m-3">%s</div>
        <div class="m-3">%s</div>
        <div class="m-3">%s</div>
        <div class="m-3">%s</div>
    </div>

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
#df1=''
#df2=''
#df3=''
contents1=''
contents2=''
contents3=''
label1=''
label2=''
label3=''
title=[]
score=[]
form = cgi.FieldStorage()


if 'outer_file' in form:
    item = form['outer_file']
    if item.file:
        fout = open(os.path.join('./outer_code_img/', item.filename), 'wb')
        while True:
            chunk = item.file.read(1000000)
            if not chunk:
                break
            fout.write(chunk)
        fout.close()

#    cgi用パス
    filepath='./outer_code_img/'+item.filename
#    content用パス
    Filepath='../outer_img/'+item.filename

#    クエリベクトル生成機能
    def ext_mean_rgb(filepath):
      image = np.array(Image.open(filepath).convert('RGB')).reshape(-1,3)
      return np.array([np.mean(image[:,0]),np.mean(image[:,1]),np.mean(image[:,2])])
    qvec=ext_mean_rgb(filepath)

#    meta.csv読み込み機能
    df = pd.read_csv('./cgi-bin/metadata/metadata_outer.csv', index_col=0)
    tfilepaths=df['imgname']
    rgbs=df[['R','G','B']]

#    qvecとコサイン類似度を計算する
    def comp_sim(qvec,tvec):
        return np.dot(qvec, tvec) / (np.linalg.norm(qvec) * np.linalg.norm(tvec))
    
    result=np.array([])
    for i in range(rgbs.index.shape[0]):
      result=np.append(result, comp_sim(qvec, rgbs.iloc[i,:].to_numpy()))

#    類似度が大きい順にソートして表示
    rank=np.argsort(result)
    
    for index in rank[:-rank.shape[0]+1:-10000]:
        title.append('{}'.format(tfilepaths[index]))
    
    for index in rank[:-rank.shape[0]+1:-10000]:
        score.append('{}'.format(result[index]))
     
    contents1='<table border="1">'
    for index in rank[:-rank.shape[0]+1:-10000]:
        contents1=contents1+'<tr><td><img src=".'+tfilepaths[index]+'" width="25%" hight="auto"></td><td>'+str(result[index])+'</td></tr>'
    contents1=contents1+'</table>'
    label1='<h2>アウター</h2>'
    
    
    
if 'tops_file' in form:
    item = form['tops_file']
    if item.file:
        fout = open(os.path.join('./tops_code_img/', item.filename), 'wb')
        while True:
            chunk = item.file.read(1000000)
            if not chunk:
                break
            fout.write(chunk)
        fout.close()

#    cgi用パス
    filepath='./tops_code_img/'+item.filename
#    content用パス
    Filepath='../tops_img/'+item.filename

#    クエリベクトル生成機能
    def ext_mean_rgb(filepath):
      image = np.array(Image.open(filepath).convert('RGB')).reshape(-1,3)
      return np.array([np.mean(image[:,0]),np.mean(image[:,1]),np.mean(image[:,2])])
    qvec=ext_mean_rgb(filepath)

#    meta.csv読み込み機能
    df = pd.read_csv('./cgi-bin/metadata/metadata_tops.csv', index_col=0)
    tfilepaths=df['imgname']
    rgbs=df[['R','G','B']]

#    qvecとコサイン類似度を計算する
    def comp_sim(qvec,tvec):
        return np.dot(qvec, tvec) / (np.linalg.norm(qvec) * np.linalg.norm(tvec))
    
    result=np.array([])
    for i in range(rgbs.index.shape[0]):
      result=np.append(result, comp_sim(qvec, rgbs.iloc[i,:].to_numpy()))

#    類似度が大きい順にソートして表示
    rank=np.argsort(result)
    
    for index in rank[:-rank.shape[0]+1:-10000]:
        title.append('{}'.format(tfilepaths[index]))
    
    for index in rank[:-rank.shape[0]+1:-10000]:
        score.append('{}'.format(result[index]))
     
    contents2='<table border="1">'
    for index in rank[:-rank.shape[0]+1:-10000]:
        contents2=contents2+'<tr><td><img src=".'+tfilepaths[index]+'" width="25%" hight="auto"></td><td>'+str(result[index])+'</td></tr>'
    contents2=contents2+'</table>'
    label2='<h2>トップス</h2>'
    
    
if 'buttoms_file' in form:
    item = form['buttoms_file']
    if item.file:
        fout = open(os.path.join('./buttoms_code_img/', item.filename), 'wb')
        while True:
            chunk = item.file.read(1000000)
            if not chunk:
                break
            fout.write(chunk)
        fout.close()

#    cgi用パス
    filepath='./buttoms_code_img/'+item.filename
#    content用パス
    Filepath='../buttoms_img/'+item.filename

#    クエリベクトル生成機能
    def ext_mean_rgb(filepath):
      image = np.array(Image.open(filepath).convert('RGB')).reshape(-1,3)
      return np.array([np.mean(image[:,0]),np.mean(image[:,1]),np.mean(image[:,2])])
    qvec=ext_mean_rgb(filepath)

#    meta.csv読み込み機能
    df = pd.read_csv('./cgi-bin/metadata/metadata_buttoms.csv', index_col=0)
    tfilepaths=df['imgname']
    rgbs=df[['R','G','B']]

#    qvecとコサイン類似度を計算する
    def comp_sim(qvec,tvec):
        return np.dot(qvec, tvec) / (np.linalg.norm(qvec) * np.linalg.norm(tvec))
    
    result=np.array([])
    for i in range(rgbs.index.shape[0]):
      result=np.append(result, comp_sim(qvec, rgbs.iloc[i,:].to_numpy()))

#    類似度が大きい順にソートして表示
    rank=np.argsort(result)
    
    for index in rank[:-rank.shape[0]+1:-10000]:
        title.append('{}'.format(tfilepaths[index]))
    
    for index in rank[:-rank.shape[0]+1:-10000]:
        score.append('{}'.format(result[index]))
     
    contents3='<table border="1">'
    for index in rank[:-rank.shape[0]+1:-10000]:
        contents3=contents3+'<tr><td><img src=".'+tfilepaths[index]+'" width="25%" hight="auto"></td><td>'+str(result[index])+'</td></tr>'
    contents3=contents3+'</table>'
    label3='<h2>ボトムス</h2>'

#num=sum(qvec == 1)
#print (html % (df3, contents))
#print (html %  contents1)
print (html % (label1, contents1, label2, contents2, label3 ,contents3))
