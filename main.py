from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
from pydantic import BaseModel
from service.sql import CloudSqlConnector

class Item(BaseModel):
    soil_moisture :int
    water_weight :int


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

@app.get('/data_show')
def data():
    
    sent = ''
    result = SqlApi.fetchData('test')
    
    for i in result:
        sent += '\t'.join(i) + '\n'
     
    return sent

@app.post('/data')
def data(item: Item):
    
    stmt = 'INSERT INTO plant_record (soil_moisture, soil_temperature, gravity, weather_temperature) VALUES(:soil_moisture, :soil_temperature, :gravity)'
    
    # TODO: convert class to json
    data = toDict(item)
    
    # TODO: webcrawl weather condition
    data.update({})
    
    for key in data.keys(): 
        
        pass

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler():
    return '404 NOT FOUND'

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0",port=8080)
