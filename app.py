import os
from flask import Flask, request, render_template, send_from_directory, request, redirect, url_for, abort
from wand.image import Image
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    for upload in request.files.getlist("file"):
        filename = upload.filename
        destination = "/".join([target, filename])
        upload.save(destination)
    return render_template("index.html", image_name=filename)

@app.route('/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route("/<photo>/info")
def open_an_image_file(photo):
    target = os.path.join(APP_ROOT, 'images/')
    image = os.listdir(target)
    if photo in image:
      with Image(filename = target + "/"+ photo) as img: 
        b = img.width
        c = img.height
        e = img.format
        f = img.size 
        d = str("Image Width : " + str(b) + "  " + "Image Height : " + str(c) + "  " + "Image Format : " + str(e) + " " + "Image Size : " + str(f))
    return render_template("index.html", output = d)

@app.route("/convert")
def convert_images():
    input = "images"
    image = os.listdir(input)
    target = os.path.join(APP_ROOT, 'result/')
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    output = "result"
    for file in image:
        with Image(filename = input+"/"+file) as img: 
            with img.convert('jpg') as converted:
                if "." in file:
                    a = file.split('.')
                    a = a[0] + ".jpg"
                    outpath = os.path.join(output+"/"+a)
                    converted.save(filename = outpath) 
                else:
                    a = file + ".jpg"
                    outpath = os.path.join(output+"/"+a)
                    converted.save(filename = outpath) 
    return render_template("index.html", output = "Images Successfully Converted")

@app.route('/<filename>/converted')
def send_converted_image(filename):
    return send_from_directory("result", filename)

if __name__ == "__main__":
    app.run(port=5555, debug=True)