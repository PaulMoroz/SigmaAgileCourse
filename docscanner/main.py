from bottle import *
import json
import Recognizer
import os, time

scans = []

@route('/docscanner/<filename>')
def file(filename):
    return static_file(filename, root=r'C:\\xampp\\htdocs\\docscanner')

@route('/docscanner/new_scan', method='POST')
def new_scan():
    global scans;
    
    language = request.forms.get('language')
    files = request.files.getall('item_file')
    
    id = len(scans)
    path = "Recognizer/input/" + str(id)
    scans.insert(id, {  "id": id,
                        "language": language,
                        "input_folder_path": path,
                        "outputs": {}
                     })
                     
    name, ext = os.path.splitext(upload.filename)
    os.mkdir(path)
    for file in files:
        file.save(path)
    
    return json.dumps({"error": 0,
                        "scan_id": id
                        })
                        
@route('/docscanner/download', method='POST')
def download():
    global scans;
    
    id = int(request.forms.get('scan_id'))
    type = int(request.forms.get('type'))
    
    if type not in scans[id]["outputs"]:
        output_path = "Recognizer/output/{1}/{0}.{1}".format(id, type)
        os.system("python Recognizer/main.py Recognizer/input/{0} {2} {1} folder s".format(id, type, output_path))
        time.sleep(3)
        scans[id]["outputs"][type] = output_path
    
    return scans[id]["outputs"][type]
        

run(host='localhost', port=8080)