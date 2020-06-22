#!/usr/bin/env python3

import flask
import werkzeug.utils as wu
import os
from image_processing.image_processor import detect_extract
import cv2

import sudoku_solver as ss

UPLOAD_FOLDER = 'static/uploads/'

#Creating a new Flask Web application. It accepts the package name.
app = flask.Flask("flask_web_app")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/<filename>')
def send_file(filename):
    return flask.send_from_directory(UPLOAD_FOLDER, filename)

def CNN_predict():
    """
    Reads the uploaded image file and predicts its label using the saved pre-trained CNN model.
    :return: Either an error if the image is not for CIFAR10 dataset or redirects the browser to a new page to show the prediction result if no error occurred.
    """
    
    """
    Setting the previously created 'secure_filename' to global.
    This is because to be able invoke a global variable created in another function, it must be defined global in the caller function.
    """
    global secure_filename
    #Reading the image file from the path it was saved in previously.
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename)
    img = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
    sudoku, cropped = detect_extract(img)
    
    secure_cropped_name = wu.secure_filename('cropped.jpg')
    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'cropped.jpg'), cropped)
    cropped_path=os.path.join(app.config['UPLOAD_FOLDER'], secure_cropped_name)
    
    isValid, solved = ss.main(sudoku)
    """
    After predicting the class label of the input image, the prediction label is rendered on an HTML page.
    The HTML page is fetched from the /templates directory. The HTML page accepts an input which is the predicted class.
    """
    return flask.render_template(template_name_or_list="prediction_result.html", detected_sudoku=sudoku, solved=solved, isValid=str(isValid), filename=original_path, cropped=cropped_path)


"""
Creating a route between the URL (http://localhost:7777/predict) to a viewer function that is called after navigating to such URL. 
Endpoint 'predict' is used to make the route reusable without hard-coding it later.
"""
app.add_url_rule(rule="/predict/", endpoint="predict", view_func=CNN_predict)

def upload_image():
    """
    Viewer function that is called in response to getting to the 'http://localhost:7777/upload' URL.
    It uploads the selected image to the server.
    :return: redirects the application to a new page for predicting the class of the image.
    """
    #Global variable to hold the name of the image file for reuse later in prediction by the 'CNN_predict' viewer functions.
    global secure_filename
    if flask.request.method == "POST":#Checking of the HTTP method initiating the request is POST.
        img_file = flask.request.files["image_file"]#Getting the file name to get uploaded.
        secure_filename = wu.secure_filename(img_file.filename)#Getting a secure file name. It is a good practice to use it.
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename)#Preparing the full path under which the image will get saved.
        img_file.save(img_path)#Saving the image in the specified path.
        print("Image uploaded successfully.")
        """
        After uploading the image file successfully, next is to predict the class label of it.
        The application will fetch the URL that is tied to the HTML page responsible for prediction and redirects the browser to it.
        The URL is fetched using the endpoint 'predict'.
        """
        return flask.redirect(flask.url_for(endpoint="predict"))
    return "Image upload failed."

"""
Creating a route between the URL (http://localhost:7777/upload) to a viewer function that is called after navigating to such URL. 
Endpoint 'upload' is used to make the route reusable without hard-coding it later.
The set of HTTP method the viewer function is to respond to is added using the 'methods' argument.
In this case, the function will just respond to requests of method of type POST.
"""
app.add_url_rule(rule="/upload/", endpoint="upload", view_func=upload_image, methods=["POST"])

def redirect_upload():
    """
    A viewer function that redirects the Web application from the root to a HTML page for uploading an image to get classified.
    The HTML page is located under the /templates directory of the application.
    :return: HTML page used for uploading an image. It is 'upload_image.html' in this exmaple.
    """
    return flask.render_template(template_name_or_list="upload_image.html")
"""
Creating a route between the homepage URL (http://localhost:7777) to a viewer function that is called after getting to such URL. 
Endpoint 'homepage' is used to make the route reusable without hard-coding it later.
"""
app.add_url_rule(rule="/", endpoint="homepage", view_func=redirect_upload)



"""
To activate the Web server to receive requests, the application must run.
A good practice is to check whether the file is whether the file called from an external Python file or not.
If not, then it will run.
"""
if __name__ == "__main__":
    """
    In this example, the app will run based on the following properties:
    host: localhost
    port: 7777
    debug: flag set to True to return debugging information.
    """

    app.run(host="localhost", port=7777, debug=True)