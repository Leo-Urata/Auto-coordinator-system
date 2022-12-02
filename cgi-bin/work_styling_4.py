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
        
        <div class="card">
            <img src="../styling_img/women1.jpg" class="card-img-top" alt="...">
            <div class="card-body">
            <h5 class="card-title">Women's styling 1</h5>
            </div>
        </div>
        
        <h4 class="m-3">このスタイリングに使用されているアイテム</h4>
        <table class="table">
          <thead>
            <tr>

              <th scope="col">トップス</th>
              <th scope="col">ボトムス</th>
            </tr>
          </thead>
          <tbody>
            <tr>

              <td><img src="../styling_tops_img/top4.jpg" class="img-fluid"></td>
              <td><img src="../styling_buttoms_img/but4.jpg" class="img-fluid"></td>
            </tr>
          </tbody>
        </table>
        
        <form action="work_styling_4.py" method="post" enctype="multipart/form-data">
            <div class="input-group m-3">
                <div class="input-group-prepend">
                  <div class="input-group-text">
                    <input type="checkbox" name="コーディネート" value="[1]" />コーディネートする
                  </div>
                </div>
            </div>
            <div class="m-3">
                <button type="submit" class="btn btn-primary">検索</button>
            </div>
        </form>

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

contents2=''
contents3=''

label2=''
label3=''

title_tops=[]
title_buttoms=[]

score_tops=[]
score_buttoms=[]
form = cgi.FieldStorage()


#ここから新しい処理
if form.getfirst('コーディネート'):
#    cgi用パス

    filepath_tops='./styling_tops_img/top4.jpg'
    filepath_buttoms='./styling_buttoms_img/but4.jpg'
    

#    クエリベクトル生成機能
    def ext_mean_rgb(filepath):
      image = np.array(Image.open(filepath).convert('RGB')).reshape(-1,3)
      return np.array([np.mean(image[:,0]),np.mean(image[:,1]),np.mean(image[:,2])])

    qvec_tops=ext_mean_rgb(filepath_tops)
    qvec_buttoms=ext_mean_rgb(filepath_buttoms)

#    meta.csv読み込み機能

    
    df_tops = pd.read_csv('./cgi-bin/metadata/metadata_tops.csv', index_col=0)
    tfilepaths_tops=df_tops['imgname']
    rgbs_tops=df_tops[['R','G','B']]
    
    df_buttoms = pd.read_csv('./cgi-bin/metadata/metadata_buttoms.csv', index_col=0)
    tfilepaths_buttoms=df_buttoms['imgname']
    rgbs_buttoms=df_buttoms[['R','G','B']]

#    qvecとコサイン類似度を計算する
    def comp_sim(qvec,tvec):
        return np.dot(qvec, tvec) / (np.linalg.norm(qvec) * np.linalg.norm(tvec))
    

    result_tops=np.array([])
    result_buttoms=np.array([])
    
      
    for i in range(rgbs_tops.index.shape[0]):
      result_tops=np.append(result_tops, comp_sim(qvec_tops, rgbs_tops.iloc[i,:].to_numpy()))
      
    for i in range(rgbs_buttoms.index.shape[0]):
      result_buttoms=np.append(result_buttoms, comp_sim(qvec_buttoms, rgbs_buttoms.iloc[i,:].to_numpy()))

#    類似度が大きい順にソートして表示
    rank_tops=np.argsort(result_tops)
    rank_buttoms=np.argsort(result_buttoms)
    
        
    for index in rank_tops[:-rank_tops.shape[0]+1:-10000]:
        title_tops.append('{}'.format(tfilepaths_tops[index]))
    
    for index in rank_tops[:-rank_tops.shape[0]+1:-10000]:
        score_tops.append('{}'.format(result_tops[index]))
        
    for index in rank_buttoms[:-rank_buttoms.shape[0]+1:-10000]:
        title_buttoms.append('{}'.format(tfilepaths_buttoms[index]))
    
    for index in rank_buttoms[:-rank_buttoms.shape[0]+1:-10000]:
        score_buttoms.append('{}'.format(result_buttoms[index]))
     
    
    contents2='<table border="1">'
    for index in rank_tops[:-rank_tops.shape[0]+1:-10000]:
        contents2=contents2+'<tr><td><img src=".'+tfilepaths_tops[index]+'" width="25%" hight="auto"></td><td>'+str(result_tops[index])+'</td></tr>'
    contents2=contents2+'</table>'
    
    contents3='<table border="1">'
    for index in rank_buttoms[:-rank_buttoms.shape[0]+1:-10000]:
        contents3=contents3+'<tr><td><img src=".'+tfilepaths_buttoms[index]+'" width="25%" hight="auto"></td><td>'+str(result_buttoms[index])+'</td></tr>'
    contents3=contents3+'</table>'
    

    label2='<h2>トップス</h2>'
    label3='<h2>ボトムス</h2>'

print (html % (label2, contents2, label3 ,contents3))
