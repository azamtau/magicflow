from flask import Flask, render_template_string, request, jsonify, url_for, render_template
import os
from werkzeug.utils import secure_filename

if not os.path.isdir("/static"):  # just for this example
    os.makedirs("/static")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    file = request.files['file']
    fname = secure_filename(file.filename)
    file.save('static/' + fname)
    # do the processing here and save the new file in static/
    fname_after_processing = fname
    return jsonify({'result_file_location': url_for('static', filename=fname_after_processing)})

  return render_template("index.html")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)