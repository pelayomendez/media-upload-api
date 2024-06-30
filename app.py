import os
from dotenv import load_dotenv

import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import Flask, render_template, request

# Env variable
load_dotenv()
CLOUD_NAME = os.getenv('CLOUD_NAME')
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# Configuration       
cloudinary.config( 
    cloud_name = CLOUD_NAME, 
    api_key = API_KEY, 
    api_secret = API_SECRET,
    secure=True
)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    upload_result = None
    thumbnail_url1 = None
    thumbnail_url2 = None
    if request.method == 'POST':
        file_to_upload = request.files['file']
        if file_to_upload:
            upload_result = upload(file_to_upload)
            thumbnail_url1, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=100,
                                                     height=100)
            thumbnail_url2, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=200,
                                                     height=100, radius=20, effect="sepia")
    return render_template('upload_form.html', upload_result=upload_result, thumbnail_url1=thumbnail_url1,
                           thumbnail_url2=thumbnail_url2)


if __name__ == "__main__":
    app.debug = True
    app.run()