import React, { useState } from 'react'
import Dropzone from 'react-dropzone'
import ReactLoading from 'react-loading'
import axios, { AxiosRequestConfig, AxiosInstance } from 'axios'
import './App.css'
interface IRect {
  text: string,
  confidence: number,
  position: {
    x: number,
    y: number,
    w: number,
    h: number
  }
}
enum Status{
  ready,
  uploading,
  res_empty,
  res_ok,
  res_err,
  img_err
}
const Text = ({ text, x, y, w, h }: { text: string, x: number, y: number, w: number, h: number }) => {
  return (
    <div className="rect-text"
      style={{
        left: x + "px",
        top: y - 20 + "px",
        width: w + "px",
        height: "20px"
      }}
    >{text}</div>
  )
}
const Rect = ({ text, x, y, w, h }: { text: string, x: number, y: number, w: number, h: number }) => {
  return (
    <div className="rect" style={{
      left: x + "px",
      top: y + "px",
      width: w + "px",
      height: h + "px"
    }}>
    </div>
  )
}
function App() {
  const [src, setSrc] = useState<string>("")
  const [status, setStatus] = useState<Status>(Status.ready)
  const [rects, setRects] = useState<IRect[]>([])
  const onDrop = async (acceptedFiles: File[]) => {
    acceptedFiles.forEach(async (file: File) => {
      console.log(file)
      // reader.readAsArrayBuffer(file)
      if (file.type.includes("image")) {
        setStatus(Status.uploading)
        const reader = new FileReader()
        reader.onload = async () => {
          const base64Str: string = reader.result + ""
          setSrc(base64Str)
        }
        reader.readAsDataURL(file)
        const data = new FormData()
        data.append('file', file)
        console.log(data)
        const res = await axios.post('/api/upload', data);
        const arr:IRect[] = res.data
        console.log(arr)
        if(arr.length==0){
          setStatus(Status.res_ok)
        }else{
          setStatus(Status.res_empty)
        }
        setRects(arr)
      }
    });

  }
  return (
    <div className="App">
      <header className="App-header">
        <Dropzone onDrop={onDrop}>
          {({ getRootProps, getInputProps }) => (
            <div {...getRootProps()}>
              <div className="img-pan">
                <img src={src} />
                {
                  rects.map((rect:IRect,index:number) => {
                    return (
                      <div key={index}>
                        <Rect x={rect.position.x} y={rect.position.y} w={rect.position.w} h={rect.position.h} text={rect.text} />
                        <Text x={rect.position.x} y={rect.position.y} w={rect.position.w} h={rect.position.h} text={rect.text} />
                      </div>
                    )
                  })
                }
              </div>
              {
                src == "" && <p>要死劲儿的把图片拖拽到这里</p>
              }
            </div>
          )}
        </Dropzone>
        {
          status==Status.uploading && <ReactLoading type={"bars"} color={"#fff"} />
        }
      </header>
    </div >
  );
}

export default App;
