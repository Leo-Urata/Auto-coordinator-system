#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

html = '''Content-type: text/html;

<html lang="ja">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">


    <title>人工知能(AI)アルゴリズムデザイン) 2022</title>
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
    
    <div>
    <img src="../home_img/home_img1.png" class="img-fluid">
    </div>
    
    
    <div class="text-center py3">
        <h2 class="m-3">使い方</h2>
        %s
    </div>
    
    <div class="container-fluid bg-light">
        <h2><span class="badge badge-success ml-5">STEP 1</span></h2>
    </div>
    
    <div class="text-center py3 m-3">
        <h3>自分の持っている洋服の写真を撮る</h3>
        <img src="../home_img/home_img2.png" class="w-50 h-50">
    </div>
    
    <div class="container-fluid bg-light">
        <h2><span class="badge badge-success ml-5">STEP 2</span></h2>
    </div>
    
    <div class="text-center py3 m-3">
        <h3>撮影したアイテムを登録する</h3>
        <img src="../home_img/home_img3.png" class="w-50 h-50">
    </div>
    
    <div class="container-fluid bg-light">
        <h2><span class="badge badge-success ml-5">STEP 3</span></h2>
    </div>
    
    <div class="text-center py3 m-3">
        <h3>オートコーディネーターに写真をアップロードする</h3>
        <img src="../home_img/home_img4.png" class="w-50 h-50">
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
