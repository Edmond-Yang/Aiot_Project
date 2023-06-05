from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import HTMLResponse
from service.webCrawl import weather_bug
import uvicorn
from pydantic import BaseModel
from service.sql import CloudSqlConnector
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import markdown
from LSTM import LSTM 

class Item(BaseModel):
    temperature :int
    moisture :int
    soil_moisture :int
    gravity: int


app = FastAPI(
    title="Aiot Project",
    description="Aiot Project",
    version="0.1.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


SqlApi = CloudSqlConnector()
WeatherCrawl = weather_bug('臺中市')

def toDict(item: Item) -> dict:
    return {'temperature': item.temperature, 'moisture': item.moisture, 'soil_moisture': item.soil_moisture, 'gravity': item.gravity}
    

@app.get('/')
def main():
    return 'test ok'

@app.get('/execute/{stmt}')
def exec(stmt: str):
    SqlApi.executeQuery(stmt)
    return 'success'

@app.get('/getData')
def getData():
    return SqlApi.fetchData('plants')

@app.get('/lstm')
def LSTM():
    return LSTM.Predict_watering_amount()

@app.get('/DataCheck/plants', response_class=HTMLResponse)
def dataCheck(request: Request):
    
    sent = '''| 編號 | 溫度 | 濕度 | 土壤濕度 | 水重 | 時間 |\n| -- | -- | -- | ---- | -- | -- |\n'''
    
    result = SqlApi.fetchData('plants')

    for n, i in enumerate(result):
        
        for j in range(len(i)) :
            i[j] = str(i[j])
            
        sent += f'| {str(n+1)} | ' + ' | '.join(i) + ' |\n'
        
     
    return templates.TemplateResponse("index.html",{'request':request, 'data' : markdown.markdown(sent, extensions=['markdown.extensions.tables'])})

@app.get('/DataCheck/weather', response_class=HTMLResponse)
def dataCheck(request: Request):
    
    sent = '''| 地區 | 預測種類 | 開始時間 | 結束時間 | 機率 |\n| -- | -- | -- | ---- | -- |\n| '''
    
    result = WeatherCrawl()

    for v in result.values():
            
        sent += f'{v} | '
        
    return templates.TemplateResponse("index.html",{'request':request, 'data' : markdown.markdown(sent, extensions=['markdown.extensions.tables'])})

@app.get('/DataCheck/watering', response_class=HTMLResponse)
def dataCheck(request: Request):
    
    sent = '''| 時間 | 澆水量 |\n| -- | -- |\n'''
    
    result = SqlApi.fetchData('records')
    
    for i in result:
        
        i[0] = str(i[0])
        i[1] = str(i[1])
            
        sent += '| ' + ' | '.join(i) + ' |\n'
        
    return templates.TemplateResponse("index.html",{'request':request, 'data' : markdown.markdown(sent, extensions=['markdown.extensions.tables'])})

@app.post('/data')
def data(item: Item):
    
    stmt = 'INSERT INTO plants (temperature, moisture, soil_moisture, gravity) VALUES(:temperature, :moisture, :soil_moisture, :gravity)'
    
    # TODO: convert class to json
    data = toDict(item)
    
    SqlApi.executeQuery(stmt, data)


@app.get('/getFormattedData')
def getFormattedData():
    
    formattedData = []
    data = SqlApi.fetchData('plants')
    
    for row in data:
        formattedData.append({'temperature': row[0], 'moisture': row[1], 'soil_moisture': row[2], 'gravity': row[3], 'time': row[4]})
    
    return formattedData

@app.get('/getAppData')
def getAppData():
    
    threshold = 10
    data = getFormattedData()
    
    if len(data) > threshold:
        data = data[-threshold:]
        
    data = {'plant': data}
    
    data.update({'weather': WeatherCrawl()})
    data.update({'watering': getWateringData()})
    
    return data


def getWateringData():
    
    threshold = 3
    data = SqlApi.fetchData('records')
    
    result = []
    
    if len(data) > threshold:
        data = data[-threshold:]
    
    for i in data:
        result.append({'time': i[0], 'water': i[1]})
        
    return result

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0",port=8080)
