from flask import Flask, request, redirect, jsonify,send_from_directory,Response
import os
from werkzeug.utils import secure_filename
import json
from flask import send_from_directory
from hurry.filesize import size
from datetime import datetime

app = Flask(__name__,static_url_path='/static')
app.config["UPLOAD_FOLDER"] = "uploads"


@app.route('/js/<path:path>')
def send_js(path):
    print(path)
    return app.send_static_file('js/'+path)

@app.route('/assets/<path:path>')
def send_assets(path):
    print(path)
    return app.send_static_file('assets/'+path)

@app.route("/")
def index():
    #return redirect("/static/index.html")
    return app.send_static_file('index.html')

@app.route("/download")
def downloadPage():
    return redirect("/static/download.html")

@app.route('/deleteFile/<filename>', methods=['GET', 'POST'])
def deleteFile(filename):
    print(filename)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'status':'success'})

@app.route('/static/downloadFile/<filename>', methods=['GET', 'POST'])
def download(filename):
    print(filename)
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)

@app.route("/upload", methods=["POST"])
def upload():
    fileob = request.files["file"]
    filename = secure_filename(fileob.filename)
    save_path = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)

    # open and close to update the access time.
    with open(save_path, "r") as f:
        pass
    resp = { 'answer' : 'File transfer completed'}
    return jsonify(resp)


@app.route("/filenames", methods=["GET"])
def get_filenames():
    filenames = os.listdir("uploads/")

    #modify_time_sort = lambda f: os.stat("uploads/{}".format(f)).st_atime

    def modify_time_sort(file_name):
        file_path = "uploads/{}".format(file_name)
        file_stats = os.stat(file_path)
        last_access_time = file_stats.st_atime
        return last_access_time
    
    def getStat(file_name):
        file_path = "uploads/{}".format(file_name)
        file_stats = os.stat(file_path)
        last_access_time = file_stats.st_atime
        s = file_stats.st_size
        return last_access_time,s
    

    filenames = sorted(filenames, key=modify_time_sort)
    data = []
    
    for i in filenames:
        access,siz = getStat(i)
        data.append({
            'name':i,
            'size':size(siz),
            'date': {
                     'day': str(datetime.fromtimestamp(access).strftime("%B %d, %Y")) ,
                     'time':str(datetime.fromtimestamp(access).strftime("%I:%M %p"))  
                     } 
        })
    #print(data)
    #return jsonify({'files':data})
    return  Response(json.dumps(data),  mimetype='application/json')


if __name__ == '__main__':
    context = ('server.crt', 'server.key')
    app.run(host="0.0.0.0", debug = True, ssl_context = context)
