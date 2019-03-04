#!/usr/bin/env python

import os
from flask import Flask, render_template, flash, request, redirect, url_for
from flask import send_from_directory

# from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'gcode'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#@app.route("/")
#def index():
#    return render_template('index.html')


#@app.route('/add-todo', methods = ['POST'])
#def addTodo():
#	data = json.loads(request.data) # load JSON data from request
#	pusher.trigger('todo', 'item-added', data) # trigger `item-added` event on `todo` channel
#	return jsonify(data)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return "<div><h3>File uploaded</h3></div>"
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download')
def download_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload Gcode</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)
