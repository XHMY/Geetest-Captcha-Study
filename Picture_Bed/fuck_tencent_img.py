from flask import Flask
from flask import send_file
app = Flask(__name__)

@app.route('/<filename>')
def get_image(filename):
    # if request.args.get('type') == '1':
    #    filename = 'ok.gif'
    # else:
    #    filename = 'error.gif'
    return send_file("final/{}".format(filename),mimetype='image/jpg')