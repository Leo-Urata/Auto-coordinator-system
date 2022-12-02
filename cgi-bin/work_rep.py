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

    <title>アイテムリスト</title>
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
        <h1 class="pt-3 ml-3"><span class="badge badge-secondary">アイテムリスト</span></h1>
        <form action="work_rep.py" method="post" enctype="multipart/form-data">
            <div class="form-group m-3">
                <div class="btn-group btn-group-toggle ">
                  <label class="btn btn-outline-primary">
                    <input type="radio" name="アウター" value="[1]" />アウター
                  </label>
                  <label class="btn btn-outline-primary">
                    <input type="radio" name="トップス" value="[2]" />トップス
                  </label>
                  <label class="btn btn-outline-primary">
                    <input type="radio" name="ボトムス" value="[3]" />ボトムス
                  </label>
                </div>
            <button type="submit" class="btn btn-primary">検索</button>
            </div>
        </form>
        
        <div class="mt-3 ml-5">%s</div>
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

if form.getfirst('アウター'):
    df = pd.read_csv('./cgi-bin/metadata/metadata_outer_img.csv')
    df['Unnamed: 0'] = df['imgname'].map(lambda s: "<img src='.{}' width='100' />".format(s))
    df.rename(columns={'Unnamed: 0':'アイテム'}, inplace=True)
    df1 = df.to_html(escape=False)

elif form.getfirst('トップス'):
    df = pd.read_csv('./cgi-bin/metadata/metadata_tops_img.csv')
    df['Unnamed: 0'] = df['imgname'].map(lambda s: "<img src='.{}' width='100' />".format(s))
    df.rename(columns={'Unnamed: 0':'アイテム'}, inplace=True)
    df1 = df.to_html(escape=False)

elif form.getfirst('ボトムス'):
    df = pd.read_csv('./cgi-bin/metadata/metadata_buttoms_img.csv')
    df['Unnamed: 0'] = df['imgname'].map(lambda s: "<img src='.{}' width='100' />".format(s))
    df.rename(columns={'Unnamed: 0':'アイテム'}, inplace=True)
    df1 = df.to_html(escape=False)

print (html % df1)
