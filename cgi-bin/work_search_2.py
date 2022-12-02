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
    

    
    <div class="container bg-light">
        <!--men's一覧1行目-->
        <div id="card">
            <h1 class="pt-3 ml-3"><span class="badge badge-secondary">オートコーディネーター</span></h1>
            %s
            <h2 class="text-center py-3">スタイリングテンプレート</h2>
        </div>
        <div class="row">
            <div class="col-md-4 col-12">
            <div class="card">
                <img src="../styling_img/men1.jpg" class="card-img-top" alt="...">
                <div class="card-body">
                <h5 class="card-title">Men's styling 1</h5>
                <a href=http://localhost:8888/cgi-bin/work_styling_1.py class="btn btn-primary">詳しく見る</a>
                </div>
            </div>
            </div>
            <div class="col-md-4 col-12">
            <div class="card">
                <img src="../styling_img/men2.jpg" class="card-img-top" alt="...">
                <div class="card-body">
                <h5 class="card-title">Men's styling 2</h5>
                <a href=http://localhost:8888/cgi-bin/work_styling_2.py class="btn btn-primary">詳しく見る</a>
                </div>
            </div>
            </div>
            <div class="col-md-4 col-12">
            <div class="card">
                <img src="../styling_img/men3.jpg" class="card-img-top" alt="...">
                <div class="card-body">
                <h5 class="card-title">Men's styling 3</h5>
                <a href=http://localhost:8888/cgi-bin/work_styling_3.py class="btn btn-primary">詳しく見る</a>
                </div>
            </div>
            </div>
        </div>
        <!--women's一覧２行目-->
        <div id="card" class="py-3"></div>
        <div class="row">
            <div class="col-md-4 col-12">
            <div class="card">
                <img src="../styling_img/women1.jpg" class="card-img-top" alt="...">
                <div class="card-body">
                <h5 class="card-title">Women's styling 1</h5>
                <a href=http://localhost:8888/cgi-bin/work_styling_4.py class="btn btn-primary">詳しく見る</a>
                </div>
            </div>
            </div>
            <div class="col-md-4 col-12">
            <div class="card">
                <img src="../styling_img/women2.jpg" class="card-img-top" alt="...">
                <div class="card-body">
                <h5 class="card-title">Women's styling 2</h5>
                <a href=http://localhost:8888/cgi-bin/work_styling_5.py class="btn btn-primary">詳しく見る</a>
                </div>
            </div>
            </div>
            <div class="col-md-4 col-12">
            <div class="card">
                <img src="../styling_img/women3.jpg" class="card-img-top" alt="...">
                <div class="card-body">
                <h5 class="card-title">Women's styling 3</h5>
                <a href=http://localhost:8888/cgi-bin/work_styling_6.py class="btn btn-primary">詳しく見る</a>
                </div>
            </div>
            </div>
        </div>
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

