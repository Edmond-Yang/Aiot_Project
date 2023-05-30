from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import FileResponse
from starlette.background import BackgroundTask
import uvicorn
from pydantic import BaseModel
from service.sql import CloudSqlConnector
import os

class Item(BaseModel):
    soil_moisture :int
    gravity :int


app = FastAPI(
    title="Aiot Project",
    description="Aiot Project",
    version="0.1.0"
)

SqlApi = CloudSqlConnector()

def toDict(item: Item) -> dict:
    return {'soil_moisture': item.soil_moisture, 'gravity': item.gravity}
    

@app.get('/')
def main():
    return 'test ok'

@app.get('/dataCheck')
def dataCheck():
    
    sent = ''
    result = SqlApi.fetchData('test')
    
    for i in result:
        sent += ','.join(i) + '\n'
        
    with open('data.csv', 'w', encoding='big5') as file:
        file.write('文字,秘密\n')
        file.write(sent)
     
    return FileResponse(
            'data.csv',
            filename='data.csv',
            background=BackgroundTask(lambda: os.remove('data.csv')),
        )

@app.post('/data')
def data(item: Item):
    
    stmt = 'INSERT INTO plant_record (soil_moisture, soil_temperature, gravity, weather_temperature) VALUES(:soil_moisture, :soil_temperature, :gravity)'
    
    # TODO: convert class to json
    data = toDict(item)
    
    # TODO: webcrawl weather condition
    data.update({})
    
    SqlApi.executeQuery(stmt, data)
    

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0",port=8080)
