# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 11:32:05 2020

@author: Piyush Soni
"""

import os
from flask import Flask, flash, request, redirect, url_for, render_template, make_response
from werkzeug.utils import secure_filename

import urllib
import numpy as np
import cv2

from image_processing.image_processor import detect_extract

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload_display.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed')
		return render_template('upload_display.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)
"""
@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
    
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
"""
@app.route('/display/<filename>', methods=['GET'])
def process(filename):
    #print("path: {}".format(os.path.join('uploads', filename)))
    img = cv2.imread(os.path.join('uploads', filename), cv2.IMREAD_GRAYSCALE)
    
    
    # Do some processing, get output_img
    #detected_sudoku, extracted_sudoku = detect_extract(img)
    #print("shape: {}".format(img.shape))
    #img = cv2.bitwise_not(img)
   
    retval, buffer = cv2.imencode('.png', img)
    response = make_response(buffer)
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__ == "__main__":
    app.run()
