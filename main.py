from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
from pydantic import BaseModel
from service.sql import CloudSqlConnector

class Item(BaseModel):
    soil_moisture: int
    soil_temperature: int
    gravity: int


app = FastAPI(
    title="Aiot Project",
    description="Aiot Project",
    version="0.1.0"
)

SqlApi = CloudSqlConnector()

@app.get('/')
def main():
    return 'test ok'

@app.post('/data')
def data(item: Item):
    # TODO: get data ()
    # TODO: webcrawl weather condition
    pass

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler():
    return RedirectResponse("/")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0",port=8080)
