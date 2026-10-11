from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import qrcode

app = FastAPI()
templates = Jinja2Templates(directory=".")

if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"img": None}
    )

@app.post("/cr", response_class=HTMLResponse)
def cr_(request: Request, url_input: str = Form(...)):
    qr = qrcode.QRCode(version=1)
    qr.add_data(url_input)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white") 
    
    file_path = "static/my_qrcode.png"
    img.save(file_path) 
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"img": file_path}
    )

