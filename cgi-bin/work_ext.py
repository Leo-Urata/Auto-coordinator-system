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

    <title>アイテム登録</title>
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
        <h1 class="pt-3 ml-3"><span class="badge badge-secondary">アイテム登録</span></h1>
        %s
        <table border="1">
            <tr>%s</tr>
        </table>
        %s
        <table border="1">
            <tr>%s</tr>
        </table>
        %s
        <table border="1">
            <tr>%s</tr>
        </table>
        <form class="was-validated" action="work_ext.py" method="post" enctype="multipart/form-data">
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

content1=''
content2=''
content3=''
content4=''
content5=''
content6=''
df1=''
df2=''
df3=''
df4=''
df5=''
df6=''
files=[]
form = cgi.FieldStorage()

###アウター用
if 'outer_file' in form:
    item = form['outer_file']
    if item.file:
        fout = open(os.path.join('./outer_img/', item.filename), 'wb')
        while True:
            chunk = item.file.read(1000000)
            if not chunk:
                break
            fout.write(chunk)
        fout.close()
    
#    cgi用パス
    filepath='./outer_img/'+item.filename
#    content用パス
    Filepath='../outer_img/'+item.filename

#    rgb値
    def ext_mean_rgb(filepath):
        image = np.array(Image.open(filepath).convert('RGB')).reshape(-1,3)
        return np.array([np.mean(image[:,0]),np.mean(image[:,1]),np.mean(image[:,2])])
        
    def metadata_rgb_write(filepath):
        rgb=ext_mean_rgb(filepath)
#        f = open('./cgi-bin/metadata_rgb.csv', 'a+')
        f = open('./cgi-bin/metadata/metadata_outer.csv', 'a')
        f.write(filepath+','+str(rgb[0])+','+str(rgb[1])+','+str(rgb[2])+'\n')
        f.close()
#        df = pd.read_csv('./cgi-bin/metadata_rgb.csv', header=None)
        df = pd.read_csv('./cgi-bin/metadata/metadata_outer.csv', header=None)
        return df
        
#    試し機能
    def metadata_write(filepath):
        f = open('./cgi-bin/metadata/metadata_outer_img.csv', 'a')
        f.write(filepath+'\n')
        f.close()
        df = pd.read_csv('./cgi-bin/metadata/metadata_outer_img.csv', header=None)
        return df
        
#    rgb値出力
    df1 = metadata_rgb_write(filepath)
    df2 = df1.to_html()
#    csv1 = df1.to_csv('./cgi-bin/metadata.csv', mode='w')

#    試し機能出力
    out = metadata_write(filepath)
    
    rgb1 =df1.iat[-1,1]
    rgb2 =df1.iat[-1,2]
    rgb3 =df1.iat[-1,3]
#    html出力
    content1='<h3>アウター</h3>'
    content2='<th><img src="'+Filepath+'" width="30%" height="auto"></th> <th>'+str(rgb1)+'</th> <th>'+str(rgb2)+'</th> <th>'+str(rgb3)+'</th>'
    
    
### トップス用
if 'tops_file' in form:
    item = form['tops_file']
    if item.file:
        fout = open(os.path.join('./tops_img/', item.filename), 'wb')
        while True:
            chunk = item.file.read(1000000)
            if not chunk:
                break
            fout.write(chunk)
        fout.close()
    
#    cgi用パス
    filepath='./tops_img/'+item.filename
#    content用パス
    Filepath='../tops_img/'+item.filename

#    rgb値
    def ext_mean_rgb(filepath):
        image = np.array(Image.open(filepath).convert('RGB')).reshape(-1,3)
        return np.array([np.mean(image[:,0]),np.mean(image[:,1]),np.mean(image[:,2])])
        
    def metadata_rgb_write(filepath):
        rgb=ext_mean_rgb(filepath)
#        f = open('./cgi-bin/metadata_rgb.csv', 'a+')
        f = open('./cgi-bin/metadata/metadata_tops.csv', 'a+')
        f.write(filepath+','+str(rgb[0])+','+str(rgb[1])+','+str(rgb[2])+'\n')
        f.close()
#        df = pd.read_csv('./cgi-bin/metadata_rgb.csv', header=None)
        df = pd.read_csv('./cgi-bin/metadata/metadata_tops.csv', header=None)
        return df
        
#    試し機能
    def metadata_write(filepath):
        f = open('./cgi-bin/metadata/metadata_tops_img.csv', 'a')
        f.write(filepath+'\n')
        f.close()
        df = pd.read_csv('./cgi-bin/metadata/metadata_tops_img.csv', header=None)
        return df
        
#    rgb値出力
    df3 = metadata_rgb_write(filepath)
    df4 = df1.to_html()
#    csv1 = df1.to_csv('./cgi-bin/metadata.csv', mode='w')

#    試し機能出力
    top = metadata_write(filepath)
    
    rgb4 =df1.iat[-1,1]
    rgb5 =df1.iat[-1,2]
    rgb6 =df1.iat[-1,3]
#    html出力
    content3='<h3>トップス</h3>'
    content4='<th><img src="'+Filepath+'" width="30%" height="auto"></th> <th>'+str(rgb1)+'</th> <th>'+str(rgb2)+'</th> <th>'+str(rgb3)+'</th>'
    
###ボトムス用
if 'buttoms_file' in form:
    item = form['buttoms_file']
    if item.file:
        fout = open(os.path.join('./buttoms_img/', item.filename), 'wb')
        while True:
            chunk = item.file.read(1000000)
            if not chunk:
                break
            fout.write(chunk)
        fout.close()
    
#    cgi用パス
    filepath='./buttoms_img/'+item.filename
#    content用パス
    Filepath='../buttoms_img/'+item.filename

#    rgb値
    def ext_mean_rgb(filepath):
        image = np.array(Image.open(filepath).convert('RGB')).reshape(-1,3)
        return np.array([np.mean(image[:,0]),np.mean(image[:,1]),np.mean(image[:,2])])
        
    def metadata_rgb_write(filepath):
        rgb=ext_mean_rgb(filepath)
#        f = open('./cgi-bin/metadata_rgb.csv', 'a+')
        f = open('./cgi-bin/metadata/metadata_buttoms.csv', 'a+')
        f.write(filepath+','+str(rgb[0])+','+str(rgb[1])+','+str(rgb[2])+'\n')
        f.close()
#        df = pd.read_csv('./cgi-bin/metadata_rgb.csv', header=None)
        df = pd.read_csv('./cgi-bin/metadata/metadata_buttoms.csv', header=None)
        return df
        
#    試し機能
    def metadata_write(filepath):
        f = open('./cgi-bin/metadata/metadata_buttoms_img.csv', 'a')
        f.write(filepath+'\n')
        f.close()
        df = pd.read_csv('./cgi-bin/metadata/metadata_buttoms_img.csv', header=None)
        return df
        
#    rgb値出力
    df5 = metadata_rgb_write(filepath)
    df6 = df1.to_html()
#    csv1 = df1.to_csv('./cgi-bin/metadata.csv', mode='w')

#    試し機能出力
    but = metadata_write(filepath)
    
    rgb7 =df1.iat[-1,1]
    rgb8 =df1.iat[-1,2]
    rgb9 =df1.iat[-1,3]
#    html出力
    content5='<h3>ボトムス</h3>'
    content6='<th><img src="'+Filepath+'" width="30%" height="auto"></th> <th>'+str(rgb1)+'</th> <th>'+str(rgb2)+'</th> <th>'+str(rgb3)+'</th>'
    
print (html % (content1, content2, content3, content4, content5, content6))
