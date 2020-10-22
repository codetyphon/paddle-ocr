paddle OCR ：paddlepaddle + flask + react

一、API安装：

首先安装paddlepaddle。

```
python3 -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
```


[选项1] api_for_hub 端口8080

paddlehub 可提供RESTful API， https://github.com/PaddlePaddle/PaddleHub/blob/release/v1.8/docs/tutorial/serving.md

但它不具备跨域功能。使用flask通过shell调用hub命令，并对返回的字符串进行处理，封装成json结果。

安装 paddlehub
```
python3 -m pip install paddlehub -i https://mirror.baidu.com/pypi/simple
```

安装文字识别模型
```
hub install chinese_ocr_db_crnn_mobile
hub install chinese_text_detection_db_mobile
```

启动api服务
```
python3 app.py
```



[选项2] api_for_ocr 端口 8081

安装 paddleocr
```
pip3 install paddleocr
```

启动
```
python3 app2.py
```

第一次启动，它会自动下载模型，并只下载一次。


两个选项不必同时运行。可根据实际情况选择运行哪一个API。

二、前端：

进入web目录：

安装
```
yarn install
```

调试
```
yarn start
```

编译
```
yarn build
```

编译后，把index.html放在 templates 目录中，把其他文件放在public文件中。


