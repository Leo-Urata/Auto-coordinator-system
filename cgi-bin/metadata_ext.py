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
    
    <h1 class="m-3">ファイルをアップロードする</h1>
    %s
    <table border="1">
        <tr>%s</tr>
    </table>
    %s
    <table border="1">
        <tr>%s</tr>
    </table>
    %s
    <p>%s</p>
    <form action="metadata_ext.py" method="post" enctype="multipart/form-data">
      <input type="file" name="file" />
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
df1=''
df2=''
df3=''
df4=''
df5=''
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
    
#    cgi用パス
    filepath='./img/'+item.filename
#    content用パス
    Filepath='../img/'+item.filename
#    content2 AKAZE用パス
    filepath2='../img/akaze_'+item.filename
    
#    rgb値
    def ext_mean_rgb(filepath):
        image = np.array(Image.open(filepath).convert('RGB')).reshape(-1,3)
        return np.array([np.mean(image[:,0]),np.mean(image[:,1]),np.mean(image[:,2])])
        
    def metadata_rgb_write(filepath):
        rgb=ext_mean_rgb(filepath)
#        f = open('./cgi-bin/metadata_rgb.csv', 'a+')
        f = open('./cgi-bin/metadata.csv', 'a+')
        f.write(filepath+','+str(rgb[0])+','+str(rgb[1])+','+str(rgb[2])+'\n')
        f.close()
#        df = pd.read_csv('./cgi-bin/metadata_rgb.csv', header=None)
        df = pd.read_csv('./cgi-bin/metadata.csv', header=None)
        return df
        
#    AKAZE
    def display(img):
        fig = plt.figure(figsize=(12,10))
        ax = fig.add_subplot(111)
        ax.imshow(img, cmap='gray')
        plt.savefig('./img/akaze_'+item.filename)
    
    file01 = cv.imread(filepath,0)
    akaze = cv.AKAZE_create()
    kp1, des1 = akaze.detectAndCompute(file01,None)
    
    kp_akaze = cv.drawKeypoints(file01, kp1, None, flags=4)
    display(kp_akaze)
    
#    顔の特徴量
    mtcnn = MTCNN()
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    
    def metadata_face_write(filepath):
        img = Image.open(filepath)
        img = img.convert('RGB')
        pixels = np.asarray(img)

        # 顔の領域を抽出する
        faces = mtcnn(pixels)
        # resnetのモデルを用いて512次元の顔特徴量を抽出する
        feature_vector = resnet(faces.unsqueeze(0)).squeeze().to('cpu').detach().numpy().copy()
        feature_vector

        text=filepath
        for value in feature_vector:
            text=text+','+str(value)

        f = open('./cgi-bin/metadata_face.csv', 'a+')
        f.write(text+'\n')
        f.close()
        df = pd.read_csv('./cgi-bin/metadata_face.csv', header=None)
        return df
    
#    rgb値出力
    df1 = metadata_rgb_write(filepath)
    df2 = df1.to_html()
#    csv1 = df1.to_csv('./cgi-bin/metadata.csv', mode='w')
    
    rgb1 =df1.iat[-1,1]
    rgb2 =df1.iat[-1,2]
    rgb3 =df1.iat[-1,3]
    
#    顔特徴量出力
    df3 = metadata_face_write(filepath)
    df4 = df3[-1:]
    df5 = df4.to_html()
#    csv2 = df3.to_csv('./cgi-bin/metadata_face.csv', mode='w')
    
#    AKAZE出力
#    df6 = pd.DataFrame(data=[{"imgname":filepath,"len(kp)":len(kp1),"len(des)":len(des1)}],index=['1'])
#    csv3 = df6.to_csv('./cgi-bin/metadata_akaze.csv', mode='a')
    
#    ここ使えるかも
    df6 = open('./cgi-bin/metadata_akaze.csv', 'a+')
    df6.write(filepath+','+str(len(kp1))+','+str(len(des1))+'\n')
    df6.close()
    
#    html出力
    content1='<h2>rgb値</h2>'
    content2='<th><img src="'+Filepath+'" width="30%" height="auto"></th> <th>'+str(rgb1)+'</th> <th>'+str(rgb2)+'</th> <th>'+str(rgb3)+'</th>'
    content3='<h2>AKAZE</h2>'
    content4='<th><img src="'+Filepath+'" width="45%" height="auto"></th> <th><img src="'+filepath2+'" width="40%" height="auto"</th>'
    content5='<h2>顔特徴量</h2>'
    
print (html % (content1, content2, content3, content4, content5, df5))
