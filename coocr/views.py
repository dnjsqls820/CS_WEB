from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
import os
import re
import requests
import cv2
import sys
import json
# from requests.aut import AuthBase
####################################################
LIMIT_PX = 2048
LIMIT_BYTE = 2048*2048
LIMIT_BOX = 40
rest_api_key = 'e0c3c269d34bfdaacf092cf675b33742'
###################################################

from PIL import Image
import pytesseract

# pytesseract.pytesseract.tesseract_cdm = "C:/Program Files/Tesseract-OCR/tesseract.exe"

def home(request):

    return render(request, '/home/ubuntu/djangoproject/cs_web/templates/coocr/home.html')

def search(request):
    if request.method== 'POST':
        result = request.POST['result']
        data = {
            'result' : result,
        }
    return render(request,'coocr/search.html', data)



#######################################################

def kakao_ocr_resize(image_path: str):
    """
    ocr detect/recognize api helper
    ocr api의 제약사항이 넘어서는 이미지는 요청 이전에 전처리가 필요.

    pixel 제약사항 초과: resize
    용량 제약사항 초과  : 다른 포맷으로 압축, 이미지 분할 등의 처리 필요. (예제에서 제공하지 않음)

    :param image_path: 이미지파일 경로
    :return:
    """
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape

        # api 사용전에 이미지가 resize된 경우, recognize시 resize된 결과를 사용해야함.
        image_path = "{}_resized.jpg".format(image_path)
        cv2.imwrite(image_path, image)

        return image_path
    return None
    
def kakao_ocr(image_path: str, appkey: str):
    """
    OCR api request example
    :param image_path: 이미지파일 경로
    :param appkey: 카카오 앱 REST API 키
    """
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()


    return requests.post(API_URL, headers=headers, files={"image": data})
    
#############################################################################

def coocr_upload(request):
    context = {}
    context['menutitle'] = 'OCR READ'
    words = ''
    wordInfo = ''
    word_all = ''
    images_folder = '/home/ubuntu/djangoproject/cs_web/coocr/static/source/'
    # global imagename
    if 'uploadfile' in request.FILES:
        uploadfile = request.FILES.get('uploadfile','')
        
        if uploadfile != '':
            name_old = uploadfile.name
            name_ext = os.path.splitext(name_old)[1]
            fs = FileSystemStorage(location=images_folder)
            imagename = fs.save(f"src-{name_old}", uploadfile)
            imgfile = Image.open(f"{images_folder}{imagename}")
            image_path = images_folder + imagename
            appkey = rest_api_key
            resize_impath = kakao_ocr_resize(image_path)
            if resize_impath is not None:
                image_path = resize_impath
                print("원본 대신 리사이즈된 이미지를 사용합니다.")
            #response를 json형태로 변환                                                                                                                                                                     
            output = kakao_ocr(image_path,appkey).json()
            #json에서 정보 추출
            wordInfo = output['result']
            words = wordInfo[0]['recognition_words']
            # filter(str.isalnum, string)메서드를 사용하여 Python의 문자열에서 특수 문자 제거
            result = ''.join(filter(str.isalnum, words))
            context['imgname'] = imagename
            context['resulttext'] = result
    return render(request, 'coocr/home.html', context)
