from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import HTMLResponse
import uvicorn
from pydantic import BaseModel
from service.sql import CloudSqlConnector
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import markdown

class Item(BaseModel):
    temperature :int
    moisture :int
    soil_moisture :int


app = FastAPI(
    title="Aiot Project",
    description="Aiot Project",
    version="0.1.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SqlApi = CloudSqlConnector()

def toDict(item: Item) -> dict:
    return {'temperature': item.temperature, 'moisture': item.moisture, 'soil_moisture': item.soil_moisture}
    

@app.get('/')
def main():
    return 'test ok'

@app.get('/execute/{stmt}')
def exec(stmt: str):
    SqlApi.executeQuery(stmt)

@app.get('/getData')
def getData():
    return SqlApi.fetchData('plants')

@app.get('/dataCheck', response_class=HTMLResponse)
def dataCheck(request: Request):
    
    sent = '''| 溫度 | 濕度 | 土壤濕度 | 水重 | 時間 |\n| -- | -- | ---- | -- | -- |\n'''
    
    result = SqlApi.fetchData('plants')

    for i in result:
        
        for j in range(len(i)) :
            i[j] = str(i[j])
            
        sent += '| ' + ' | '.join(i) + ' |\n'
        
     
    return templates.TemplateResponse("index.html",{'request':request, 'data' : markdown.markdown(sent, extensions=['markdown.extensions.tables'])})


@app.post('/data')
def data(item: Item):
    
    stmt = 'INSERT INTO plants (temperature, moisture, soil_moisture, gravity) VALUES(:temperature, :moisture, :soil_moisture, :gravity)'
    
    # TODO: convert class to json
    data = toDict(item)
    
    # TODO: webcrawl weather condition
    data.update({'gravity': 0})
    
    SqlApi.executeQuery(stmt, data)


@app.get('/getFormattedData')
def getFormattedData():
    
    formattedData = []
    data = SqlApi.fetchData('plants')
    
    if len(data) > 7:
        data = data[-7:]
    
    for row in data:
        formattedData.append({'temperature': row[0], 'moisture': row[1], 'soil_moisture': row[2], 'gravity': row[3], 'time': row[4]})
    
    return formattedData

@app.get('/getAppData')
def getAppData():
    
    appData = {'temperature': [], 'moisture': [], 'soil_moisture': [], 'gravity': [], 'time': []}
    data = SqlApi.fetchData('plants')
    
    if len(data) > 7:
        data = data[-7:]
    
    for row in data:
        appData['temperature'].append(row[0])
        appData['moisture'].append(row[1])
        appData['soil_moisture'].append(row[2])
        appData['gravity'].append(row[3])
        appData['time'].append(row[4])
        
    return appData

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0",port=8080)
