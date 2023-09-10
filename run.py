import os, sys
import subprocess
from subprocess import Popen
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import argparse
import torch
from models.experimental import attempt_load

#Flask 객체 인스턴스 생성
app = Flask(__name__)
app.debug = True

# def root_path():
# 	'''root 경로 유지'''
# 	real_path = os.path.dirname(os.path.realpath(__file__))
# 	sub_path = "\\".join(real_path.split("\\")[:-1])
# 	return os.chdir(sub_path)


# 메인 페이지 라우팅
@app.route('/') # 접속하는 url
def index():
    return render_template('index.html')

@app.route('/food_get')
def food_get():
   return render_template('food_get.html')

@app.route('/food_post', methods=['GET', 'POST'])
def food_post():
    if request.method == 'POST':
      # root_path()
       
      # User Image
      user_img = request.files['user_img']
      
      filename = secure_filename(user_img.filename)
      # 사용자가 입력한 이미지 경로 설정
      image_path = './Images/'
      # Image폴더가 존재하지 않으면 생성하고, 이미지 저장
      os.makedirs(image_path, exist_ok=True) 
      user_img.save(os.path.join(image_path, filename))
      user_img_path = image_path+str(user_img.filename)
      
      
      ## 학습한 모델로 이미지 detection 및 영양정보 담기

      # detect.py를 서브프로세스로 실행
      process = Popen(["python", "detect.py", "--weights", "epoch_049.pt", '--source', user_img_path], shell=True)
      process.wait()
      
      return render_template('food_post.html')
    
    else:
      return render_template('food_get.html')


if __name__=="__main__":
  
  def load_yolov7_model():
     model = attempt_load('epoch_049.pt', map_location='cpu')
     return model
  
  
  # 앱이 시작될때 모델을 한번 로드
  yolov7_model = load_yolov7_model()
  
  # 서비스 start
  app.run(debug=True, host='127.0.0.1', port=5000)
  
  # host 등을 직접 지정 가능
  # app.run(host="127.0.0.1", port="5000", debug=True)