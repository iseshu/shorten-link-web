import os
import tg
import json
import string
import random
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

title = os.environ.get('TITLE','Url Shorten')
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

async def create_url(url):
    with open('data.json', 'r') as f:
        data = json.load(f)
    if url in data['links']:
        return {'url': url,"id": data['ids'][data['links'].index(url)]}
    else:
        id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
        with open('data.json', 'w') as f:
            data['ids'].append(id)
            data['links'].append(url)
            json.dump(data, f)
        return {"id":id,"url":url}




@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse('index.html', {"request": request,"title":title})

@app.get("/o/{id}")
async def dlsc(id: str,request: Request):
    with open('data.json', 'r') as f:
        data = json.load(f)
    if id in data['ids']:
        return RedirectResponse(data['links'][data['ids'].index(id)])
    else:
        return templates.TemplateResponse('404.html', {"request": request,"id":id,"title":title})

@app.get('/api')
async def create(request: Request):
    a = request.query_params.get('url')
    data = await create_url(a)
    return data

@app.post('/telegram')
async def tele(request: Request):
    data = await request.json()
    await tg.telegram(data)
    return data