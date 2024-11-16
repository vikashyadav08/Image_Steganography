import io
import os
import time
from flask import Flask, flash, redirect, render_template, request, send_file, url_for
from PIL import Image
import pymongo
from stegano import lsb



app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


UPLOAD_FOLDER = 'hidden_file'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = pymongo.MongoClient("mongodb+srv://gyansanchar:gyansanchar@gyansanchar.z1gbmz8.mongodb.net/stegano")

mydb = client["mydatabase"]
mycollection = mydb["mycollection"]


@app.route('/')
def index():
    return render_template('index.html',textIsHidden=False)
@app.route('/new_design')
def new_design():
    return render_template('new_index.html',textIsHidden=False)
@app.route('/text')
def text():
    return render_template('text.html',textIsHidden=False)
@app.route('/files')
def file():
    return render_template('file.html',textIsHidden=False)
@app.route('/audio')
def audio():
    return render_template('audio.html',textIsHidden=False)
@app.route('/video')
def video():
    return render_template('video.html',textIsHidden=False)
@app.route('/image')
def image():
    return render_template('image.html',textIsHidden=False)

@app.route("/encode",methods=['GET','POST'])
def encode():
    image_file = request.files.get("imageFileEncode")    
    pil_image = Image.open(image_file.stream)

    collection_data = {}

    timestamp = str(int(time.time()))
    collection_data['timestamp'] = timestamp
    file_to_hide = request.files['fileToHide']
    if file_to_hide:
        file_to_hide = request.files['fileToHide']

        new_filename = str(timestamp)+"_"+file_to_hide.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

        file_to_hide.save(file_path)

        collection_data['type']='file'
        collection_data['data'] = file_path
        collection_data['mimetype'] = file_to_hide.mimetype

    else:
        text_to_hide = request.form.get('textToHide')
        collection_data['type'] = 'text'
        collection_data['data'] = text_to_hide

    secret = lsb.hide(pil_image, timestamp)
    
    imgByteArr = io.BytesIO()
    secret.save(imgByteArr, format='PNG')  # Adjust the format as needed
    imgByteArr.seek(0)

    encode_password = request.form.get('encodePassword')
    collection_data['password'] = encode_password
     
    mycollection.insert_one(collection_data)
    return send_file(imgByteArr,
        mimetype='image/png',
        as_attachment=True,
        download_name="encoded_"+image_file.filename)


@app.route("/decode",methods=['GET','POST'])
def decode():

    image_file = request.files.get("imageFileDecode")    
    pil_image = Image.open(image_file.stream)

    timestamp_ = lsb.reveal(pil_image)
    
    encode_password = request.form.get('encodePassword')
    data = mycollection.find_one({"timestamp":timestamp_,"password":encode_password})

    if not data:
        flash("Either invalid file or password")
        return redirect("/")
    
    if data['type']=="text":
        return render_template('text.html',textIsHidden=True,hiddenText=data['data'])

    return send_file(
        data['data'],
        mimetype=data['mimetype'],
        as_attachment=True,
        download_name="decoded_"+"".join(data['data'].split("_")[1:])
        )



if __name__ == "__main__":
    app.run(debug=True)