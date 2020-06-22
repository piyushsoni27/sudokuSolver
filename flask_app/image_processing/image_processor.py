# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 19:01:00 2020

@author: Piyush
"""
import cv2
if __name__ == '__main__':
    import image_processor_utils as im_utils
else:
    import image_processing.image_processor_utils as im_utils

### parameters
## options: 'open'(erode->dilate), 'close'(dilate->Erode), 'dilate', 'erode'
MORPH_OP_PREPROCESS_IMAGE="open"  
CROPPED_SQUARE_IMAGE_SIDE=400

global model

def detect_extract(img):
    processed = im_utils.pre_process_image(img, morph_operation=MORPH_OP_PREPROCESS_IMAGE)
    
    #im_utils.plot_images(original, 'original')
    #im_utils.plot_images(processed, 'processed')
    
    corners = im_utils.find_corners_of_largest_polygon(processed)
    #im_utils.display_points(original, corners)
    
    cropped = im_utils.crop_and_warp(img, corners)
    resized = cv2.resize(cropped, (CROPPED_SQUARE_IMAGE_SIDE, CROPPED_SQUARE_IMAGE_SIDE), interpolation=cv2.INTER_AREA)
    
    #resize_process= im_utils.pre_process_image(resized)
    #im_utils.plot_images(cropped, 'resize_process')
    
    squares = im_utils.infer_grid(resized)
    sudoku = im_utils.get_digits(resized, squares, 28, model, morph_op="close")
    
    # im_utils.show_digits(digits)
    return sudoku, cropped

if __name__ == "__main__":
    img = '../../images/7.jpg'
    img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    model = '../../text_recognizer_models/digit_recognizer_keras_224_tf_110.h5'
    
    sudoku, _ = detect_extract(img)
    print(sudoku)
    print(type(sudoku))
    
else:
    model = '../text_recognizer_models/digit_recognizer_keras_224_tf_110.h5'