#!/usr/bin/env python

import os
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask import send_from_directory, session

from magesty import tune_layers, read_file_to_buf, calc_layer_printing_time, list_diff

# from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "super secret key"

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'download'
ALLOWED_EXTENSIONS = set(['txt', 'gcode'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

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


#@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return "<div><h3>File uploaded</h3></div>" + filename
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<filename>')
def download_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload', methods=['GET', 'POST'])
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
            flash('yooououououou')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # azam
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            buf, num_layers = read_file_to_buf(file_path)

            # calculate each layer printing time
            tb_tuned_layers = calc_layer_printing_time(filename, buf)
            
            # enable default settings for these layers
            layers_down = list_diff([x for x in range(0, num_layers)], tb_tuned_layers)

            param_to_tune = "M106 S0"  # TEMP_MAGIC, FLOW_MAGIC
            param_default = "M106 S255" # TEMP_DEFAULT, FLOW_DEFAULT

            tune_layers(file_path, buf, tb_tuned_layers, layers_down, param_to_tune, param_default)
            file.save(os.path.join(app.config['DOWNLOAD_FOLDER'], filename))

            #return redirect(url_for('uploaded_file', filename=filename))
            #return render_template("generated.html", path="download/"+filename)
            #return download_file(filename)
            path = app.config['UPLOAD_FOLDER']+'/'+filename
            return jsonify({"path":path})
    #return render_template("index.html")
    return "<h3>render_template('index.html')</h3>"

    '''
    <!doctype html>
    <title>Upload Gcode</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)



'''

1. Loadbar
2. 



'''