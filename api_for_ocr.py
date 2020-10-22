# coding: utf-8
import os
import uuid
import hashlib
from time import time
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, json
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flasgger import Swagger
from paddleocr import PaddleOCR, draw_ocr
ocr = PaddleOCR()
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(import_name=__name__,
            static_url_path='/', # 配置静态文件的访问 url 前缀
            static_folder='public',    # 配置静态文件的文件夹
            template_folder='templates') # 配置模板文件的文件夹
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
swagger = Swagger(app)
CORS(app)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def html():
    return render_template('index.html')


class Upload(Resource):
    def post(self):
        """上传文件
        ---
        consumes:
            - multipart/form-data
        parameters:
            - name: file
              in: formData
              type: file
              required: true
        definitions:
            err:
                type: object
                properties:
                    err:
                        type: boolean
                    msg:
                        type: string
            ok:
                type: object
                properties:
                    err:
                        type: boolean
                    id:
                        type: string
        responses:
            200:
                description: xxx
                schema:
                    $ref: '#/definitions/err'
                examples:
                    {
                        "created_time": 1602820202.3093352,
                        "stoped_time": 0,
                        "started_time": 0,
                        "file_md5": "f10eb831fb8166e75b4241725b354b50",
                        "finished_time": 0,
                        "result": null,
                        "status": "NotStarted",
                        "uuid": "827cc965-5d7e-4bc5-ac2d-d8a70d7a1684"
                    }

        """
        if 'file' not in request.files:
            return jsonify(err=True, msg='No file part')
        file = request.files['file']
        print(file)
        if file.filename == '':
            return jsonify(err=True, msg='No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            arr = filename.split('.')
            extname = arr[len(arr)-1]

            # pdf = file.read()
            # file_md5 = hashlib.md5(file.read()).hexdigest()
            id = str(uuid.uuid4())
            newfilename = "{}.{}".format(id, extname)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], newfilename)
            file.save(filepath)
            result = ocr.ocr(filepath)
            items = []
            item = dict()
            item["position"] = dict()
            for line in result:
                position = line[0]
                x = position[0][0]
                y = position[0][1]
                w = position[1][0] - position[0][0]
                h = position[3][1] - position[0][1]
                item["position"]["x"] = x
                item["position"]["y"] = y
                item["position"]["w"] = w
                item["position"]["h"] = h
                item["text"] = line[1][0]
                item["confidence"] = line[1][1]
                items.append(item)
            obj_str = str(items).replace("'", '"')
            out = json.loads(obj_str)
            return jsonify(out)
        return jsonify(err=True, msg='file type Not Allowed')


api.add_resource(Upload, '/api/upload')

app.run(port=8081, debug=True, host='0.0.0.0')
