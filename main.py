from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import HTMLResponse
import uvicorn
from pydantic import BaseModel
from service.sql import CloudSqlConnector
from fastapi.templating import Jinja2Templates
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

templates = Jinja2Templates(directory="templates")

SqlApi = CloudSqlConnector()

def toDict(item: Item) -> dict:
    return {'temperature': item.temperature, 'moisture': item.moisture, 'soil_moisture': item.soil_moisture}
    

@app.get('/')
def main():
    return 'test ok'

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
    

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0",port=8080)
